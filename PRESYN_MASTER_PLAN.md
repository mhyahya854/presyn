# PRESYN: CANONICAL MASTER PLAN AND GOVERNANCE SPECIFICATION

```
Document Identifier : PRESYN_MASTER_PLAN.md
Classification      : Canonical Architecture and Implementation Authority
Project Status      : Baseline Established (Phase 00 Complete)
Target Environment  : CPU-First Workplace Deployment (Windows / Linux)
Specification Model : Single Authoritative Source of Truth
```

---

## 1. ABSOLUTE PROJECT AUTHORITY RULE

This document (`PRESYN_MASTER_PLAN.md`) is the single canonical specification, design authority, and acceptance standard for the Presyn platform. 

1. **Sole Authority**: No competing specifications, architecture notes, design mockups, or secondary planning documents may supersede, contradict, or invalidate the requirements contained herein.
2. **Implementation Verification**: At the conclusion of development, another engineer, auditor, or autonomous agent will inspect the codebase against this document to verify requirement fulfillment. Every requirement must be classified into one of four states:
   - `IMPLEMENTED`: Verified with concrete code and automated/manual test evidence.
   - `PARTIALLY IMPLEMENTED`: Incomplete or missing secondary validation.
   - `NOT IMPLEMENTED`: Planned capability not yet constructed.
   - `NOT APPLICABLE`: Formal scope exclusion explicitly documented with rationale in the Change Log.
3. **Traceability**: Every functional, architectural, interface, security, and governance requirement carries a permanent, immutable Traceability ID (`PRESYN-*`).
4. **Subordinate Documents**: `README.md` and supplementary documentation may summarize or reference this document, but they must never act as competing specifications.

### 1.1 Repository Visibility Lifecycle Policy
1. **Public Development Lifecycle**: The Presyn repository (`mhyahya854/presyn`) must remain PUBLIC throughout development across Phases 00 through 19 and throughout active Phase 20 development.
2. **Post-Completion Privatization**: The repository transitions from PUBLIC to PRIVATE as the final operational release action only after the entire project is 100% complete, Phase 20 has verified that every REQUIRED Master Plan requirement is IMPLEMENTED with concrete evidence, and all final release security and audit gates pass.
3. **Prohibition of Intermediate Privatization**: No intermediate prompt, subagent, or developer action may change repository visibility to private during development. No future prompt may alter repository visibility unless permitted by this lifecycle rule or explicitly overridden by the project owner.
4. **Permanent Security Boundary**: Public repository visibility does NOT permit sensitive runtime, biometric, or organizational data into Git. The security boundary strictly mandates:
   - NEVER commit real biometric feature embeddings or raw template dumps
   - NEVER commit real employee photographs, enrollment captures, or CCTV footage
   - NEVER commit camera snapshots or uncurated facial crops
   - NEVER commit database binaries (*.db, *.sqlite, *.sqlite3)
   - NEVER commit credentials, secret keys, API tokens, or production configurations
   - NEVER commit private workplace records or sensitive operational logs

---

## 2. IMMUTABLE DESIGN RULES

The following rules represent permanent, non-negotiable acceptance gates for all Presyn frontend, backend, documentation, and user-facing artifacts. Any pull request, commit, or implementation phase violating any rule below fails acceptance immediately.

### 2.1 Prohibited Visual and Interface Patterns
The Presyn interface must **NEVER** use:
- Purple gradients or gradient-heavy SaaS visuals
- Pill-shaped buttons or pill-shaped navigation for ordinary controls (rectangular or lightly rounded corners with standard radius only; compact status tags are the only permitted exception)
- Unnecessary glassmorphism, background blurs, or heavy frosted glass effects
- Excessive glowing borders, neon drop shadows, or pulsating card outlines
- Excessive floating cards with artificial depth layers
- Gratuitous animated backgrounds, canvas particle fields, or reactive grids
- Cursor-following animations, custom animated pointers, or trailing graphics
- Excessive scrolling animations, over-the-top scroll effects, scroll-jacking, or parallax gimmicks
- Emoji used as interface icons, status indicators, or navigational symbols (use `lucide-react` SVG icons exclusively)
- Decorative AI sparkle iconography (e.g., star clusters, magic wands)
- "Made with AI" badges, banners, or footer tags
- Generic "Powered by AI" badges unless technically, functionally, and contextually necessary

### 2.2 Prohibited Copy and Text Patterns
Marketing, documentation, and product copy must **NEVER** use:
- M-dashes or em dashes in marketing or product copy (use standard hyphens, colons, or parentheses)
- AI-slop marketing copy, buzzword hyperbole, or hyperbolic corporate jargon
- Generic exaggerated AI claims (e.g., "revolutionary cognitive insight", "omniscient awareness")
- Claims of "100% accuracy", "bulletproof recognition", or "guaranteed identification"
- Emotional or mental-state inference claims (e.g., "detects employee happiness", "measures team morale")

### 2.3 Strict Anti-Fabrication Policy
To preserve enterprise credibility, operational trustworthiness, and audit integrity, Presyn strictly prohibits fabricated, synthetic, or invented data presented as real:
- **NO Fake Reviews or Testimonials**: Never display invented customer quotes, case studies, or user reviews.
- **NO Fake Logos or Accounts**: Never display fabricated partner logos, customer badges, or fictitious client enterprises.
- **NO Fake Dashboards or Metrics**: Never populate dashboards with mock operational figures, imaginary employee counts, fictitious alert numbers, or invented uptime percentages to make the interface look active.
- **NO Fake Recognition Statistics**: Never display uncalibrated or unmeasured recognition accuracy percentages as though they represent measured field telemetry.
- **NO Fake Activity Data**: Never generate synthetic presence histories or activity state streams pretending to represent live workplace behavior.

### 2.4 Truthful Empty States
When real runtime or telemetry data does not yet exist, Presyn interfaces must display clean, truthful, and unambiguous empty states, including:
- `"No data yet"`
- `"Waiting for camera feed"`
- `"No employees enrolled"`
- `"No attendance records for selected date"`
- `"System not calibrated"`
- `"Camera offline or unreachable"`

---

## 3. MANDATORY BRAND AND WEBSITE RULES

1. **Custom Branding and Favicon**: Presyn must provide a dedicated, custom SVG/PNG favicon and a distinct, refined corporate identity.
2. **Legal and Governance Pages**: The application must incorporate a dedicated Privacy Policy page and a Terms & Conditions page, accessible via persistent, standardized footer links across all views.
3. **Imagery and Photography Policy**: If photographic assets are ever required in documentation or interface contexts, use only:
   - Authentic project or facility photography provided by the system owner
   - Properly licensed, neutral real photography
   - Clean product interface captures and technical schematics
   - Never generate AI-slop stock photography depicting fictitious employees, fake offices, or synthetic security staff.

---

## 4. VISUAL DIRECTION AND UX PRINCIPLES

Presyn must project the visual demeanor of a high-reliability, enterprise-grade physical intelligence system:

- **Tone and Temperament**: Modern, serious, refined, enterprise-ready, precise, calm, technical, trustworthy, and minimal. It must not feel sterile, generic SaaS, cyberpunk, dystopian surveillance, or playful.
- **Operational Ergonomics**: Prioritize clear visual hierarchy, typographic legibility, rapid scanning for security operators, situational awareness, and truthful system state reflection.
- **Control Form Factors**: Buttons and input fields must use conventional rectangular or slightly rounded rectangular geometry (e.g., `rounded-md`, 4px to 6px corner radii). Fully rounded pill styling is strictly restricted to compact status tags (e.g., `ONLINE`, `CONFIRMED`).
- **Typography**: Clean, neutral, high-legibility sans-serif typefaces (e.g., Inter or system sans-serif stack) with consistent tabular figures (`font-mono` or `tabular-nums`) for numeric counters, timestamps, coordinates, and latency metrics.

---

## 5. PRODUCT DEFINITION AND SCOPE

### 5.1 Platform Identity
Presyn is a local-first, CPU-optimized workplace presence, CCTV intelligence, face recognition, attendance, visitor management, security zone, and physical activity-state platform.

Presyn is not merely "a face attendance app". It is an extensible physical-space operational intelligence engine capable of continuous video stream analysis, real-time spatial awareness, multi-person tracking, and auditable event processing.

### 5.2 Core Capabilities (23 Functional Pillars)
1. **CCTV / Webcam Ingestion**: Resilient capture from RTSP feeds and USB webcams with automated backoff and reconnect logic.
2. **Real-Time Person Detection**: Continuous multi-person spatial bounding using lightweight CPU-capable models.
3. **Face Detection**: Accurate facial localization and landmark extraction using SCRFD-style architectures.
4. **Face Recognition**: Exact cosine similarity matching against enrolled biometric feature vectors.
5. **Employee Enrollment**: Five-view guided enrollment pipeline enforcing rigorous image quality gates.
6. **Attendance Automation**: Deduplicated arrival and departure processing with custom shift, grace period, and holiday logic.
7. **Continuous Person Tracking**: Persistent multi-object tracking across video frames with occlusion handling.
8. **Presence Sessions**: State-driven session lifecycles tracking physical presence and room transitions.
9. **Zone Tracking**: User-defined polygon zones supporting entry, exit, dwelling, and restricted area boundaries.
10. **Activity-State Estimation**: Conservative classification of physical states (sitting, standing, walking, unknown) derived from multi-frame pose and motion vectors.
11. **Duration Tracking**: Granular temporal accounting of time spent in zones and specific activity states.
12. **Visitor Mode**: Dynamic system toggle re-routing unrecognized people from security escalation into visitor management.
13. **Unknown-Person Alerts**: Configurable notifications for unclassified individuals detected in monitored spaces.
14. **Manual Verification Queue**: Human-in-the-loop review interface for ambiguous recognitions, edge-case matches, and corrections.
15. **Recognition Quality Controls**: Pre-embedding image quality filtration discarding blurry, dark, overexposed, or extreme-angle frames.
16. **Safe Incremental Learning**: Conservative, gated addition of novel biometric templates to prevent profile drift.
17. **Optional Mask Detection**: Auxiliary classification identifying masked subjects and elevating matching rigor.
18. **Optional Liveness / Anti-Spoofing**: Passive presentation attack detection mitigating printed photo and screen replays.
19. **Optional Facial Expression Trend Analysis**: Aggregated, team-level expression grouping without individual performance scoring.
20. **Reporting and Exports**: Comprehensive CSV reporting for attendance, presence sessions, zone audits, and system health.
21. **System Health and Diagnostics**: Granular telemetry covering inference latency, FPS, memory, CPU, and model readiness.
22. **Administrative Controls**: Role-based access control (RBAC), configuration tuning, and fine-grained camera management.
23. **Privacy and Biometric Governance**: Explicit consent records, template purging, automated retention lifecycle, and audit logs.

