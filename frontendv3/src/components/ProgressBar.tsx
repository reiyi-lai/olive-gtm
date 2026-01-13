import React from 'react';

interface ProgressBarProps {
  progress: number;
  currentStep: string;
  error?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ 
  progress, 
  currentStep, 
  error 
}) => {
  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">{currentStep}</span>
        <span className="text-sm text-gray-500">{progress}%</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className={`h-2 rounded-full transition-all duration-300 ${
            error ? 'bg-red-500' : 'bg-olive-600'
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>
      
      {error && (
        <div className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
          Error: {error}
        </div>
      )}
    </div>
  );
};

