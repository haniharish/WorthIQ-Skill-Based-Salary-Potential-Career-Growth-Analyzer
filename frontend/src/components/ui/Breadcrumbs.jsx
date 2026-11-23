import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

const ROUTE_LABELS = {
  dashboard: 'Overview',
  'salary-analysis': 'Salary Analysis',
  'skill-impact': 'Skill Intelligence',
  'skill-intelligence': 'Skill Intelligence',
  'job-matching': 'Role Matching',
  'role-matching': 'Role Matching',
  'career-roadmap': 'Career Roadmap',
  roadmaps: 'Career Roadmap',
  'what-if-simulator': 'What-If Simulator',
  'what-if': 'What-If Simulator',
  'saved-reports': 'Saved Reports',
  reports: 'Saved Reports',
  explanations: 'SHAP Explainability',
  profile: 'My Profile',
  setup: 'Setup',
  settings: 'Settings',
};

export const Breadcrumbs = ({ customItems }) => {
  const location = useLocation();

  if (customItems) {
    return (
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
        <Link to="/dashboard" className="text-slate-400 hover:text-indigo-600 transition-colors flex items-center gap-1">
          <Home className="w-3.5 h-3.5" />
        </Link>
        {customItems.map((item, idx) => (
          <React.Fragment key={idx}>
            <ChevronRight className="w-3 h-3 text-slate-300 shrink-0" />
            {item.path ? (
              <Link to={item.path} className="text-slate-500 hover:text-indigo-600 transition-colors truncate max-w-[150px]">
                {item.label}
              </Link>
            ) : (
              <span className="font-semibold text-slate-800 truncate max-w-[150px]">{item.label}</span>
            )}
          </React.Fragment>
        ))}
      </nav>
    );
  }

  const segments = location.pathname.split('/').filter(Boolean);

  if (segments.length === 0 || (segments.length === 1 && segments[0] === 'dashboard')) {
    return (
      <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
        <Link to="/dashboard" className="text-slate-400 hover:text-indigo-600 transition-colors flex items-center gap-1">
          <Home className="w-3.5 h-3.5" />
        </Link>
        <ChevronRight className="w-3 h-3 text-slate-300 shrink-0" />
        <span className="font-semibold text-slate-800">Dashboard</span>
      </nav>
    );
  }

  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
      <Link to="/dashboard" className="text-slate-400 hover:text-indigo-600 transition-colors flex items-center gap-1">
        <Home className="w-3.5 h-3.5" />
      </Link>
      {segments.map((seg, idx) => {
        const isLast = idx === segments.length - 1;
        const label = ROUTE_LABELS[seg] || (seg.length > 15 ? `${seg.slice(0, 8)}...` : seg);
        const path = `/${segments.slice(0, idx + 1).join('/')}`;

        return (
          <React.Fragment key={path}>
            <ChevronRight className="w-3 h-3 text-slate-300 shrink-0" />
            {isLast ? (
              <span className="font-semibold text-slate-800">{label}</span>
            ) : (
              <Link to={path} className="text-slate-500 hover:text-indigo-600 transition-colors">
                {label}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};

export default Breadcrumbs;
