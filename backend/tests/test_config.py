"""Unit Tests for Presyn Application Settings."""

from backend.app.core.config import Settings


def test_settings_load_defaults():
    """Verify default configuration loads with sound values."""
    custom_settings = Settings()
    assert custom_settings.ENVIRONMENT in ["development", "testing", "production"]
    assert custom_settings.PORT == 8000
    assert custom_settings.HOST == "127.0.0.1"
    assert custom_settings.DATABASE_URL.startswith("sqlite:///")
    assert custom_settings.FACE_MAX_TEMPLATES_PER_EMPLOYEE == 50


def test_cors_origins_parsing():
    """Verify CORS origins string parses into clean list."""
    settings_obj = Settings(CORS_ORIGINS="http://localhost:3000, https://example.com ")
    origins = settings_obj.cors_origins_list
    assert len(origins) == 2
    assert "http://localhost:3000" in origins
    assert "https://example.com" in origins


def test_feature_flags_default_false():
    """Verify all optional modules default to disabled."""
    settings_obj = Settings()
    assert settings_obj.ENABLE_MASK_DETECTION is False
    assert settings_obj.ENABLE_LIVENESS_CHECK is False
    assert settings_obj.ENABLE_EXPRESSION_TRENDS is False
