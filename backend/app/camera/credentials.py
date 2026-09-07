"""Runtime-only camera credential resolution for RTSP authentication."""

from __future__ import annotations

import os
import re
from typing import Optional, Union
from urllib.parse import quote, urlsplit, urlunsplit

from backend.app.core.exceptions import PresynException, ValidationException

_CREDENTIAL_REF_PATTERN = re.compile(r"^[A-Z0-9_]+$")


class CredentialsUnavailableError(PresynException):
    """Raised when runtime environment credentials for a camera are missing or incomplete."""

    def __init__(self, message: str = "Camera credentials unavailable in runtime environment.") -> None:
        super().__init__(message=message, error_code="CREDENTIALS_UNAVAILABLE")


def validate_credential_ref(credential_ref: Optional[str]) -> Optional[str]:
    """Validate that credential_ref conforms to strict alphanumeric uppercase naming convention."""
    if credential_ref is None:
        return None
    ref = credential_ref.strip()
    if not ref:
        return None
    if not _CREDENTIAL_REF_PATTERN.match(ref):
        raise ValidationException(
            "Invalid credential reference format. Expected uppercase alphanumeric characters and underscores."
        )
    return ref


def resolve_camera_runtime_source(
    source_type: str,
    device_index: Optional[int] = None,
    rtsp_url: Optional[str] = None,
    credential_ref: Optional[str] = None,
) -> Union[int, str]:
    """Resolve runtime camera source safely in memory without writing secrets to persistent storage.

    For WEBCAM: returns the integer device index.
    For RTSP without credential_ref: returns the credential-free rtsp_url.
    For RTSP with credential_ref: securely injects environment credentials into the in-memory URI.
    """
    source_upper = str(source_type).upper()
    if "WEBCAM" in source_upper:
        if device_index is None:
            raise ValidationException("WEBCAM camera source requires a valid device_index.")
        return device_index

    if not rtsp_url:
        raise ValidationException("RTSP camera source requires a valid rtsp_url.")

    validated_ref = validate_credential_ref(credential_ref)
    if not validated_ref:
        return rtsp_url

    username_key = f"PRESYN_CAMERA_{validated_ref}_USERNAME"
    password_key = f"PRESYN_CAMERA_{validated_ref}_PASSWORD"

    username = os.environ.get(username_key)
    password = os.environ.get(password_key)

    if username is None or password is None:
        raise CredentialsUnavailableError(
            f"Camera credentials for reference '{validated_ref}' unavailable in runtime environment."
        )

    # Construct authenticated URI in memory only with URL-encoded userinfo
    parsed = urlsplit(rtsp_url)
    quoted_user = quote(username, safe="")
    quoted_pass = quote(password, safe="")
    netloc = f"{quoted_user}:{quoted_pass}@{parsed.netloc}"

    return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))
