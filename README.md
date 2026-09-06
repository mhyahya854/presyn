# Presyn

Presyn is a planned local-first, CPU-optimized workplace presence, CCTV intelligence, face recognition, attendance, visitor management, security zone, and physical activity-state platform.

## Current Project Status

**Phase 01 Implemented: Core Application Skeleton & Database Foundation**

Phase 01 is implemented and verified. The repository contains the operational FastAPI backend skeleton, 23 V1 relational domain models, Alembic migration infrastructure, truthful health and system telemetry endpoints, React 18 / TypeScript / Vite frontend shell with the six planned operational hubs, custom geometric SVG favicon, dedicated Privacy Policy and Terms & Conditions pages, deterministic test suites (pytest and vitest), automated compliance audit scripts, and GitHub Actions CI.

Camera ingestion, face detection, and biometric pipelines remain deliberately unconstructed and will activate beginning in Phase 02.

For the single authoritative project standard, consult [PRESYN_MASTER_PLAN.md](PRESYN_MASTER_PLAN.md).

## Core Principles

- **Local-First and Offline-Capable**: The planned platform is designed to operate locally without mandatory external network or cloud connections for core recognition and attendance.
- **CPU-First Architecture**: Presyn will be built and optimized for standard enterprise-class CPU execution (such as Intel Core i7-1355U) without GPU or CUDA dependencies.
- **Truthful System State**: Complete prohibition of fabricated metrics, simulated dashboard values, fake customer accounts, or uncalibrated accuracy claims. Unpopulated views will display clear empty states.
- **Biometric Minimization**: Feature vectors (512-dimensional embeddings) will be computed for matching while raw facial captures are not permanently stored in production databases.
- **Auditability and Governance**: Every sensitive administrative action, manual attendance correction, and biometric profile adjustment will be logged in an immutable audit trail.

## Public Development Lifecycle and Security Boundary

Presyn will remain public throughout development (Phases 00 through 19 and Phase 20 development). The repository will transition to private as the final lifecycle action only after Phase 20 is complete, all required Master Plan acceptance gates pass, and final release verification is signed off.

Public repository development does NOT permit sensitive runtime or biometric data to enter Git. The project enforces strict boundary protection:

- NEVER commit real biometric data or face-template dumps
- NEVER commit real employee photographs or CCTV footage
- NEVER commit camera snapshots or enrollment image matrices
- NEVER commit production database files (*.db, *.sqlite, *.sqlite3)
- NEVER commit credentials, private keys, API tokens, or secrets
- NEVER commit private deployment configurations or sensitive workplace records

## Planned Technology Stack Summary

- **Backend Runtime**: Python 3.10.x
- **API Framework**: FastAPI with Uvicorn ASGI server
- **Data Validation & Settings**: Pydantic v2 and pydantic-settings
- **Database & Migrations**: SQLite (V1) with SQLAlchemy 2.0 and Alembic
- **Computer Vision & Inference**: OpenCV, ONNX Runtime CPU, SCRFD-style face detection, ArcFace-style feature embeddings
- **Vector Matching**: Exact normalized NumPy cosine similarity matrix multiplication
- **Spatial Tracking**: ByteTrack multi-object tracking
- **Frontend Framework**: React 18, TypeScript, and Vite
- **Styling**: Tailwind CSS adhering to strict rectangular and lightly rounded control geometry
- **Iconography**: Lucide React SVG icons (no emojis as interface icons)
- **Real-Time Communication**: Native browser WebSocket and FastAPI WebSocket routes

## Repository Structure

```
.
|-- PRESYN_MASTER_PLAN.md   # Single canonical implementation authority
|-- README.md               # Repository summary and governance overview
|-- .gitignore              # Biometric, secret, and runtime boundary protection
|-- .env.example            # Environment configuration template
|-- backend/                # FastAPI backend, CV pipelines, and domain engines
|-- frontend/               # React 18 / Vite / Tailwind console interface
|-- models/                 # ONNX model directory (local weights excluded from Git)
|-- data/                   # Local database and transient runtime storage
|-- docs/                   # Supplementary architectural diagrams and notes
`-- scripts/                # Development, calibration, and benchmark utilities
```

## Implementation Phases and Acceptance Gates

Development will proceed strictly in sequential phases according to [PRESYN_MASTER_PLAN.md](PRESYN_MASTER_PLAN.md):

- **Phase 00**: Authority, Governance, Repository Baseline, and Planning (Completed)
- **Phase 01**: Core Skeleton (FastAPI, React 18, Vite, Tailwind CSS, SQLite, Alembic, Health) (Completed)
- **Phase 02**: Camera Ingestion Engine (Webcam, RTSP, Decoupled Queues, Reconnect, WS Video)
- **Phase 03**: Face Detection & Quality Gating (SCRFD ONNX CPU, Landmarks, Blur/Size Filters)
- **Phase 04**: Employee Domain Model & Five-View Interactive Enrollment Wizard
- **Phase 05**: ArcFace Embedding Pipeline & Exact Normalized NumPy Vector Search
- **Phase 06**: Multi-Frame Temporal Identity Verifier & Calibration Engine
- **Phase 07**: Attendance Engine, Shifts, Deduplicated Arrivals, & Audit Corrections
- **Phase 08**: Visitor Mode Architecture & Unknown-Person Escalation Workflows
- **Phase 09**: Conservative Safe Incremental Face-Template Learning Engine
- **Phase 10**: Person Detection (ONNX CPU) & ByteTrack Multi-Object Spatial Tracking
- **Phase 11**: Polygon Zone Architecture & Continuous Presence Session Management
- **Phase 12**: Pose & Motion Estimation for Physical Activity Tracking
- **Phase 13**: Centralized Manual Verification Queue & Security Workflows
- **Phase 14**: Mask-Aware Recognition Adaptation & Policy Hardening
- **Phase 15**: Optional Liveness & Presentation Attack Detection Adapter
- **Phase 16**: Reporting Engine, CSV Exports, Operational Analytics, & Diagnostics
- **Phase 17**: Optional Aggregate Facial Expression Trend Analysis Adapter
- **Phase 18**: Performance Profiling, Scale Benchmarking (100+ Employees / 5,000 Vectors)
- **Phase 19**: Security, Privacy Hardening, Cryptographic Audit Trail, & Policy Purging
- **Phase 20**: Comprehensive Acceptance Verification, Soak Testing, & Master Plan Sign-Off

No phase is accepted without passing automated unit, integration, build, and security quality gates.

## Development Commands

### Backend

```bash
# Setup Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
pip check

# Run database migrations
alembic -c backend/alembic.ini upgrade head

# Run backend tests
pytest

# Launch backend server
python backend/run.py
```

### Frontend

```bash
# Install frontend dependencies
cd frontend
npm install

# Run frontend tests
npm test

# Launch local development server
npm run dev

# Build production bundle
npm run build
```

### Compliance & Governance Audit

```bash
python scripts/audit_compliance.py
```

## Privacy, Security, and Biometric Governance

Presyn is designed with strict biometric data protection principles:

- Raw facial photography will be discarded after feature vector extraction unless temporary snapshot retention is explicitly enabled by local policy.
- An employee deletion request will immediately purge all associated embedding vectors and biometric profiles.
- System activity-state classifications (sitting, standing, walking) reflect physical space dynamics and must never be converted into automated employee productivity scores.
- Deployment in production environments requires independent local legal review for workplace biometric compliance.

## Development-State Disclaimer

Presyn is under active initial development. This repository establishes the authoritative baseline. Features described in the roadmap are planned and will be validated systematically in subsequent development phases.
