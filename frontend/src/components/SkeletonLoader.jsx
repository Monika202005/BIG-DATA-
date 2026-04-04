import React from 'react';

const SkeletonLoader = () => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden animate-pulse">
      <div className="p-5">
        <div className="flex justify-between items-start mb-4">
          <div className="h-6 bg-slate-200 rounded-full w-24"></div>
          <div className="text-right space-y-2">
            <div className="h-3 bg-slate-200 rounded w-16 ml-auto"></div>
            <div className="h-6 bg-slate-200 rounded w-12 ml-auto"></div>
          </div>
        </div>
        
        <div className="h-6 bg-slate-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-slate-200 rounded w-full mb-2"></div>
        <div className="h-4 bg-slate-200 rounded w-5/6 mb-4"></div>
        
        <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
          <div className="h-4 bg-slate-200 rounded w-20"></div>
          <div className="h-4 bg-slate-200 rounded w-24"></div>
        </div>
      </div>
    </div>
  );
};

export default SkeletonLoader;