### 5.3 Non-Goals and Explicit Exclusions
- **Not an NVR/Continuous Video Recorder**: Presyn does not store 24/7 continuous video archives. Video recording remains the responsibility of existing enterprise NVRs. Presyn stores structured metadata, timestamped events, and brief, policy-governed thumbnail snapshots.
- **Not an Employee Productivity Scorer**: Presyn physical activity states (sitting, standing, walking) reflect physical space metrics. They must never be converted into automated work performance metrics, productivity scores, or disciplinary algorithms.
- **Not an Internet Face Search Platform**: Presyn operates exclusively against an internal, locally enrolled employee roster. It does not scrape public web resources or search external identity databases.
- **Not a Cloud-Dependent SaaS**: Presyn core recognition, tracking, attendance, and analytics operate 100% locally and offline without external network dependencies.
- **Not a GPU/CUDA-Reliant Platform**: The primary architecture is strictly optimized for modern CPU execution, eliminating specialized hardware dependencies.

---

## 6. CORE OPERATING CONSTRAINTS AND TARGET HARDWARE

- **Operating Systems**: Windows 11 / Windows 10 (development and primary enterprise deployment) and Linux (Ubuntu 22.04 LTS secondary deployment).
- **Target Processor Class**: Typical modern office-grade CPU such as Intel Core i7-1355U (10 cores, 12 threads) or equivalent AMD Ryzen 7 mobile/desktop processors.
- **Hardware Acceleration**: CPU-only execution using ONNX Runtime CPU Execution Provider (`CPUExecutionProvider`). Zero CUDA or dedicated GPU requirements.
- **Capacity Envelope**:
  - 100+ enrolled employees
  - Up to 50 curated face templates per employee
  - Approximately 5,000 active biometric embedding vectors loaded in memory
  - Simultaneous processing of 2 to 4 camera streams at throttled inference frame rates
- **Operational Range**: Intended recognition distance of 4 to 6 feet (1.2 to 1.8 meters) using standard 1080p CCTV/webcam focal lengths.
- **Accuracy Expectation**: 90% to 95% identification accuracy under controlled office lighting, frontal/semi-frontal pose, and calibrated thresholds. Accuracy is never claimed as guaranteed. The system strictly prefers false rejection (routing to manual review) over false identity acceptance.

---

## 7. SYSTEM ARCHITECTURE AND TECHNOLOGY STACK

```
+-------------------------------------------------------------------------+
|                              PRESYN PLATFORM                            |
+-------------------------------------------------------------------------+
|                                                                         |
|  +---------------------+   RTSP / MJPEG   +--------------------------+  |
|  |   CCTV / IP CAM     | ---------------->|  CAMERA INGESTION CORE   |  |
|  |   USB WEBCAMS       |   OpenCV Video   |  Frame Throttling & Queue|  |
|  +---------------------+                  +--------------------------+  |
|                                                         |               |
|                                                         v               |
|                                           +--------------------------+  |
|                                           |  CV & TRACKING PIPELINE  |  |
|                                           |  - Person Det (ONNX CPU) |  |
|                                           |  - ByteTrack Multi-Object|  |
|                                           |  - SCRFD Face Detection  |  |
|                                           |  - Quality Filtering     |  |
|                                           |  - ArcFace Embeddings    |  |
|                                           |  - Normalized NumPy Cos  |  |
|                                           |  - Multi-Frame Verifier  |  |
|                                           |  - Pose / Motion Estim.  |  |
|                                           +--------------------------+  |
|                                                         |               |
|                                                         v               |
|  +---------------------+   JSON Event     +--------------------------+  |
|  |   FASTAPI BACKEND   | <--------------- |  EVENT & STATE ENGINE    |  |
|  |   SQLAlchemy Core   |   Broadcast      |  - Presence Sessions     |  |
|  |   Alembic Migrations|                  |  - Zone Boundary Logic   |  |
|  |   REST API v1       |                  |  - Attendance Engine     |  |
|  |   Native WebSocket  |                  |  - Visitor / Unknown     |  |
|  +---------------------+                  +--------------------------+  |
|            |                                            |               |
|            v                                            v               |
|  +---------------------+                      +----------------------+  |
|  |   SQLITE STORAGE    |                      |   OPTIONAL MODULES   |  |
|  |   presyn.db         |                      |   - Mask Detector    |  |
|  |   Events, Templates |                      |   - Liveness Probe   |  |
|  |   Attendance, Logs  |                      |   - Expression Trend |  |
|  +---------------------+                      +----------------------+  |
|            |                                                            |
|            v HTTP REST / Native WebSocket                               |
|  +-------------------------------------------------------------------+  |
|  |                       REACT 18 + VITE FRONTEND                    |  |
|  |  TypeScript | Tailwind CSS | Lucide Icons | Custom SVG Charts    |  |
|  |  Live Grid  | Attendance  | People Roster | Security & Audit     |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

### 7.1 Backend Stack
- **Runtime**: Python 3.10.x
- **API Framework**: FastAPI with Uvicorn ASGI server
- **Validation and Settings**: Pydantic v2 and `pydantic-settings`
- **Database & ORM**: SQLite for V1 with SQLAlchemy 2.0 and Alembic schema migrations
- **System Telemetry**: `psutil` (monitoring CPU, RAM, disk I/O, process status)
- **Asynchronous Testing**: `pytest`, `pytest-asyncio`, and `httpx`

### 7.2 Computer Vision and Machine Learning Stack
- **Image Processing**: OpenCV (`opencv-python-headless`), Pillow, and NumPy
- **Inference Runtime**: ONNX Runtime CPU (`onnxruntime` with default execution provider)
- **Face Detection**: SCRFD-style ONNX architecture producing bounding boxes and 5-point facial landmarks
- **Face Recognition**: ArcFace-style deep feature extractor outputting 512-dimensional normalized embeddings
- **Vector Search Engine**: Exact normalized NumPy cosine similarity matrix multiplication (`A @ B.T`). FAISS is explicitly omitted from V1 dependencies as 5,000 vectors execute in sub-10ms on modern CPUs. Approximate nearest neighbor indices (e.g., HNSWlib) will only be evaluated if empirical scale benchmarks demonstrate necessity.

### 7.3 Frontend Stack
- **Framework & Language**: React 18 with TypeScript
- **Tooling**: Vite for fast local building and Hot Module Replacement (HMR)
- **Styling**: Tailwind CSS with strict utility tokens adhering to the Immutable Design Rules
- **Iconography**: `lucide-react` SVG icons
- **Navigation**: `react-router-dom` v6
- **Data Synchronization**: Native browser WebSocket for live feeds and `@tanstack/react-query` for cached REST data
- **Visualizations**: Lightweight, project-owned SVG chart components (no heavy charting dependencies)

---

## 8. OPTIONAL MODEL ARCHITECTURE AND ISOLATION POLICY

Optional capabilities must never compromise the resilience, startup speed, or baseline attendance operations of Presyn:

### 8.1 Optional Modules
1. **Mask Detection** (`backend/features/mask_detector.py`)
2. **Liveness / Anti-Spoofing** (`backend/features/liveness_detector.py`)
3. **Facial Expression Trend Analysis** (`backend/features/expression_analyzer.py`)

### 8.2 Architectural Isolation Rules
- **Lazy Loading**: Optional models are loaded into memory only upon first explicit invocation after startup, never blocking core application initialization.
- **Feature Flags**: Controlled by environment variables defaulting to `false`:
  ```bash
  ENABLE_MASK_DETECTION=false
  ENABLE_LIVENESS_CHECK=false
  ENABLE_EXPRESSION_TRENDS=false
  ```
- **Fail-Safe Exception Handling**: All optional module adapters must wrap imports, model loading, and inference calls in granular `try...except` blocks.
- **Non-Fatal Degradation**: Missing model files, corrupted weights, or runtime exceptions must emit a structured log warning and return an `UNAVAILABLE` status code. Under no circumstances may an optional model crash camera ingestion, face recognition, or attendance creation.

---

## 9. CAMERA AND INGESTION ARCHITECTURE

### 9.1 Supported Sources and Domain Model
- Direct USB/V4L2/DirectShow webcams (`source_type = WEBCAM`, `device_index = 0, 1, 2...`, `rtsp_url = NULL`)
- Network IP cameras streaming via credential-free RTSP (`source_type = RTSP`, `device_index = NULL`, `rtsp_url = rtsp://camera.local/stream`, `credential_ref = optional opaque identifier`)
- Synthetic test video files / MJPEG streams for repeatable automated testing

### 9.2 Camera Secret Boundary Architecture
- **Permanent Secret Rule**: Camera authentication secrets (usernames, passwords, tokens) are NEVER stored directly in the camera database table, NEVER committed to Git, and NEVER returned through general health or system telemetry endpoints.
- **Credential Reference**: The database stores only non-secret stream addresses (`rtsp_url`) and an optional opaque reference key (`credential_ref`, e.g., `MAIN_ENTRANCE_CAMERA`).
- **Runtime-Only Secret Resolution**: In Phase 02, actual stream credentials will be resolved at runtime from local deployment configuration or secure environment variables, not from Git and not from general client responses.
- **Model-Level Safeguards**: Inline URI userinfo credentials (prohibiting usernames or passwords embedded before the host authority) are rejected by model validation without echoing the credential or logging the secret-bearing URL. Query parameters must likewise never contain sensitive tokens.

