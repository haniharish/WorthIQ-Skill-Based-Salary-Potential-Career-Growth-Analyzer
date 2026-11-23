import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import Button from './Button';

export const ErrorState = ({
  title = 'Failed to load data',
  message = 'An unexpected error occurred while fetching information from the server.',
  onRetry,
  className = '',
}) => {
  return (
    <div
      className={`rounded-2xl border border-rose-200 bg-rose-50/50 p-6 sm:p-8 text-center max-w-md mx-auto ${className}`}
    >
      <div className="w-10 h-10 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-3">
        <AlertTriangle className="w-5 h-5" />
      </div>
      <h3 className="text-sm font-bold text-rose-950 tracking-tight">{title}</h3>
      <p className="text-xs text-rose-800 mt-1 leading-relaxed max-w-sm mx-auto">
        {message}
      </p>

      {onRetry && (
        <div className="mt-4 flex justify-center">
          <Button
            variant="outline"
            size="sm"
            icon={RefreshCw}
            onClick={onRetry}
            className="border-rose-300 text-rose-900 hover:bg-rose-100/70"
          >
            Try Again
          </Button>
        </div>
      )}
    </div>
  );
};

export default ErrorState;
