import React from 'react';
import Card from './Card';
import Badge from './Badge';

export const StatCard = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badgeText,
  badgeVariant = 'indigo',
  trend,
  trendDirection = 'neutral',
  progressPercent,
  className = '',
  onClick,
}) => {
  return (
    <Card
      padding="p-5"
      className={`relative overflow-hidden transition-all duration-200 hover:shadow-md ${
        onClick ? 'cursor-pointer hover:border-indigo-300' : ''
      } ${className}`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider truncate">
          {title}
        </span>
        {Icon && (
          <div className="p-2 rounded-lg bg-indigo-50/80 text-indigo-600 shrink-0">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-3">
        <div className="flex items-baseline gap-2 flex-wrap">
          <p className="text-2xl font-black text-slate-900 tracking-tight">{value}</p>
          {badgeText && (
            <Badge variant={badgeVariant} size="xs">
              {badgeText}
            </Badge>
          )}
        </div>

        {subtitle && (
          <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5 flex-wrap">
            {trend && (
              <span
                className={`font-semibold ${
                  trendDirection === 'up'
                    ? 'text-emerald-600'
                    : trendDirection === 'down'
                    ? 'text-rose-600'
                    : 'text-slate-600'
                }`}
              >
                {trend}
              </span>
            )}
            <span>{subtitle}</span>
          </p>
        )}
      </div>

      {typeof progressPercent === 'number' && (
        <div className="w-full bg-slate-100 h-1.5 rounded-full mt-3.5 overflow-hidden">
          <div
            className="bg-indigo-600 h-1.5 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(100, Math.max(0, progressPercent))}%` }}
          />
        </div>
      )}
    </Card>
  );
};

export default StatCard;