### 9.3 Ingestion Engine Capabilities
- **Decoupled Capture and Inference**: Separate background capture threads read camera frames continuously to avoid buffer latency, while inference workers consume frames at a controlled, throttled rate (e.g., 5 FPS).
- **Automated Reconnect Logic**: Network connection drops trigger exponential backoff reconnection loops (initial 2s, doubling up to 30s) without blocking sibling cameras.
- **Telemetry Tracking**:
  - Camera online/offline status (using controlled `CameraStatus` enums)
  - Capture FPS vs. Processed Inference FPS
  - Inter-frame latency and total processing pipeline duration
  - Timestamp of last successfully decoded frame
  - Error and dropped frame counters
- **Configuration Persistence**: Camera definitions (name, location, source_type, device_index, rtsp_url, credential_ref, is_active, target_fps, reconnect_delay, status) are persisted in the database and manageable via REST API without secret leakage.

---

## 10. PERSON DETECTION AND MULTI-OBJECT TRACKING

Presyn enforces a strict architectural separation between **Person Tracking** (spatial persistence) and **Face Recognition** (identity resolution):

```
[SCHEMA EXAMPLE - SYNTHETIC VALUES (EXAMPLE ONLY - NOT PRODUCTION DATA)]
Video Frame
   |
   v
[ Person Detector (ONNX) ] ---------> Bounding Boxes [x1, y1, x2, y2]
   |
   v
[ Multi-Object Tracker (ByteTrack) ] -> Persistent Track ID (e.g., Track #14)
   |
   +---> Spatial Zone Evaluation (Entry, Hallway, Desk)
   |
   +---> Pose & Motion Estimation (Sitting, Standing, Walking)
   |
   +---> Face Detector (SCRFD)
            |
            v
         Face Quality Gate (Size, Blur, Angle)
            |
            v
         ArcFace Embedding (512D)
            |
            v
         Top-K Cosine Search -> Identity Association (Associate Track #14 with Employee #102)
```

### 10.1 Tracking Engine Specifications
- **Algorithm**: ByteTrack multi-object tracking implementation utilizing Kalman filters and Hungarian association.
- **Track Continuity**: Maintains track persistence across temporary occlusions (configurable `track_lost_timeout` defaulting to 3.0 seconds).
- **Multi-Person Capacity**: Tracks multiple concurrent subjects simultaneously across the frame.
- **Identity Fusion**: When a high-confidence face identity is verified within a person bounding box, the track inherits the employee identity, eliminating the need to execute face recognition on every single frame.

---

## 11. FACE QUALITY GATING AND ENROLLMENT PIPELINE

### 11.1 Face Quality Pre-Filters
Faces detected in video frames must pass strict quality gates prior to embedding computation:
1. **Minimum Resolution**: Minimum face bounding box size of 48x48 pixels (recommended 64x64+ for enrollment).
2. **Blur Detection**: Laplacian variance metric (`variance_of_laplacian >= 60.0`). Blurry crops are discarded.
3. **Illumination Range**: Mean pixel brightness must fall between 40.0 and 220.0 (discarding underexposed and overexposed frames).
4. **Pose Extremes**: Facial landmark geometry must verify frontal or near-frontal orientation (yaw <= 30 deg, pitch <= 25 deg, roll <= 20 deg).
5. **Boundary Integrity**: The face bounding box must lie entirely within the camera frame boundaries.

### 11.2 Five-View Employee Enrollment
Employee biometric onboarding requires a structured, multi-view capture session:
1. **View 1**: Frontal unmasked (neutral expression, direct gaze)
2. **View 2**: Left angle unmasked (~20 to 30 degrees yaw)
3. **View 3**: Right angle unmasked (~20 to 30 degrees yaw)
4. **View 4**: Frontal with workplace face covering (if mask detection enabled/applicable)
5. **View 5**: Angled with workplace face covering (if mask detection enabled/applicable)

The Enrollment UI must provide real-time interactive feedback guiding the user through each step, displaying explicit failure reasons (e.g., `"Face too small"`, `"Too blurry"`, `"Multiple faces detected"`) and preventing low-quality template storage.

### 11.3 Biometric Template Limits
- Maximum of 50 curated templates stored per employee.
- Each template records: `template_id`, `employee_id`, `vector_512d`, `view_type`, `quality_score`, `created_at`, `source_type` (`ENROLLMENT` vs. `INCREMENTAL`).

---

## 12. IDENTITY ASSOCIATION AND MULTI-FRAME VERIFICATION

Identity confirmation must **NEVER** rely on a blind "nearest face wins" single-frame match.

### 12.1 Recognition Decision Pipeline
1. **Feature Extraction**: 512-dimensional normalized vector extracted via ArcFace ONNX model.
2. **Top-K Exact Search**: Compute cosine similarity against all active employee templates via NumPy vector dot product.
3. **Top-1 Threshold Check**: Top match similarity score must meet or exceed `FACE_SIMILARITY_THRESHOLD` (default 0.65).
4. **Top-1 / Top-2 Margin Check**: The difference between the top candidate score and the second-best candidate from a different employee must meet or exceed `FACE_MARGIN_THRESHOLD` (default 0.10). Matches failing this check are classified as `AMBIGUOUS`.
5. **Multi-Frame Verification Window**:
   - A temporal evaluation window spanning 1.0 to 3.0 seconds (default 2.0s).
   - Requires a minimum number of valid agreeing frames (e.g., 5 matching frames out of 8 sampled).
   - Tracks vote distribution, median similarity, and consistency.
6. **Final Classification States**:
   - `CONFIRMED`: Identity passed threshold, margin, and multi-frame consistency.
   - `CANDIDATE`: Currently accumulating votes in the active verification window.
   - `UNKNOWN`: Subject detected but similarity falls below threshold across all employees.
   - `AMBIGUOUS`: Top match is too close to a secondary candidate; flagged for manual review.
   - `REJECTED`: Frame discarded due to quality failure or severe orientation.
   - `MANUAL_REVIEW`: Escalated to administrative queue for human verification.

### 12.2 Visual Verification Indicator
The live interface communicates verification progression through a dedicated state indicator:
- State 1: `VERIFYING` (subtle framing animation indicating evidence gathering, vote progress bar)
- State 2: `VERIFIED` (clean crisp confirmation tag displaying employee name and calibrated confidence)
- Prohibited: No Apple FaceID clone graphics, no playful bouncing emojis, no glowing cyberpunk shields.

---

## 13. SAFE INCREMENTAL LEARNING POLICY

Presyn supports conservative incremental biometric template enrichment to adapt to minor appearance variations over time without succumbing to profile drift:

- **Strict Gating Criteria**: A runtime template may be stored automatically only if:
  1. The identity is already `CONFIRMED` with exceptional confidence (similarity >= 0.82).
  2. The match margin over the second-place identity is >= 0.15.
  3. The face crop surpasses elevated quality standards (size >= 80px, blur >= 80.0).
  4. The multi-frame verification window passed with 100% unanimous agreement.
  5. The subject has fewer than the maximum 50 templates.
  6. The candidate embedding is meaningfully distinct from all existing templates (cosine distance >= 0.08 from existing templates, preventing redundant duplicates).
  7. The system is not operating in visitor or unknown mode.
- **Administrative Governance**: Administrators must be provided an interface to inspect, audit, and selectively purge incrementally learned templates.

---

## 14. MASK-AWARE AND LIVENESS POLICIES

### 14.1 Mask Policy
- When optional mask detection is active and classifies a face as masked:
  - System raises the matching threshold (`FACE_SIMILARITY_THRESHOLD` increased by 0.08).
  - Multi-frame agreement requirement is increased from 5 to 8 votes.
  - Automatic incremental template learning is strictly disabled.
- If the mask model is unavailable or disabled, the system assigns `mask_status = UNAVAILABLE` and proceeds conservatively using standard calibrated thresholds.

### 14.2 Liveness and Anti-Spoofing Policy
- Evaluates presentation attack indicators (printed photo, screen glare, moiré pattern, unnatural texture).
- Possible states: `PASSED`, `FAILED`, `SUSPICIOUS`, `UNAVAILABLE`, `DISABLED`.
- **Core Security Axiom**: `UNAVAILABLE` must **NEVER** be treated as `PASSED`.
- High-risk security zones or enrollment workflows trigger manual review if liveness returns `SUSPICIOUS` or `FAILED`.

---

## 15. ATTENDANCE LOGIC AND POLICY ENGINE

### 15.1 Core Attendance Rules
- **Daily Arrival Deduplication**: Only the first valid `CONFIRMED` identity event of the day per employee generates an official Daily Arrival record. Subsequent camera detections update presence tracking but never create duplicate arrival records.
- **Departure Processing**: Daily departure can be configured via explicit checkout zone detection, longest observed presence session, or end-of-shift boundary.
- **Camera Visibility Separation**: Camera presence is explicitly decoupled from employment productivity evaluation. Attendance records signify physical site arrival, not work output.

### 15.2 Shifts, Grace Periods, and Corrections
- **Shift Support**: Configurable standard, flexible, and overnight shift configurations.
- **Grace Periods**: Configurable late arrival buffers (e.g., 15 minutes post shift-start before tagging `LATE`).
- **Audit-Controlled Manual Corrections**:
  - Authorized administrators may correct, insert, or void attendance entries.
  - Every correction mandates: `record_id`, `admin_user_id`, `timestamp`, `original_value`, `corrected_value`, and an explicit mandatory `reason_text`.
  - Corrections are permanently recorded in the immutable audit log.

---

## 16. SPATIAL ZONES, CONTINUOUS PRESENCE, AND ACTIVITY-STATE ESTIMATION

### 16.1 Configurable Polygon Zones
- Administrators define arbitrary 2D polygon boundaries over camera feeds.
- **Zone Types**: `ENTRY`, `EXIT`, `WORK_AREA`, `DESK_AREA`, `RECEPTION`, `BREAK_AREA`, `HALLWAY`, `RESTRICTED_AREA`.
- **Spatial Events**: `entered_zone`, `exited_zone`, `present_in_zone`, `left_monitored_zone`.
- **Truthful Absence Rule**: When a person disappears from a camera view, the truthful system state is initially `temporarily_lost` or `not_visible_on_camera`. The system must never falsely claim the employee has "left the workplace" unless supported by an exit zone transit or confirmed timeout.

