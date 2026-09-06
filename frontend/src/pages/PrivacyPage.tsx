import React from "react";
import { ShieldCheck } from "lucide-react";

export const PrivacyPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-2 text-blue-500 mb-2">
          <ShieldCheck className="w-5 h-5" />
          <span className="text-xs font-mono uppercase tracking-wider">PRESYN-DESIGN-010</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Presyn Privacy Policy</h1>
        <p className="text-xs text-slate-400 mt-1">
          Last updated: 2026-09-06 (Phase 01 Core Application Foundation)
        </p>
      </div>

      <div className="space-y-6 text-sm text-slate-300 leading-relaxed">
        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">1. Architecture and Privacy Principles</h2>
          <p>
            Presyn is an open-development workplace presence and spatial intelligence software platform.
            The software is engineered with a strict local-first architecture. Presyn does not operate
            a centralized cloud biometric repository and does not perform cross-site or public internet
            face search. All processing occurs locally within the infrastructure deployed and managed
            by the local system operator.
          </p>
          <p>
            Because Presyn is currently in active stage development (Phase 01), camera ingestion,
            face detection, biometric embedding extraction, and attendance recognition logic are
            not yet operational. The data policies detailed herein describe the design and privacy
            boundaries embedded in the software architecture.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">2. Planned Data Categories</h2>
          <p>
            When enabled in a completed deployment, Presyn is designed to manage the following categories
            of workplace information:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
            <li>
              <strong className="text-slate-200">Employee Identity Records:</strong> Structural metadata including
              employee identifiers, full names, department associations, work schedules, and operational status.
            </li>
            <li>
              <strong className="text-slate-200">Biometric Template Embeddings:</strong> Mathematical vector
              representations (512-dimensional float arrays) derived from authorized enrollment imagery. Original
              biometric source photos may be discarded or encrypted according to deployment policy.
            </li>
            <li>
              <strong className="text-slate-200">Attendance Verification Records:</strong> Daily check-in timestamps,
              shift durations, first-seen and last-seen timestamps, and verification confidence metrics.
            </li>
            <li>
              <strong className="text-slate-200">Spatial Presence & Activity Metadata:</strong> Zone dwell times,
              anonymized tracking identifiers, bounding box coordinates, and coarse activity states.
            </li>
            <li>
              <strong className="text-slate-200">Visitor & Unknown-Person Events:</strong> Temporary visitor records,
              short-lived tracking tokens, and timestamped event records when an unidentified face is observed.
            </li>
            <li>
              <strong className="text-slate-200">Optional Visual Snapshots:</strong> Transient cropped face images
              stored temporarily for human operator review, subject to strict automated retention pruning.
            </li>
            <li>
              <strong className="text-slate-200">Expression and State Aggregates:</strong> Coarse aggregate engagement
              statistics at the zone or department level. Presyn does not generate individual emotional profiles.
            </li>
            <li>
              <strong className="text-slate-200">Audit Logs & System Events:</strong> Cryptographically verifiable
              audit records documenting all administrative access, template enrollment, manual reviews, and configuration changes.
            </li>
          </ul>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">3. Data Minimization & Retention</h2>
          <p>
            Presyn incorporates data minimization controls by default:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
            <li>
              Raw video frames are processed in-memory and immediately discarded. Continuous CCTV video
              is never persisted to disk by the Presyn processing engine.
            </li>
            <li>
              Configurable automated retention windows govern raw detection events, unknown-person records,
              and review snapshots. Once a retention period expires, files and associated database entries
              are permanently purged.
            </li>
            <li>
              Biometric deletion is supported via explicit administrative actions that purge both database
              embeddings and FAISS/indexing caches.
            </li>
          </ul>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">4. Deployment Compliance Responsibility</h2>
          <p>
            Presyn is provided as open-source software. The organization or entity deploying Presyn acts
            as the sole data controller and assumes full legal responsibility for compliance with applicable
            data protection laws (such as GDPR, CCPA/CPRA, Illinois BIPA, and relevant local labor regulations).
          </p>
          <p>
            Deploying organizations must conduct a Data Protection Impact Assessment (DPIA), provide adequate
            notice and obtain required employee or visitor consents, establish legal grounds for biometric
            processing, and configure appropriate retention periods prior to activating camera feeds.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">5. Security Governance</h2>
          <p>
            The software design enforces role-based access control (RBAC), SQLite foreign key integrity,
            parameterized SQL queries, and explicit sanitization to prevent secrets or biometric data from
            leaking through public API endpoints, logs, or unauthenticated health probes.
          </p>
        </section>
      </div>
    </div>
  );
};
