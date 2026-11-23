import React from 'react';
import Badge from './Badge';

export const ConfidenceIndicator = ({ level = 'Medium', score, showBar = true, size = 'sm' }) => {
  const normalizedLevel = (level || 'Medium').toLowerCase();

  const getVariant = () => {
    switch (normalizedLevel) {
      case 'high':
        return 'emerald';
      case 'medium':
        return 'indigo';
      case 'low':
      default:
        return 'amber';
    }
  };

  const getPercentage = () => {
    if (typeof score === 'number') return Math.min(100, Math.max(0, score));
    switch (normalizedLevel) {
      case 'high':
        return 88;
      case 'medium':
        return 70;
      case 'low':
      default:
        return 45;
    }
  };

  const percentage = getPercentage();

  return (
    <div className="space-y-1.5">
      <div className="flex items-center gap-2">
        <Badge variant={getVariant()} size={size} dot={true}>
          {level} Confidence {typeof score === 'number' ? `(${score}%)` : ''}
        </Badge>
      </div>

      {showBar && (
        <div className="w-full bg-slate-100 h-1 rounded-full overflow-hidden">
          <div
            className={`h-1 rounded-full transition-all duration-500 ${
              normalizedLevel === 'high'
                ? 'bg-emerald-500'
                : normalizedLevel === 'medium'
                ? 'bg-indigo-500'
                : 'bg-amber-500'
            }`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      )}
    </div>
  );
};

export default ConfidenceIndicator;