### 16.2 Continuous Presence Lifecycles
Presence sessions transition through distinct states:
1. `VISIBLE`: Actively detected and tracked on at least one monitored camera.
2. `TEMPORARILY_LOST`: Subject occluded or absent for < 15 seconds; session remains active.
3. `LEFT_MONITORED_ZONE`: Subject observed leaving camera boundary without immediate reappearance.
4. `RETURNED`: Subject re-identified within the session recovery window.
5. `SESSION_CLOSED`: Subject absent beyond timeout threshold; presence duration finalized.

### 16.3 Activity-State Tracking
- **Physical States**: `sitting`, `standing`, `walking`, `unknown`.
- **Multi-Frame Synthesis**: Estimates are derived from keypoint skeletal geometry (ONNX CPU pose model) combined with spatial displacement vectors across successive tracking frames.
- **Storage Minimization**: Activity is persisted as aggregated `activity_segments` (start time, end time, duration, confidence) rather than wasteful per-frame database records.

---

## 17. VISITOR MANAGEMENT AND UNKNOWN-PERSON WORKFLOWS

### 17.1 Visitor Mode Engine
- **Visitor Mode ON**: Unrecognized individuals are classified as `VISITOR`, initiating visitor presence tracking, temporary visitor ID assignment, and host employee association.
- **Visitor Mode OFF**: Unrecognized individuals trigger `UNKNOWN_PERSON` security alerts, initiating security queue logging and cooldown notifications.
- **Architectural Linkage**: The frontend Visitor Mode toggle directly dispatches an authenticated REST request updating the backend tracking state. It is never a cosmetic UI-only toggle.

### 17.2 Unknown Person Processing
- Unknown subjects are **NEVER** force-matched to the nearest employee database record.
- Every unknown encounter logs: `unknown_id`, `track_id`, `camera_id`, `zone_id`, `first_seen`, `last_seen`, and an optional policy-governed thumbnail crop.
- **Resolution Actions**: Authorized personnel can resolve unknown items into:
  1. `Classified as Visitor`
  2. `Enrolled as New Employee`
  3. `Associated with Known Employee (Correction)`
  4. `Dismissed / False Positive`
  5. `Escalated to Security Review`

---

## 18. DEDICATED MANUAL REVIEW QUEUE

A centralized verification queue handles all ambiguous or high-risk operational events:
- **Queue Sources**: Ambiguous recognition candidates (narrow margin), borderline masked matches, presentation attack / liveness warnings, unknown persons, and attendance correction appeals.
- **Operator Interface**: Displays camera origin, timestamp, top candidate identities with similarity scores, calculated margin, failure reason, and visual crops (if retention permits).
- **Auditability**: All manual decisions (`APPROVE`, `REJECT`, `RECLASSIFY`) are recorded with reviewer identity, timestamp, and justification notes.

---

## 19. OPTIONAL FACIAL EXPRESSION TREND ANALYSIS

To ensure ethical compliance, privacy integrity, and technical accuracy:
- **Exact Terminology**: Must be designated solely as **Facial Expression Trend Analysis**. It must **NEVER** be labeled "emotion detection", "sentiment analysis", "morale measurement", or "mental state detection".
- **Strict Analytical Scope**: Provides coarse visual expression classification (e.g., smiling, neutral, expressive) aggregated purely at the team/department level over broad time windows (e.g., weekly aggregates).
- **Absolute Behavioral Safeguards**:
  - Expression data must **NEVER** influence attendance, security clearance, physical access, or employee performance evaluation.
  - Never generate individual employee emotional timelines or productivity correlations.
  - Heavy throttling: inference restricted to 1 sample per 30 to 60 seconds per tracked subject on high-resolution crops (face >= 64px, confidence >= 0.40).

---

## 20. DATABASE DOMAIN MODEL (CONCEPTUAL SCHEMA)

The Presyn V1 database uses SQLite managed via SQLAlchemy 2.0 with Alembic migrations.

```
+-----------------------------------------------------------------------------------------------+
|                                      DATABASE SCHEMA MAP                                      |
+-----------------------------------------------------------------------------------------------+
|                                                                                               |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|  |    departments    |        |     employees     |------->|        face_templates         |  |
|  |-------------------|        |-------------------|   1:N  |-------------------------------|  |
|  | id (PK)           | 1    N | id (PK)           |        | id (PK)                       |  |
|  | name              |<-------| department_id (FK)|        | employee_id (FK)              |  |
|  | code              |        | employee_number   |        | vector_512d (BLOB)            |  |
|  +-------------------+        | first_name        |        | view_type                     |  |
|                               | last_name         |        | quality_score                 |  |
|                               | status            |        | source_type                   |  |
|                               +-------------------+        +-------------------------------+  |
|                                         |                                                     |
|                                         | 1:N                                                 |
|                                         v                                                     |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|  |attendance_records |<-------| attendance_correct|        |       presence_sessions       |  |
|  |-------------------| 1    N |-------------------|        |-------------------------------|  |
|  | id (PK)           |        | id (PK)           |        | id (PK)                       |  |
|  | employee_id (FK)  |        | record_id (FK)    |        | employee_id (FK, nullable)    |  |
|  | date              |        | admin_user_id (FK)|        | track_id                      |  |
|  | arrival_time      |        | original_value    |        | first_seen / last_seen        |  |
|  | departure_time    |        | corrected_value   |        | current_camera_id (FK)        |  |
|  | status            |        | reason            |        | status                        |  |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|                                                                          |                    |
|                                                                          v 1:N                |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|  |      cameras      |------->|       zones       |        |       activity_segments       |  |
|  |-------------------| 1    N |-------------------|        |-------------------------------|  |
|  | id (PK)           |        | id (PK)           |        | id (PK)                       |  |
|  | name              |        | camera_id (FK)    |        | session_id (FK)               |  |
|  | rtsp_url          |        | name              |        | activity_state                |  |
|  | location          |        | polygon_json      |        | started_at / ended_at         |  |
|  | status            |        | zone_type         |        | duration_seconds              |  |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|                                                                                               |
|  +-------------------+        +-------------------+        +-------------------------------+  |
|  |    users_admins   |        |    audit_logs     |        |      manual_review_items      |  |
|  |-------------------|        |-------------------|        |-------------------------------|  |
|  | id (PK)           |        | id (PK)           |        | id (PK)                       |  |
|  | username          |        | actor_id (FK)     |        | item_type                     |  |
|  | password_hash     |        | action            |        | camera_id (FK)                |  |
|  | role (ADMIN/VIEW) |        | target_type       |        | candidate_data_json           |  |
|  | is_active         |        | target_id         |        | resolution_status             |  |
|  +-------------------+        | timestamp         |        | reviewer_id (FK)              |  |
|                               +-------------------+        +-------------------------------+  |
+-----------------------------------------------------------------------------------------------+
```

### 20.1 Core Table Inventory (23 Conceptual Entities)
1. `employees`: Core workforce records (id, employee_number, name, department_id, status, created_at, updated_at).
2. `departments`: Organizational hierarchy units (id, name, code).
3. `face_templates`: Biometric embeddings (id, employee_id, vector_512d, quality_score, view_type, source_type, created_at).
4. `cameras`: Ingestion stream definitions (id, name, rtsp_url, location, is_active, target_fps, reconnect_delay).
5. `zones`: Geometric polygon boundaries (id, camera_id, name, polygon_json, zone_type, is_active).
6. `tracks`: Ephemeral spatial track history (id, camera_id, track_id, started_at, ended_at).
7. `identity_verifications`: Audit log of verification windows (id, track_id, employee_id, confidence, vote_count, status).
8. `presence_sessions`: Continuous spatial sessions (id, employee_id, track_id, first_seen, last_seen, camera_id, zone_id, status).
9. `activity_segments`: Temporal physical states (id, session_id, activity_state, started_at, ended_at, duration_seconds).
10. `attendance_records`: Official workplace arrival/departure entries (id, employee_id, date, arrival_time, departure_time, status).
11. `attendance_corrections`: Immutable audit log of manual adjustments (id, record_id, admin_user_id, original_value, corrected_value, reason, timestamp).
12. `unknown_people`: Clustered unclassified entities (id, track_id, first_seen, last_seen, resolution_status).
13. `unknown_events`: Instantaneous sightings of unknowns (id, unknown_id, camera_id, zone_id, timestamp, snapshot_path).
14. `visitors`: Registered temporary visitors (id, full_name, host_employee_id, badge_number, status).
15. `visitor_events`: Transit records of visitors (id, visitor_id, camera_id, zone_id, timestamp).
16. `manual_review_items`: Verification queue entries (id, item_type, camera_id, candidate_data_json, status, reviewer_id, resolved_at).
17. `expression_events`: Optional aggregate expression samples (id, department_id, timestamp, expression_label, confidence).
18. `system_events`: Telemetry event log (id, event_type, severity, component, message, timestamp).
19. `settings`: Key-value application runtime configuration (key, value, updated_at).
20. `users_admins`: Console authentication principals (id, username, password_hash, role, is_active).
21. `roles`: Role definitions and permission scopes (id, name, permissions_json).
22. `audit_logs`: Immutable security action log (id, actor_id, action, target_type, target_id, timestamp, details_json).
23. `model_versions`: Tracking active model files, hashes, and calibration states (id, module_name, model_file, sha256_hash, loaded_at).

---

## 21. REST API AND LIVE WEBSOCKET EVENT CONTRACT

