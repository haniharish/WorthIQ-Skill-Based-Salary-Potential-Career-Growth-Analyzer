import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, Sparkles } from 'lucide-react';

export const Logo = ({
  className = '',
  size = 'md',
  to = '/',
  showBadge = false,
}) => {
  const iconSizes = {
    sm: 'w-6 h-6',
    md: 'w-7 h-7',
    lg: 'w-9 h-9',
  };

  const textSizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  };

  const content = (
    <div className={`inline-flex items-center gap-2.5 font-bold tracking-tight select-none ${className}`}>
      <div className={`relative flex items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-600 to-violet-500 text-white shadow-sm shadow-indigo-500/25 ${iconSizes[size] || iconSizes.md}`}>
        <TrendingUp className="w-4 h-4 stroke-[2.5]" />
        <span className="absolute -top-1 -right-1 flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
      </div>
      <div className="flex items-center">
        <span className={`text-slate-900 font-extrabold ${textSizes[size] || textSizes.md}`}>
          Worth<span className="text-indigo-600 font-extrabold">IQ</span>
        </span>
        {showBadge && (
          <span className="ml-2 text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-700 border border-indigo-200/60">
            Phase 1
          </span>
        )}
      </div>
    </div>
  );

  if (to) {
    return <Link to={to} className="inline-block transition-opacity hover:opacity-90">{content}</Link>;
  }

  return content;
};

export default Logo;
