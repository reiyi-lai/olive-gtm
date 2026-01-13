import React from 'react';
import { JobState } from '../types';

interface ResultsViewProps {
  jobState: JobState;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ jobState }) => {
  if (!jobState.app_urls || jobState.app_urls.length === 0) return null;

  return (
    <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
      <h3 className="font-semibold text-purple-900 mb-3">
        🎉 Your Olive Apps are Ready!
      </h3>
      <p className="text-purple-700 mb-4">
        {jobState.total_tools} internal tools have been created for {jobState.company_name}
      </p>
      
      <div className="space-y-3">
        {jobState.app_urls.map((url, index) => (
          <div key={index} className="bg-white p-4 rounded border">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-sm font-medium text-gray-700">
                  Tool {index + 1}: {jobState.tool_suggestions?.[index]?.title || `App ${index + 1}`}
                </span>
                <div className="text-xs text-gray-500 font-mono mt-1">{url}</div>
              </div>
              <button
                onClick={() => window.open(url, '_blank')}
                className="px-4 py-2 bg-purple-600 text-white text-sm rounded hover:bg-purple-700 transition-colors"
              >
                Open App
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