### 21.1 Versioned REST API (`/api/v1`)
- `/api/v1/health`: System readiness, CPU, memory, database, and model statuses.
- `/api/v1/system`: Configuration tuning, feature flags, calibration parameters, and logs.
- `/api/v1/cameras`: Ingestion source management (CRUD, test connection, FPS configuration).
- `/api/v1/zones`: Polygon zone management per camera view.
- `/api/v1/employees`: Employee roster management, biometric profile status, and history.
- `/api/v1/enrollment`: Five-view enrollment capture session endpoints.
- `/api/v1/attendance`: Daily attendance queries, monthly rollups, and CSV exports.
- `/api/v1/attendance/corrections`: Admin manual attendance adjustments with mandatory reasons.
- `/api/v1/presence`: Live presence sessions, current room occupancy, and zone statistics.
- `/api/v1/activity`: Physical activity segment summaries and duration reporting.
- `/api/v1/visitors`: Visitor registration, check-in, check-out, and active visitor roster.
- `/api/v1/unknowns`: Unrecognized subject alerts and resolution actions.
- `/api/v1/review`: Manual verification queue ingestion and resolution actions.
- `/api/v1/reports`: Standardized attendance, presence, security, and health export generators.
- `/api/v1/settings`: Global policy adjustments (retention, thresholds, shift hours).

### 21.2 Stable Live Event Contract (WebSocket Schema)
All real-time events broadcast over `/api/v1/ws/live` conform to a standardized JSON schema. Frontend clients safely handle null or absent optional properties:

SCHEMA EXAMPLE - SYNTHETIC VALUES (EXAMPLE ONLY - NOT PRODUCTION DATA):
```json
{
  "event_id": "evt_9b1c7f4a-8d23-4c91-9876-1a2b3c4d5e6f",
  "event_type": "PRESENCE_UPDATE",
  "timestamp": "2026-09-06T21:45:00.123Z",
  "camera_id": "cam_entrance_01",
  "camera_name": "Main Office Entrance",
  "frame_id": 14082,
  "track_id": 42,
  "spatial": {
    "bounding_box": [320, 180, 540, 720],
    "zone_id": "zone_lobby_entry",
    "zone_name": "Lobby Entry Zone"
  },
  "face": {
    "detected": true,
    "quality_score": 84.5,
    "face_width_px": 92,
    "blur_score": 78.2,
    "brightness_score": 112.0
  },
  "identity": {
    "employee_id": "emp_10492",
    "employee_name": "Sarah Connor",
    "recognition_status": "CONFIRMED",
    "confidence": 0.884,
    "top1_score": 0.884,
    "top2_score": 0.612,
    "match_margin": 0.272
  },
  "verification": {
    "window_seconds": 2.0,
    "valid_frame_count": 8,
    "same_identity_votes": 7
  },
  "activity": {
    "state": "walking",
    "confidence": 0.91,
    "duration_seconds": 4.2
  },
  "optional_features": {
    "mask_status": "UNMASKED",
    "mask_confidence": 0.98,
    "liveness_status": "PASSED",
    "liveness_confidence": 0.89,
    "expression_label": null,
    "expression_confidence": null
  },
  "system_state": {
    "visitor_mode": false,
    "attendance_action_triggered": "ARRIVAL_RECORDED",
    "warning": null
  }
}
```

---

## 22. FRONTEND PRODUCT INFORMATION ARCHITECTURE

The Presyn user interface is partitioned into six core operational environments:

```
+-------------------------------------------------------------------------+
| PRESYN CONSOLE     [● SYSTEM ONLINE]   [VISITOR MODE: OFF]   Admin (v1) |
+-------------------------------------------------------------------------+
| [1. LIVE]  [2. ATTENDANCE]  [3. PEOPLE]  [4. SECURITY]  [5. ANALYTICS]  |
|            [6. SYSTEM]                                                  |
+-------------------------------------------------------------------------+
|                                                                         |
|  1. LIVE CONSOLE                                                        |
|     - Multi-Camera Tile Grid (Webcam / RTSP) with Live Bounding Boxes   |
|     - Truthful Status Tags: [VERIFYING...] [VERIFIED] [UNKNOWN]         |
|     - Spatial Zone Overlays (Configurable Canvas Polygons)              |
|     - Real-Time Subject Drawer (Track ID, Activity State, Duration)     |
|                                                                         |
|  2. ATTENDANCE CENTER                                                   |
|     - Daily Arrival & Departure Ledger with Shift Alignment Flags       |
|     - Monthly Rollup Grid & Filterable Exception Indicators             |
|     - Audit-Tracked Manual Correction Modal (Mandatory Reason Input)   |
|     - Formatted CSV Attendance Ledger Export Trigger                    |
|                                                                         |
|  3. PEOPLE & ENROLLMENT                                                 |
|     - Employee Roster with Department Filters & Enrollment Progress     |
|     - Five-View Interactive Biometric Enrollment Wizard                 |
|     - Biometric Profile Governance (Audit Logs, Safe Template Purge)    |
|                                                                         |
|  4. SECURITY & VISITOR HUB                                              |
|     - Operational Visitor Mode State Switch (Direct Backend Binding)    |
|     - Unknown Person Sighting Log & Resolution Dispatcher               |
|     - Manual Review Queue (Narrow-Margin & Spoof Warning Auditing)      |
|                                                                         |
|  5. ANALYTICS & OCCUPANCY                                               |
|     - Zone Dwell Time & Spatial Distribution SVG Visualizations         |
|     - Physical Activity Breakdown (Sitting / Standing / Walking)        |
|     - System Recognition Accuracy & Calibration Metric History          |
|                                                                         |
|  6. SYSTEM & HARDWARE HEALTH                                            |
|     - Subsystem Readiness Matrix (Database, CV Models, Camera Feeds)    |
|     - CPU, RAM, & Inference Latency Oscilloscopes (psutil Telemetry)    |
|     - Feature Flag Configuration & Calibration Parameter Adjuster       |
|     - Comprehensive Cryptographic Audit Trail Inspector                 |
+-------------------------------------------------------------------------+
```

---

## 23. CALIBRATION AND PERFORMANCE TARGETS

### 23.1 Calibration Protocol
Presyn prohibits arbitrary hard-coded accuracy claims. Deployment requires a structured calibration phase recording:
- Empirical similarity threshold tuning against site-specific lighting and camera hardware.
- Margin threshold validation against employee cohort similarity distributions.
- Laplacian blur cutoff calibration for environmental motion patterns.
- Active calibration version stored in `model_versions` table for audit repeatability.

### 23.2 Concrete Performance Targets
The following quantifiable benchmarks must be validated on modern office-grade CPU hardware (Intel Core i7-1355U equivalent):

```
+------------------------------------+-------------------------+--------------------+
| Metric                             | Planning Target         | Verification Method|
+------------------------------------+-------------------------+--------------------+
| Enrolled Employee Capacity         | 100+ employees          | Synthetic Roster   |
| Active Biometric Vector Volume     | Up to 5,000 embeddings  | Vector Matrix Bench|
| Inference Frame Rate               | >= 5 FPS per stream     | Internal Telemetry |
| Recognition Decision Window        | 1.0 to 3.0 seconds      | Multi-Frame Timer  |
| Vector Search Latency (5,000 vecs) | < 100 ms (target <15ms) | Benchmark Script   |
| Attendance SQLite Write Latency    | < 300 ms                | Transaction Timer  |
| Dashboard WebSocket Event Latency  | < 1,000 ms              | Round-Trip Timer   |
| Cold Backend Startup Duration      | < 30 seconds            | Uvicorn Launch Log |
| 1-Hour Soak Stability              | Zero Memory Leak        | psutil Soak Script |
| Camera Stream Reliability          | Auto-Recovery < 10s     | Network Pull Test  |
+------------------------------------+-------------------------+--------------------+
```

---

## 24. SECURITY, PRIVACY, AND DATA GOVERNANCE

### 24.1 Biometric Protection Principles
- **Template Storage Only**: Raw facial images are never permanently stored in production databases. Presyn computes 512-dimensional float32 feature vectors and securely discards raw image matrices unless short-term snapshot retention is explicitly enabled by administrative policy.
- **Biometric Erasure (`Right to be Forgotten`)**: Deleting an employee record completely expunges all associated embedding vectors from disk and memory indexes.
- **Zero Secrets in Source Control**: All passwords, tokens, session keys, and database files are strictly governed by `.gitignore`.

### 24.2 CCTV Snapshot and Video Storage Boundary
- Presyn **NEVER** acts as an unrestricted CCTV recorder.
- Continuous video footage is retained exclusively on third-party enterprise NVR infrastructure.
- Presyn stores structured tabular metadata, lifecycle events, and optional low-resolution thumbnail crops strictly restricted by retention policy (default 7 days).

### 24.3 Immutable Audit Logging
The system maintains an append-only audit trail logging all high-privilege operations:
- Employee creation, profile modification, and biometric deletion
- Biometric template enrollment and incremental learning purges
- Manual attendance record adjustments and reason documentation
- Unknown person reclassifications and manual identity approvals
- Camera, zone, feature flag, and calibration parameter changes

---

## 25. COMPREHENSIVE TESTING STRATEGY

Every implementation phase must satisfy explicit unit, integration, and regression tests.

### 25.1 Mandatory Test Scenarios
1. **Core Infrastructure**: FastAPI startup, SQLite connection pooling, Alembic migration execution, and schema integrity.
2. **Camera Resiliency**: DirectShow webcam capture, RTSP reconnect backoff under network interruption, corrupted frame recovery.
3. **Face Quality Filters**: Synthetic validation rejecting overexposed, underexposed, blurred (low Laplacian variance), tiny (<48px), and severe off-axis faces.
4. **Vector Mathematics**: Validating normalized NumPy cosine similarity against reference dot-product implementations; verifying top-1/top-2 margin calculations.
5. **Enrollment Verification**: Full five-view enrollment wizard test rejecting duplicate templates and poor alignment.
6. **Attendance Rules**: Strict single-arrival-per-day enforcement; overnight shift boundary calculations; manual correction audit verification.
7. **Spatial Tracking**: Multi-object ByteTrack stability under simulated crossing and temporary 3-second occlusion.
8. **Zone Geometry**: Ray-casting point-in-polygon algorithm verifying entry/exit event emission across complex concave polygons.
9. **Activity Classification**: Pose keypoint ratio evaluation distinguishing sitting vs. standing vs. walking across continuous synthetic frame sequences.
10. **Optional Feature Isolation**: System startup and core attendance execution with optional model weights missing, corrupted, or toggled off.
11. **Scale Benchmarks**: NumPy cosine similarity matrix benchmark querying 5,000 synthetic 512D vectors under 20ms on CPU.

