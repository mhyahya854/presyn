import React from "react";
import { FileText } from "lucide-react";

export const TermsPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-2 text-blue-500 mb-2">
          <FileText className="w-5 h-5" />
          <span className="text-xs font-mono uppercase tracking-wider">PRESYN-DESIGN-011</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Presyn Terms & Conditions</h1>
        <p className="text-xs text-slate-400 mt-1">
          Last updated: 2026-09-06 (Phase 01 Core Application Foundation)
        </p>
      </div>

      <div className="space-y-6 text-sm text-slate-300 leading-relaxed">
        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">1. Development Stage & Nature of Software</h2>
          <p>
            Presyn is an evolving software project currently in Phase 01 development. The code is provided
            on an "as is" and "as available" basis, without warranty of any kind, express or implied, including
            but not limited to the warranties of merchantability, fitness for a particular purpose, or
            non-infringement.
          </p>
          <p>
            Features in early development phases are subject to active modification, refactoring, and schema
            migrations. Users and operators deploying this software do so at their own discretion and risk.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">2. Deployment and Operational Responsibility</h2>
          <p>
            Presyn is designed as self-hosted software. No managed service, uptime service level agreement (SLA),
            or hosted infrastructure is provided by the software authors.
          </p>
          <p>
            The deploying operator is solely responsible for:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
            <li>Procuring and maintaining compatible hardware, cameras, and network infrastructure.</li>
            <li>Configuring appropriate authentication, TLS certificates, and internal network firewall rules.</li>
            <li>Backing up application databases and encryption keys.</li>
            <li>Conducting regular security audits and updating host software components.</li>
          </ul>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">3. Biometric and Legal Compliance</h2>
          <p>
            Biometric data processing is subject to rigorous and varying statutory frameworks worldwide.
            Deploying operators must obtain qualified legal counsel in their respective jurisdictions prior to
            deploying cameras or collecting facial biometric templates.
          </p>
          <p>
            Operators are required to ensure strict compliance with consent collection, retention limits,
            written policies, and disclosure obligations under applicable laws including, but not limited to,
            the European Union General Data Protection Regulation (GDPR) and the Illinois Biometric Information
            Privacy Act (BIPA).
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">4. Recognition Accuracy & Human Review</h2>
          <p>
            Computer vision and biometric recognition systems operate probabilistically. Presyn does not
            guarantee 100% facial recognition accuracy, liveness detection infallibility, or continuous track
            association across complex camera handoffs or difficult lighting conditions.
          </p>
          <p>
            Presyn is designed with human-in-the-loop review queues. Adverse disciplinary, employment, or
            access denial decisions must never be automated solely based on unverified inference scores without
            human review and verification.
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">5. Prohibited Uses</h2>
          <p>
            Presyn must not be used for:
          </p>
          <ul className="list-disc list-inside space-y-1.5 pl-2 text-slate-400">
            <li>Unlawful mass surveillance, tracking in private sanctuaries, or stalking without explicit legal authority.</li>
            <li>Harassment, discrimination, or unlawful profiling based on protected personal characteristics.</li>
            <li>Weaponized, military, or lethal autonomous systems.</li>
            <li>Any application that violates applicable national or international human rights conventions.</li>
          </ul>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold text-slate-100">6. Limitation of Liability</h2>
          <p>
            In no event shall the authors, maintainers, or contributors of Presyn be liable for any claim,
            damages, or other liability, whether in an action of contract, tort, or otherwise, arising from,
            out of, or in connection with the software or the use or other dealings in the software.
          </p>
        </section>
      </div>
    </div>
  );
};
