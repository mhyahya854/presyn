import React from "react";
import { NavLink } from "react-router-dom";
import {
  Video,
  Clock,
  Users,
  Shield,
  BarChart2,
  Activity,
} from "lucide-react";

interface NavItem {
  name: string;
  to: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItem[] = [
  { name: "Live", to: "/live", icon: Video },
  { name: "Attendance", to: "/attendance", icon: Clock },
  { name: "People", to: "/people", icon: Users },
  { name: "Security", to: "/security", icon: Shield },
  { name: "Analytics", to: "/analytics", icon: BarChart2 },
  { name: "System", to: "/system", icon: Activity },
];

export const Navbar: React.FC = () => {
  return (
    <header className="border-b border-slate-800 bg-[#111726] sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center space-x-8">
            <NavLink
              to="/live"
              className="flex items-center space-x-2.5 text-white font-semibold text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded px-1"
              aria-label="Presyn Home"
            >
              <svg
                className="w-6 h-6 shrink-0"
                viewBox="0 0 32 32"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <rect width="32" height="32" rx="4" fill="#090d16" />
                <rect x="0.5" y="0.5" width="31" height="31" rx="3.5" stroke="#1e293b" />
                <rect x="7" y="7" width="5" height="18" rx="1" fill="#2563eb" />
                <rect x="12" y="7" width="9" height="5" fill="#2563eb" />
                <rect x="17" y="10" width="4" height="6" fill="#2563eb" />
                <rect x="12" y="14" width="9" height="5" fill="#2563eb" />
                <circle cx="21" cy="23" r="2.5" fill="#10b981" />
              </svg>
              <span className="tracking-tight text-slate-100 font-bold text-lg">PRESYN</span>
              <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                Phase 01
              </span>
            </NavLink>

            <nav aria-label="Main navigation" className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      `flex items-center space-x-2 px-3 py-1.5 text-xs font-medium rounded border transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 ${
                        isActive
                          ? "bg-slate-800 text-white border-slate-700"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60 border-transparent"
                      }`
                    }
                  >
                    <Icon className="w-3.5 h-3.5 shrink-0" />
                    <span>{item.name}</span>
                  </NavLink>
                );
              })}
            </nav>
          </div>

          <div className="flex items-center space-x-3 text-xs text-slate-400">
            <span className="inline-flex items-center space-x-1.5 px-2 py-1 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono">
              <span className="w-1.5 h-1.5 rounded-sm bg-emerald-500"></span>
              <span>CORE SKELETON</span>
            </span>
          </div>
        </div>

        {/* Mobile Navigation bar */}
        <div className="md:hidden py-2 border-t border-slate-800/80 flex flex-wrap gap-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center space-x-1.5 px-2.5 py-1 text-xs font-medium rounded border transition-colors ${
                    isActive
                      ? "bg-slate-800 text-white border-slate-700"
                      : "text-slate-400 hover:text-slate-200 border-transparent"
                  }`
                }
              >
                <Icon className="w-3 h-3 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </div>
      </div>
    </header>
  );
};