---

## 26. IMPLEMENTATION ROADMAP (PHASES 00 TO 20)

```
PHASE 00: Authority, Governance, Repository Baseline, and Planning [CURRENT]
PHASE 01: Core Skeleton (FastAPI, React 18, Vite, Tailwind CSS, SQLite, Alembic, Health)
PHASE 02: Camera Ingestion Engine (Webcam, RTSP, Decoupled Queues, Reconnect, WS Video)
PHASE 03: Face Detection & Quality Gating (SCRFD ONNX CPU, Landmarks, Blur/Size Filters)
PHASE 04: Employee Domain Model & Five-View Interactive Enrollment Wizard
PHASE 05: ArcFace Embedding Pipeline & Exact Normalized NumPy Vector Search
PHASE 06: Multi-Frame Temporal Identity Verifier & Calibration Engine
PHASE 07: Attendance Engine, Shifts, Deduplicated Arrivals, & Audit Corrections
PHASE 08: Visitor Mode Architecture & Unknown-Person Escalation Workflows
PHASE 09: Conservative Safe Incremental Face-Template Learning Engine
PHASE 10: Person Detection (ONNX CPU) & ByteTrack Multi-Object Spatial Tracking
PHASE 11: Polygon Zone Architecture & Continuous Presence Session Management
PHASE 12: Pose & Motion Estimation for Physical Activity Tracking (Sitting/Standing/Walking)
PHASE 13: Centralized Manual Verification Queue & Security Workflows
PHASE 14: Mask-Aware Recognition Adaptation & Policy Hardening
PHASE 15: Optional Liveness & Presentation Attack Detection Adapter
PHASE 16: Reporting Engine, CSV Exports, Operational Analytics, & Diagnostics
PHASE 17: Optional Aggregate Facial Expression Trend Analysis Adapter
PHASE 18: Performance Profiling, Scale Benchmarking (100+ Employees / 5,000 Vectors)
PHASE 19: Security, Privacy Hardening, Cryptographic Audit Trail, & Policy Purging
PHASE 20: Comprehensive Acceptance Verification, Soak Testing, & Master Plan Sign-Off
```

---

## 27. PERMANENT GIT WORKFLOW FOR ALL FUTURE PROMPTS

Every future implementation phase and development prompt must execute and verify the following 10-step sequence prior to concluding:

1. **Inspect Working Tree**: Run `git status` to verify modified, created, and untracked files.
2. **Execute Quality Gates**: Run all relevant unit, integration, and build checks (`pytest`, `npm run build`).
3. **Update Requirement Evidence**: Update the Final Implementation Verification Matrix in `PRESYN_MASTER_PLAN.md`.
4. **Inspect Working Diffs**: Run `git diff` to verify code correctness and formatting.
5. **Security & Secret Audit**: Confirm no `.env` files, API keys, database binaries (`.db`), or biometric media files are staged.
6. **Selective Staging**: Execute `git add` exclusively on intended, validated code files.
7. **Conventional Commit**: Create a meaningful commit conforming to conventional commits specification.
8. **Remote Push**: Execute `git push origin main`.
9. **Push Verification**: Verify remote update succeeded via `git status -uno` and `git rev-parse HEAD`.
10. **Report Commit SHA**: Report the exact commit hash and verification state in the final response.

---

## 28. MASTER PLAN CHANGE CONTROL LOG

All modifications to this document must be appended to this immutable change log to maintain historical provenance.

```
+------------+-----------------------+------------------------------------------+---------------------+----------+---------+
| Date       | Affected Req IDs      | Description of Modification              | Rationale           | Decision | Commit  |
+------------+-----------------------+------------------------------------------+---------------------+----------+---------+
| 2026-09-06 | ALL (Baseline Init)   | Initial creation of Canonical Master Plan| Prompt 1 Authority  | APPROVED | e48f478 |
| 2026-09-06 | PRESYN-GEN-005,       | Prompt 1B Governance Correction: lock    | Explicit project    | APPROVED | Pending |
|            | PRESYN-DESIGN-008-018 | public development lifecycle (privatize  | owner decision &    |          | P1B     |
|            |                       | only after Phase 20 complete); expand    | audit granularity   |          |         |
|            |                       | granular design requirements (009-018);  | standard            |          |         |
|            |                       | reconcile PRESYN-DESIGN-008 as governance|                     |          |         |
|            |                       | obligation and set concrete pages/assets |                     |          |         |
|            |                       | to NOT IMPLEMENTED until code verified.  |                     |          |         |
| 2026-09-06 | PRESYN-GEN-005        | Finalize Prompt 1B commit provenance hash| Post-commit audit   | APPROVED | 71df599 |
| 2026-09-06 | PRESYN-DATA-001       | Update model_versions to sha256_hash;    | Security & integrity| APPROVED | In Prog |
|            | and schema examples   | label schema examples as synthetic.      | standard update     |          | (Ph 01) |
| 2026-09-06 | Phase 01 Requirements | Phase 01 Core Application Skeleton:      | Phase 01 Foundation | APPROVED | In Prog |
|            | PRESYN-DESIGN-009-018 | FastAPI, 23 models, Alembic, health API, | milestone delivery  |          | (Ph 01) |
|            | PRESYN-DATA-001-003   | React 18, Vite, Tailwind, 6 domain shells|                     |          |         |
|            | PRESYN-UI-001-002     | favicon, legal pages, tests, CI.         |                     |          |         |
| 2026-09-06 | PRESYN-DATA-001,      | Phase 01 Post-Implementation Correction: | Independent post-   | APPROVED | 7e8dd61 |
|            | PRESYN-CAM-001 (found)| webcam/RTSP source model, secret-safe    | Phase 01 audit:     |          | (P1-Corr|
|            | PRESYN-TEST-001       | RTSP credential reference architecture,  | fix webcam support, |          | )       |
|            |                       | 11 finite domain status enums with check | secret safety, and  |          |         |
|            |                       | constraints, migration proof, regression.| uncontrolled strings|          |         |
| 2026-09-07 | PRESYN-DATA-001,      | Phase 01 Database Constraint Hardening:  | Independent audit:  | APPROVED | Pending |
|            | PRESYN-DATA-002,      | add explicit SQLite-level named CHECK    | enforce CHECK       |          | P1-Fin  |
|            | PRESYN-TEST-001       | constraints in new Alembic migration     | constraints in      |          |         |
|            |                       | d7327f3b3421 for all finite domain enums;| migrated databases, |          |         |
|            |                       | prove direct SQL failure on invalid data.| clean worktree.     |          |         |
+------------+-----------------------+------------------------------------------+---------------------+----------+---------+
```

---

## 29. REQUIREMENT TRACEABILITY CATALOG

Every capability in Presyn is governed by an explicit, immutable Traceability ID:

### 29.1 General & Governance (`PRESYN-GEN-*`)
- `PRESYN-GEN-001`: Single canonical specification authority located in `PRESYN_MASTER_PLAN.md`.
- `PRESYN-GEN-002`: Readme maintains subordinate linkage without competing specifications.
- `PRESYN-GEN-003`: Permanent 10-step Git workflow enforced across all prompts.
- `PRESYN-GEN-004`: Immutable Change Control Log maintained for all specification adjustments.
- `PRESYN-GEN-005`: Repository Visibility Lifecycle (Repository remains PUBLIC through Phases 00 to 19 and Phase 20 development; transitions to PRIVATE only after 100% Phase 20 completion and final release acceptance).

### 29.2 Immutable Design Rules (`PRESYN-DESIGN-*`)
- `PRESYN-DESIGN-001`: Strict prohibition of purple gradients and gradient-heavy SaaS visuals.
- `PRESYN-DESIGN-002`: Conventional rectangular or lightly rounded controls; no pill buttons.
- `PRESYN-DESIGN-003`: Complete prohibition of fabricated metrics, reviews, logos, counters, and statistics.
- `PRESYN-DESIGN-004`: Implementation of truthful empty states across all unpopulated views.
- `PRESYN-DESIGN-005`: Prohibition of emojis as interface icons (use `lucide-react` SVG icons exclusively).
- `PRESYN-DESIGN-006`: Prohibition of em dashes in marketing, technical, and product copy.
- `PRESYN-DESIGN-007`: Elimination of AI-slop imagery, stock photography, and hyperbolic AI buzzwords.
- `PRESYN-DESIGN-008`: Legal and privacy page requirement recorded as an immutable design obligation in specification.
- `PRESYN-DESIGN-009`: Custom Presyn favicon exists and is used by the production frontend.
- `PRESYN-DESIGN-010`: Dedicated Privacy Policy page exists and is reachable from persistent footer navigation.
- `PRESYN-DESIGN-011`: Dedicated Terms & Conditions page exists and is reachable from persistent footer navigation.
- `PRESYN-DESIGN-012`: No "Made with AI" badge/tag and no unnecessary "Powered by AI" branding in production UI.
- `PRESYN-DESIGN-013`: No cursor-following animation, custom animated cursor, or trailing-pointer effect.
- `PRESYN-DESIGN-014`: No AI-slop photography, generated fake employees, generated fake offices, or misleading synthetic workplace imagery.
- `PRESYN-DESIGN-015`: No AI-slop copy, exaggerated AI marketing language, or fake hero claims.
- `PRESYN-DESIGN-016`: No fabricated reviews, testimonials, customer logos, customer accounts, customer identities, case studies, production metrics, counters, or social proof.
- `PRESYN-DESIGN-017`: No excessive scroll animation, scroll-jacking, gratuitous parallax, or over-the-top page motion.
- `PRESYN-DESIGN-018`: Custom brand assets and product imagery must never weaken biometric/runtime Git safety boundaries.

