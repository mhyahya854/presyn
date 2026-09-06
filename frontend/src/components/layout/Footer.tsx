import React from "react";
import { Link } from "react-router-dom";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800 bg-[#090d16] py-4 px-6 text-xs text-slate-400">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center space-x-2">
          <span className="font-medium text-slate-300">Presyn</span>
          <span className="text-slate-600">|</span>
          <span>(c) 2026 Presyn. Workplace presence and intelligence platform.</span>
        </div>
        <nav aria-label="Legal navigation" className="flex items-center space-x-6">
          <Link
            to="/privacy"
            className="text-slate-400 hover:text-slate-200 transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500 rounded px-1"
          >
            Privacy Policy
          </Link>
          <Link
            to="/terms"
            className="text-slate-400 hover:text-slate-200 transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500 rounded px-1"
          >
            Terms & Conditions
          </Link>
        </nav>
      </div>
    </footer>
  );
};
