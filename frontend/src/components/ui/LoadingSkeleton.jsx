import React from 'react';

export const Skeleton = ({ className = '', rounded = 'rounded-md' }) => {
  return (
    <div
      className={`animate-pulse bg-slate-200/80 ${rounded} ${className}`}
      aria-hidden="true"
    />
  );
};

export const CardSkeleton = ({ count = 1 }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-4"
        >
          <div className="flex items-center justify-between">
            <Skeleton className="h-3 w-24" />
            <Skeleton className="h-7 w-7 rounded-lg" />
          </div>
          <div className="space-y-2">
            <Skeleton className="h-6 w-36" />
            <Skeleton className="h-3 w-20" />
          </div>
          <Skeleton className="h-1.5 w-full rounded-full" />
        </div>
      ))}
    </>
  );
};

export const TableSkeleton = ({ rows = 5, cols = 4 }) => {
  return (
    <div className="w-full border border-slate-200 rounded-xl overflow-hidden bg-white">
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex gap-4">
        {Array.from({ length: cols }).map((_, i) => (
          <Skeleton key={i} className="h-3 flex-1" />
        ))}
      </div>
      <div className="divide-y divide-slate-100">
        {Array.from({ length: rows }).map((_, r) => (
          <div key={r} className="px-5 py-4 flex gap-4 items-center">
            {Array.from({ length: cols }).map((_, c) => (
              <Skeleton key={c} className="h-4 flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export const ChartSkeleton = ({ height = 'h-64' }) => {
  return (
    <div className={`w-full ${height} rounded-xl border border-slate-200 bg-white p-5 flex flex-col justify-between`}>
      <div className="flex justify-between items-center">
        <Skeleton className="h-4 w-32" />
        <Skeleton className="h-3 w-16" />
      </div>
      <div className="flex items-end gap-3 h-40 pt-4">
        <Skeleton className="h-2/5 flex-1" />
        <Skeleton className="h-3/5 flex-1" />
        <Skeleton className="h-4/5 flex-1" />
        <Skeleton className="h-full flex-1" />
        <Skeleton className="h-3/4 flex-1" />
        <Skeleton className="h-1/2 flex-1" />
      </div>
    </div>
  );
};

export default { Skeleton, CardSkeleton, TableSkeleton, ChartSkeleton };