Note: Requirements 009 through 018 provide explicit, item-by-item final audit granularity for the immutable design and brand rules, complementing and operationalizing requirements 001 through 008 without superseding them.

### 29.3 Core Operating & Hardware Constraints (`PRESYN-CONST-*`)
- `PRESYN-CONST-001`: Windows and Linux local-first CPU deployment without GPU/CUDA requirement.
- `PRESYN-CONST-002`: Performance calibration targeting Intel Core i7-1355U class processors.
- `PRESYN-CONST-003`: Memory and indexing support for 100+ employees and ~5,000 vector embeddings.
- `PRESYN-CONST-004`: 90% to 95% recognition accuracy target under controlled calibration; zero false claims.

### 29.4 Camera & Ingestion Architecture (`PRESYN-CAM-*`)
- `PRESYN-CAM-001`: Multi-source camera ingestion supporting RTSP network feeds and DirectShow USB webcams.
- `PRESYN-CAM-002`: Automated exponential backoff reconnect logic for dropped network streams.
- `PRESYN-CAM-003`: Decoupled capture thread and throttled inference processing queue.
- `PRESYN-CAM-004`: Telemetry tracking for capture FPS, inference FPS, latency, and connection state.

### 29.5 Computer Vision & Face Recognition (`PRESYN-REC-*`)
- `PRESYN-REC-001`: SCRFD-style ONNX face detection producing bounding boxes and 5-point facial landmarks.
- `PRESYN-REC-002`: Pre-embedding quality filters for resolution, Laplacian blur, and brightness.
- `PRESYN-REC-003`: ArcFace-style 512-dimensional normalized feature vector extraction on CPU.
- `PRESYN-REC-004`: Exact normalized NumPy cosine similarity vector search (`A @ B.T`).
- `PRESYN-REC-005`: Top-1 similarity threshold and top-1/top-2 candidate margin validation.
- `PRESYN-REC-006`: Multi-frame verification window (1.0 to 3.0 seconds) enforcing vote consensus.
- `PRESYN-REC-007`: Original Presyn visual verification indicator (`VERIFYING` to `VERIFIED`).

### 29.6 Enrollment & Incremental Learning (`PRESYN-ENROLL-*`)
- `PRESYN-ENROLL-001`: Five-view interactive employee enrollment wizard with real-time feedback.
- `PRESYN-ENROLL-002`: Maximum storage cap of 50 curated biometric templates per employee.
- `PRESYN-ENROLL-003`: Conservative incremental learning policy requiring elevated similarity and margin.
- `PRESYN-ENROLL-004`: Administrative template audit interface for inspecting and purging learned templates.

### 29.7 Person Tracking & Spatial Zones (`PRESYN-TRACK-*`)
- `PRESYN-TRACK-001`: Architectural separation between Person Tracking and Face Recognition.
- `PRESYN-TRACK-002`: Multi-person ByteTrack tracking preserving identity through temporary occlusions.
- `PRESYN-TRACK-003`: Configurable 2D polygon zones (entry, exit, work, restricted) on camera feeds.
- `PRESYN-TRACK-004`: Continuous presence session state machine (`VISIBLE`, `TEMPORARILY_LOST`, etc.).

### 29.8 Activity-State Estimation (`PRESYN-ACT-*`)
- `PRESYN-ACT-001`: Multi-frame pose and motion estimation classifying sitting, standing, and walking.
- `PRESYN-ACT-002`: Storage of duration-based `activity_segments` rather than wasteful per-frame rows.
- `PRESYN-ACT-003`: Strict policy prohibition preventing activity states from acting as productivity scores.

### 29.9 Attendance Policy Engine (`PRESYN-ATT-*`)
- `PRESYN-ATT-001`: Deduplicated first-arrival-of-the-day creation per confirmed employee.
- `PRESYN-ATT-002`: Support for standard, flexible, and overnight shifts with configurable grace periods.
- `PRESYN-ATT-003`: Audit-controlled manual attendance adjustment interface requiring mandatory text reasons.
- `PRESYN-ATT-004`: Formatted CSV attendance reporting and export generation.

### 29.10 Visitor & Unknown Workflows (`PRESYN-VIS-*`)
- `PRESYN-VIS-001`: Operational Visitor Mode toggle directly governing backend classification logic.
- `PRESYN-VIS-002`: Unknown person escalation flow preventing force-matching against employee roster.
- `PRESYN-VIS-003`: Centralized manual review queue for ambiguous recognitions and security warnings.

### 29.11 Optional Module Architecture (`PRESYN-OPT-*`)
- `PRESYN-OPT-001`: Lazy-loaded, feature-flagged isolation for all optional machine learning models.
- `PRESYN-OPT-002`: Optional mask detection elevating similarity threshold and disabling auto-learning.
- `PRESYN-OPT-003`: Optional liveness / anti-spoofing probe where `UNAVAILABLE` never equals `PASSED`.
- `PRESYN-OPT-004`: Optional aggregate Facial Expression Trend Analysis strictly decoupled from evaluations.

### 29.12 Database & Storage (`PRESYN-DATA-*`)
- `PRESYN-DATA-001`: SQLite relational schema supporting all 23 conceptual entities via SQLAlchemy 2.0.
- `PRESYN-DATA-002`: Alembic database migration management for reproducible schema versioning.
- `PRESYN-DATA-003`: Storage boundary restricting video archiving to external enterprise NVRs.

### 29.13 API & Live Streaming (`PRESYN-API-*`)
- `PRESYN-API-001`: Versioned REST API (`/api/v1`) providing full CRUD and management endpoints.
- `PRESYN-API-002`: Native WebSocket live event broadcasting conforming to standardized JSON contract.

### 29.14 Frontend & User Experience (`PRESYN-UI-*`)
- `PRESYN-UI-001`: Six primary information architecture domains (Live, Attendance, People, Security, Analytics, System).
- `PRESYN-UI-002`: Modern, calm, technical visual design implemented via React 18, Vite, and Tailwind CSS.
- `PRESYN-UI-003`: Project-owned lightweight SVG data visualizations without heavy external charting bloat.

### 29.15 Security, Privacy & Audit (`PRESYN-SEC-*`)
- `PRESYN-SEC-001`: Strict biometric data minimization storing 512D vectors without permanent raw photos.
- `PRESYN-SEC-002`: Role-based access control (RBAC) protecting sensitive administrative actions.
- `PRESYN-SEC-003`: Comprehensive cryptographic append-only audit trail logging all high-privilege events.
- `PRESYN-SEC-004`: Configurable data retention policies for events, logs, and temporary snapshots.

### 29.16 Performance & Testing (`PRESYN-TEST-*`)
- `PRESYN-TEST-001`: Automated test suite covering unit, integration, and scale benchmark scenarios.
- `PRESYN-TEST-002`: 100+ identity / 5,000 vector scale benchmark validating sub-100ms CPU vector search.
- `PRESYN-TEST-003`: 1-hour continuous soak test verifying zero memory leaks and stable camera ingestion.

---

## 30. FINAL IMPLEMENTATION VERIFICATION MATRIX

This matrix serves as the ultimate acceptance ledger for the Presyn project. Every requirement will be updated with concrete code and test evidence across development phases.

