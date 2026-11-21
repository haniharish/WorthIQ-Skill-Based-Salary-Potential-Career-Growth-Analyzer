import React from 'react';

const variants = {
  indigo: 'bg-indigo-50 text-indigo-700 border-indigo-200/60',
  emerald: 'bg-emerald-50 text-emerald-700 border-emerald-200/60',
  amber: 'bg-amber-50 text-amber-700 border-amber-200/60',
  slate: 'bg-slate-100 text-slate-700 border-slate-200/80',
  rose: 'bg-rose-50 text-rose-700 border-rose-200/60',
  sky: 'bg-sky-50 text-sky-700 border-sky-200/60',
  purple: 'bg-purple-50 text-purple-700 border-purple-200/60',
};

const dotColors = {
  indigo: 'bg-indigo-500',
  emerald: 'bg-emerald-500',
  amber: 'bg-amber-500',
  slate: 'bg-slate-500',
  rose: 'bg-rose-500',
  sky: 'bg-sky-500',
  purple: 'bg-purple-500',
};

export const Badge = ({
  children,
  variant = 'indigo',
  size = 'sm',
  dot = false,
  className = '',
}) => {
  const sizeClasses = size === 'xs' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs';

  return (
    <span
      className={`
        inline-flex items-center font-medium rounded-full border
        ${variants[variant] || variants.indigo}
        ${sizeClasses}
        ${className}
      `}
    >
      {dot && (
        <span
          className={`w-1.5 h-1.5 rounded-full mr-1.5 ${
            dotColors[variant] || dotColors.indigo
          }`}
        />
      )}
      {children}
    </span>
  );
};

export default Badge;
