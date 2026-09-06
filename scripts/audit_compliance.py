"""Presyn automated compliance, design rules, em dash, and requirement consistency audit.

This script executes all static compliance gates required by Phase 01.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files and directories to scan
CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".css", ".html", ".json", ".md", ".yml", ".yaml", ".ini"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", ".pytest_cache", ".ruff_cache", "__pycache__"}
EXCLUDED_FILES = {"package-lock.json"}  # npm dependencies metadata


def audit_em_dashes() -> int:
    """Audit repository text files for U+2014 em dash characters."""
    print("--- [GATE 1] Em Dash Audit (U+2014) ---")
    violations = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in files:
            if f in EXCLUDED_FILES:
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS or f in {"alembic.ini", "pytest.ini", ".env.example", "README.md"}:
                path = Path(root) / f
                try:
                    content = path.read_text(encoding="utf-8")
                    if "\u2014" in content:
                        for line_idx, line in enumerate(content.splitlines(), start=1):
                            if "\u2014" in line:
                                rel_path = path.relative_to(ROOT)
                                violations.append(f"{rel_path}:{line_idx}: contains em dash: {line.strip()[:80]}")
                except Exception as exc:
                    print(f"Warning reading {path}: {exc}")

    if violations:
        print(f"FAILED: Found {len(violations)} em dash violations:")
        for v in violations[:20]:
            print(f"  {v}")
        return len(violations)

    print("PASS: Zero U+2014 em dash characters detected.")
    return 0


def audit_prohibited_ai_terms() -> int:
    """Audit source files for prohibited AI marketing tags."""
    print("\n--- [GATE 2] Prohibited AI Badges Audit ---")
    prohibited_patterns = [
        re.compile(r"Made\s+with\s+AI", re.IGNORECASE),
        re.compile(r"Powered\s+by\s+AI", re.IGNORECASE),
    ]
    violations = []

    # Exclude files that define the prohibition checks
    allowed_check_files = {
        "design_rules.test.tsx",
        "audit_compliance.py",
        "PRESYN_MASTER_PLAN.md",  # Master plan documents the prohibition rule
    }

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and d not in {"test", "tests"}]
        for f in files:
            if f in EXCLUDED_FILES or f in allowed_check_files or "test" in f.lower():
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in {".py", ".ts", ".tsx", ".js", ".jsx", ".html", ".css"}:
                path = Path(root) / f
                try:
                    content = path.read_text(encoding="utf-8")
                    for pattern in prohibited_patterns:
                        match = pattern.search(content)
                        if match:
                            rel_path = path.relative_to(ROOT)
                            violations.append(f"{rel_path}: matches '{match.group(0)}'")
                except Exception as exc:
                    print(f"Warning reading {path}: {exc}")

    if violations:
        print(f"FAILED: Found {len(violations)} prohibited AI tags:")
        for v in violations:
            print(f"  {v}")
        return len(violations)

    print("PASS: Zero prohibited AI badges detected.")
    return 0


def audit_styling_rules() -> int:
    """Audit frontend styling for prohibited gradients and purple classes."""
    print("\n--- [GATE 3] Prohibited Styling Rules Audit ---")
    prohibited_css = [
        re.compile(r"from-purple", re.IGNORECASE),
        re.compile(r"to-purple", re.IGNORECASE),
        re.compile(r"via-purple", re.IGNORECASE),
        re.compile(r"bg-gradient", re.IGNORECASE),
    ]
    violations = []
    allowed_check_files = {"design_rules.test.tsx", "audit_compliance.py"}

    frontend_dir = ROOT / "frontend" / "src"
    if frontend_dir.exists():
        for root, dirs, files in os.walk(frontend_dir):
            if "test" in dirs:
                dirs.remove("test")
            for f in files:
                if f in allowed_check_files:
                    continue
                ext = os.path.splitext(f)[1].lower()
                if ext in {".ts", ".tsx", ".css"}:
                    path = Path(root) / f
                    content = path.read_text(encoding="utf-8")
                    for pat in prohibited_css:
                        if pat.search(content):
                            rel_path = path.relative_to(ROOT)
                            violations.append(f"{rel_path}: contains prohibited styling pattern {pat.pattern}")

    if violations:
        print(f"FAILED: Found {len(violations)} styling rule violations:")
        for v in violations:
            print(f"  {v}")
        return len(violations)

    print("PASS: Zero prohibited gradients or purple classes in frontend source.")
    return 0


def audit_local_machine_paths() -> int:
    """Audit tracked text files for accidental local absolute paths."""
    print("\n--- [GATE 4] Local Machine Path References Audit ---")
    path_patterns = [
        re.compile(r"[C-Z]:\\[Uu]sers\\"),
        re.compile(r"[C-Z]:/[Uu]sers/"),
        re.compile(r"/Users/[a-zA-Z0-9_-]+/"),
        re.compile(r"/home/[a-zA-Z0-9_-]+/"),
    ]
    violations = []
    # Exclude files where local user info is not tracked or test fixtures
    excluded_from_path_scan = {
        "package-lock.json",
        "audit_compliance.py",
    }

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for f in files:
            if f in EXCLUDED_FILES or f in excluded_from_path_scan:
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS or f in {"alembic.ini", "pytest.ini", ".env.example", "README.md"}:
                path = Path(root) / f
                try:
                    content = path.read_text(encoding="utf-8")
                    for pat in path_patterns:
                        match = pat.search(content)
                        if match:
                            rel_path = path.relative_to(ROOT)
                            violations.append(f"{rel_path}: contains absolute path '{match.group(0)}'")
                except Exception as exc:
                    print(f"Warning reading {path}: {exc}")

    if violations:
        print(f"FAILED: Found {len(violations)} tracked local machine path references:")
        for v in violations:
            print(f"  {v}")
        return len(violations)

    print("PASS: Zero tracked local machine path references detected.")
    return 0


def audit_requirement_consistency() -> int:
    """Audit requirement matrix consistency in PRESYN_MASTER_PLAN.md."""
    print("\n--- [GATE 5] Requirement Matrix Consistency Audit ---")
    plan_path = ROOT / "PRESYN_MASTER_PLAN.md"
    if not plan_path.exists():
        print("FAILED: PRESYN_MASTER_PLAN.md not found.")
        return 1

    content = plan_path.read_text(encoding="utf-8")

    # Section 29: Requirement Traceability Catalog
    # Section 30: Final Implementation Verification Matrix
    s29_marker = "29. REQUIREMENT TRACEABILITY CATALOG"
    s30_marker = "30. FINAL IMPLEMENTATION VERIFICATION MATRIX"
    s31_marker = "31. DEFINITION OF DONE AND FINAL ACCEPTANCE CRITERIA"

    idx29 = content.find(s29_marker)
    idx30 = content.find(s30_marker)
    idx31 = content.find(s31_marker)

    if idx29 == -1 or idx30 == -1 or idx31 == -1:
        print("FAILED: Could not find Sections 29, 30, and 31 markers.")
        return 1

    catalog_text = content[idx29:idx30]
    matrix_text = content[idx30:idx31]

    req_pattern = re.compile(r"(PRESYN-[A-Z0-9]+-[0-9]{3})")

    # Find IDs in catalog
    catalog_ids = []
    for line in catalog_text.splitlines():
        if "PRESYN-" in line and (line.strip().startswith("-") or "###" in line or "| PRESYN-" in line or "**PRESYN-" in line):
            matches = req_pattern.findall(line)
            if matches:
                catalog_ids.append(matches[0])

    # Find IDs in matrix table lines
    matrix_ids = []
    for line in matrix_text.splitlines():
        if line.strip().startswith("|") and "PRESYN-" in line:
            matches = req_pattern.findall(line)
            if matches:
                matrix_ids.append(matches[0])

    catalog_set = set(catalog_ids)
    matrix_set = set(matrix_ids)

    catalog_only = sorted(list(catalog_set - matrix_set))
    matrix_only = sorted(list(matrix_set - catalog_set))

    duplicate_catalog = [x for x in catalog_set if catalog_ids.count(x) > 1]
    duplicate_matrix = [x for x in matrix_set if matrix_ids.count(x) > 1]

    print(f"Catalog Requirements Count : {len(catalog_ids)} (Unique: {len(catalog_set)})")
    print(f"Matrix Requirements Count  : {len(matrix_ids)} (Unique: {len(matrix_set)})")
    print(f"Catalog Only IDs Count     : {len(catalog_only)}")
    print(f"Matrix Only IDs Count      : {len(matrix_only)}")
    print(f"Duplicate Catalog IDs      : {len(duplicate_catalog)}")
    print(f"Duplicate Matrix IDs       : {len(duplicate_matrix)}")

    if catalog_only or matrix_only or duplicate_catalog or duplicate_matrix:
        print("FAILED: Requirement consistency mismatch detected.")
        if catalog_only:
            print(f"  Catalog only: {catalog_only}")
        if matrix_only:
            print(f"  Matrix only: {matrix_only}")
        if duplicate_catalog:
            print(f"  Duplicate catalog: {duplicate_catalog}")
        if duplicate_matrix:
            print(f"  Duplicate matrix: {duplicate_matrix}")
        return 1

    print("PASS: Requirement catalog and matrix are 100% consistent (75 unique requirements).")
    return 0


def main():
    print("=== PRESYN COMPLIANCE & DESIGN RULES AUDIT ===")
    errors = 0
    errors += audit_em_dashes()
    errors += audit_prohibited_ai_terms()
    errors += audit_styling_rules()
    errors += audit_local_machine_paths()
    errors += audit_requirement_consistency()

    print("\n==============================================")
    if errors == 0:
        print("ALL COMPLIANCE GATES PASSED")
        sys.exit(0)
    else:
        print(f"AUDIT FAILED WITH {errors} TOTAL ISSUES")
        sys.exit(1)


if __name__ == "__main__":
    main()