```
+------------------+------------------------------------------------------+---------------+-------------------------+-------------------------+-----------------+------------------------------------------+
| Requirement ID   | Requirement Description                              | Planned Phase | Implementation Evidence | Test Evidence           | Status          | Notes                                    |
+------------------+------------------------------------------------------+---------------+-------------------------+-------------------------+-----------------+------------------------------------------+
| PRESYN-GEN-001   | Canonical Master Plan Authority Document             | Phase 00      | PRESYN_MASTER_PLAN.md   | Manual Inspection       | IMPLEMENTED     | Single authoritative planning standard   |
| PRESYN-GEN-002   | Subordinate README Linkage                           | Phase 00      | README.md               | Manual Inspection       | IMPLEMENTED     | Clear pointer without competing specs    |
| PRESYN-GEN-003   | Permanent 10-Step Git Workflow                       | Phase 00      | PRESYN_MASTER_PLAN.md   | Verification Run        | IMPLEMENTED     | Mandatory for all future phases          |
| PRESYN-GEN-004   | Immutable Change Control Log                         | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 28 Baseline     | IMPLEMENTED     | Baseline established                     |
| PRESYN-GEN-005   | Repository Visibility Lifecycle (Public in Dev, Priv)| Phase 00      | Master Plan Sec 1.1, 28 | gh repo view (PUBLIC)   | IMPLEMENTED     | Public dev lifecycle; private post-P20   |
| PRESYN-DESIGN-001| Prohibition of Purple Gradients & SaaS Visuals       | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-002| Rectangular / Lightly Rounded Controls; No Pills     | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-003| Prohibition of Fabricated Data / Fake Social Proof   | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-004| Truthful Empty State Messaging                       | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-005| Prohibition of Emojis as Interface Icons             | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-006| Prohibition of Em Dashes in Copy                     | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-007| Prohibition of AI-Slop Imagery and Buzzwords         | Phase 00      | PRESYN_MASTER_PLAN.md   | Section 2 Audit         | IMPLEMENTED     | Immutable design rule recorded           |
| PRESYN-DESIGN-008| Accessible Privacy & Terms Governance Obligation     | Phase 00      | Master Plan Section 3   | Manual Inspection       | IMPLEMENTED     | Governance recorded; pages in 010/011    |
| PRESYN-DESIGN-009| Custom Presyn SVG Favicon Used by Frontend           | Phase 01      | frontend/public/favicon | vitest design_rules.test | IMPLEMENTED     | Custom geometric SVG favicon in index.html|
| PRESYN-DESIGN-010| Dedicated Privacy Policy Page with Footer Access     | Phase 01      | frontend/src/pages/Priv | vitest App.test.tsx      | IMPLEMENTED     | Accessible /privacy page and footer link  |
| PRESYN-DESIGN-011| Dedicated Terms & Conditions Page with Footer Access | Phase 01      | frontend/src/pages/Term | vitest App.test.tsx      | IMPLEMENTED     | Accessible /terms page and footer link    |
| PRESYN-DESIGN-012| No "Made with AI" Tags or Unnecessary AI Badges      | Phase 01      | Clean source / UI tree  | audit_compliance.py G2   | IMPLEMENTED     | Zero AI badges in source or rendered UI   |
| PRESYN-DESIGN-013| No Cursor-Following Animations or Pointer Trails     | Phase 01      | Native CSS cursor       | audit_compliance.py G3   | IMPLEMENTED     | Standard cursor; zero pointer animations  |
| PRESYN-DESIGN-014| No AI-Slop Photography or Fake Employee Stock Media  | Phase 01      | Zero tracked photo bins | audit_compliance.py G4   | IMPLEMENTED     | Zero stock photos; truthful empty states  |
| PRESYN-DESIGN-015| No AI-Slop Copy, Exaggerated Claims, or Fake Metrics | Phase 01      | Real telemetry copy only| vitest pages.test.tsx    | IMPLEMENTED     | Truthful empty states on all hub pages    |
| PRESYN-DESIGN-016| No Fabricated Reviews, Logos, Accounts, or Counters  | Phase 01      | Truthful UI empty states| vitest App.test.tsx      | IMPLEMENTED     | Zero fake reviews, logos, or demo accounts|
| PRESYN-DESIGN-017| No Excessive Scroll Animation or Parallax Gimmick    | Phase 01      | Standard CSS layout     | Frontend code inspection | IMPLEMENTED     | Zero parallax or scroll-jacking libraries |
| PRESYN-DESIGN-018| Brand Assets Never Weaken Git Safety Boundaries      | Phase 01      | SVG only; strict ignore | audit_compliance.py G4   | IMPLEMENTED     | Zero binary models or biometrics in git   |
| PRESYN-CONST-001 | Local-First CPU Architecture (No CUDA)               | Phase 01      | CPU backend dependencies| pip check; test_config   | PARTIAL         | Foundation established; CV in Phase 02+   |
| PRESYN-CONST-002 | Target Office CPU Optimization (Core i7-1355U class) | Phase 01      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 01 / Phase 18              |
| PRESYN-CONST-003 | 100+ Employees / ~5,000 Embedding Capacity Envelope  | Phase 05      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 05 / Phase 18              |
| PRESYN-CONST-004 | 90-95% Calibrated Recognition Accuracy Envelope      | Phase 06      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 06                         |
| PRESYN-CAM-001   | RTSP and Webcam Ingestion Architecture               | Phase 02      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 02                         |
| PRESYN-CAM-002   | Automated Reconnection with Exponential Backoff      | Phase 02      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 02                         |
| PRESYN-CAM-003   | Decoupled Capture and Inference Frame Throttling     | Phase 02      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 02                         |
| PRESYN-CAM-004   | Ingestion Telemetry & Health Monitoring              | Phase 02      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 02                         |
| PRESYN-REC-001   | SCRFD ONNX Face Detection & 5-Point Landmarks        | Phase 03      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 03                         |
| PRESYN-REC-002   | Face Quality Filtering (Blur, Size, Illumination)    | Phase 03      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 03                         |
| PRESYN-REC-003   | ArcFace ONNX 512D Normalized Embedding Extraction    | Phase 05      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 05                         |
| PRESYN-REC-004   | Exact Normalized NumPy Cosine Similarity Search      | Phase 05      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 05                         |
| PRESYN-REC-005   | Top-1 Threshold & Top-1/Top-2 Margin Validation      | Phase 05      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 05                         |
| PRESYN-REC-006   | Multi-Frame Temporal Verification Window (1 to 3s)    | Phase 06      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 06                         |
| PRESYN-REC-007   | Original Presyn Visual Verification Interaction       | Phase 06      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 06                         |
| PRESYN-ENROLL-001| Five-View Interactive Employee Enrollment Wizard      | Phase 04      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 04                         |
| PRESYN-ENROLL-002| Cap of 50 Curated Face Templates Per Employee        | Phase 04      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 04                         |
| PRESYN-ENROLL-003| Conservative Incremental Template Learning Engine     | Phase 09      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 09                         |
| PRESYN-ENROLL-004| Administrative Template Audit & Purge Management      | Phase 09      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 09                         |
| PRESYN-TRACK-001 | Separation of Spatial Tracking from Face Recognition  | Phase 10      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 10                         |
| PRESYN-TRACK-002 | ByteTrack Multi-Person Spatial Tracking               | Phase 10      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 10                         |
| PRESYN-TRACK-003 | Configurable Polygon Spatial Zones on Camera Feeds    | Phase 11      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 11                         |
| PRESYN-TRACK-004 | Continuous Presence Session Lifecycle Management      | Phase 11      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 11                         |
| PRESYN-ACT-001   | Physical Activity-State Estimation (Sit/Stand/Walk)   | Phase 12      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 12                         |
| PRESYN-ACT-002   | Temporal Activity-Segment Aggregation Storage         | Phase 12      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 12                         |
| PRESYN-ACT-003   | Strict Prohibition of Productivity Scoring from Pose  | Phase 12      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 12                         |
| PRESYN-ATT-001   | Deduplicated Daily Arrival Attendance Automation      | Phase 07      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 07                         |
| PRESYN-ATT-002   | Multi-Shift, Overnight, & Grace Period Support        | Phase 07      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 07                         |
| PRESYN-ATT-003   | Audit-Tracked Manual Attendance Corrections           | Phase 07      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 07                         |
| PRESYN-ATT-004   | Formatted Attendance CSV Reporting & Export           | Phase 07      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 07                         |
| PRESYN-VIS-001   | Active Visitor Mode Logic & State Switching           | Phase 08      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 08                         |
| PRESYN-VIS-002   | Unknown Person Escalation & Resolution Dispatcher     | Phase 08      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 08                         |
| PRESYN-VIS-003   | Centralized Manual Verification Queue                 | Phase 13      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 13                         |
| PRESYN-OPT-001   | Lazy-Loaded, Isolated Optional Model Architecture     | Phase 14      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 14                         |
| PRESYN-OPT-002   | Optional Mask Detection & Stricter Matching Policy    | Phase 14      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 14                         |
| PRESYN-OPT-003   | Optional Liveness Probe (Unavailable != Passed)       | Phase 15      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 15                         |
| PRESYN-OPT-004   | Optional Aggregate Facial Expression Trend Analysis   | Phase 17      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 17                         |
| PRESYN-DATA-001  | Relational SQLite Schema with 23 Domain Entities      | Phase 01      | backend/app/db/models   | pytest (38 backend tests)| IMPLEMENTED     | 23 models; webcam/RTSP; DB-level CHECKs  |
| PRESYN-DATA-002  | Alembic Schema Migrations Infrastructure              | Phase 01      | alembic.ini, migrations | test_migrations.py (7x)  | IMPLEMENTED     | 3 revisions: v1 + hardening; direct SQL  |
| PRESYN-DATA-003  | CCTV Storage Boundary (No 24/7 Video Archiving)       | Phase 01      | DB schema / .gitignore  | test_models.py           | PARTIAL         | Schema boundaries defined; video in Ph 02 |
| PRESYN-API-001   | Versioned REST API Architecture (`/api/v1`)           | Phase 01      | backend/app/api/router  | test_health_system.py    | PARTIAL         | Health & system v1 live; CRUD in Ph 04-13 |
| PRESYN-API-002   | Native WebSocket Live Streaming Contract              | Phase 02      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 02                         |
| PRESYN-UI-001    | Six Primary Operational Information Architecture Hubs | Phase 01      | 6 domain pages & App    | vitest App.test.tsx      | IMPLEMENTED     | Live, Attendance, People, Security, etc.  |
| PRESYN-UI-002    | High-Legibility Modern Interface (React + Tailwind)   | Phase 01      | React 18, Vite, Tailwind| npm run build; vitest    | IMPLEMENTED     | Clean slate theme; high-contrast tokens   |
| PRESYN-UI-003    | Project-Owned SVG Visualizations (No Bloat)           | Phase 16      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 16                         |
| PRESYN-SEC-001   | Biometric Vector Minimization & Template Erasure      | Phase 04      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 04                         |
| PRESYN-SEC-002   | Role-Based Access Control (RBAC) Governance           | Phase 19      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 19                         |
| PRESYN-SEC-003   | Immutable Append-Only Audit Logging Architecture      | Phase 01      | audit_log model schema  | test_models.py           | PARTIAL         | Schema foundation live; signing in Ph 19  |
| PRESYN-SEC-004   | Granular Data Retention Policies and Automated Purge  | Phase 19      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 19                         |
| PRESYN-TEST-001  | Automated Unit, Integration, & Regression Test Suite  | Phase 01      | pytest & vitest, CI     | 38 pytest, 17 vitest, CI | PARTIAL         | Core test harness live; expands per phase |
| PRESYN-TEST-002  | 100+ Identity / 5,000 Vector Scale Benchmark Suite    | Phase 18      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 18                         |
| PRESYN-TEST-003  | 1-Hour Soak Stability Verification Test               | Phase 20      | Pending Implementation  | Pending Test Execution  | NOT IMPLEMENTED | Planned Phase 20                         |
+------------------+------------------------------------------------------+---------------+-------------------------+-------------------------+-----------------+------------------------------------------+
```

---

## 31. DEFINITION OF DONE AND FINAL ACCEPTANCE CRITERIA

The Presyn project cannot be declared complete until the Final Implementation Verification Matrix is reviewed item by item. 

1. **Zero Unapproved Omissions**: Every requirement designated `NOT IMPLEMENTED` or `PARTIALLY IMPLEMENTED` blocks project completion unless an approved scope modification with justified business or technical rationale is permanently recorded in the Master Plan Change Control Log.
2. **Documented Evidence**: Every implemented requirement must reference concrete source file paths and passing automated test suites.
3. **Hardware Compliance**: All performance targets must be empirically demonstrated on target CPU hardware.
4. **Governance Compliance**: The codebase must be completely clean of purple gradients, pill buttons, fabricated metrics, em dashes, emojis as interface icons, and committed secrets or biometrics.
