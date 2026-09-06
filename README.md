# Presyn

Presyn is a local-first, CPU-optimized workplace presence, CCTV intelligence, face recognition, attendance, visitor management, security zone, and physical activity-state platform.

## Current Project Status

**Baseline Governance and Planning Stage (Phase 00)**

This repository currently contains the authoritative planning, architectural specifications, governance rules, and initial repository baseline. Application implementation has not yet begun. No features are claimed as implemented at this stage.

For the single authoritative project standard, consult [PRESYN_MASTER_PLAN.md](file:///c:/Users/mhyah/Downloads/New%20folder/01_PROJECTS/CCTV_Face_Recognition_Attendance/PRESYN_MASTER_PLAN.md).

## Core Principles

- **Local-First and Offline-Capable**: Core recognition, tracking, attendance, and analytics operate locally without mandatory external network or cloud connections.
- **CPU-First Architecture**: Built and optimized for standard enterprise-class CPU execution (such as Intel Core i7-1355U) without GPU or CUDA dependencies.
- **Truthful System State**: Complete prohibition of fabricated metrics, simulated dashboard values, fake customer accounts, or uncalibrated accuracy claims. Unpopulated views display clear empty states.
- **Biometric Minimization**: Feature vectors (512-dimensional embeddings) are computed for matching while raw facial captures are not permanently stored in production databases.
- **Auditability and Governance**: Every sensitive administrative action, manual attendance correction, and biometric profile adjustment is logged in an immutable audit trail.

## Technology Stack Summary

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

Development proceeds strictly in sequential phases according to [PRESYN_MASTER_PLAN.md](file:///c:/Users/mhyah/Downloads/New%20folder/01_PROJECTS/CCTV_Face_Recognition_Attendance/PRESYN_MASTER_PLAN.md):

- **Phase 00**: Authority, Governance, Repository Baseline, and Planning (Completed)
- **Phase 01**: Core Skeleton (FastAPI, React 18, Vite, Tailwind CSS, SQLite, Alembic, Health)
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

## Privacy, Security, and Biometric Governance

Presyn is designed with strict biometric data protection principles:

- Raw facial photography is discarded after feature vector extraction unless temporary snapshot retention is explicitly enabled by local policy.
- An employee deletion request immediately purges all associated embedding vectors and biometric profiles.
- System activity-state classifications (sitting, standing, walking) reflect physical space dynamics and must never be converted into automated employee productivity scores.
- Deployment in production environments requires independent local legal review for workplace biometric compliance.

## Development-State Disclaimer

Presyn is under active initial development. This repository establishes the authoritative baseline. Features described in the roadmap are planned and will be validated systematically in subsequent development phases.
