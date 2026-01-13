import React from 'react';
import { JobState } from '../types';

interface ClaudeAnalysisViewProps {
  claudeAnalysis: JobState['claude_analysis'];
}

export const ClaudeAnalysisView: React.FC<ClaudeAnalysisViewProps> = ({ claudeAnalysis }) => {
  if (!claudeAnalysis) return null;


  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-4">
      <h3 className="font-semibold text-blue-900 mb-3">✅ Company Analysis Complete</h3>
      
      {/* Business Description */}
      <div className="bg-white p-3 rounded">
        <h4 className="font-medium text-blue-800 mb-1">Business Description</h4>
        <div className="text-sm text-blue-800">{claudeAnalysis.business_description}</div>
      </div>


      {/* Target Customers */}
      <div className="bg-white p-3 rounded">
        <h4 className="font-medium text-blue-800 mb-1">Target Customers</h4>
        <div className="text-sm text-blue-800">{claudeAnalysis.target_customers}</div>
      </div>

      {/* Data Needs */}
      {/* <div>
        <h4 className="font-medium text-blue-800 mb-1">Likely Data Needs</h4>
        <ul className="text-sm text-blue-700 list-disc list-inside space-y-1">
          {claudeAnalysis.likely_data_needs.map((need, index) => (
            <li key={index}>{need}</li>
          ))}
        </ul>
      </div> */}

      {/* Schema Preview */}
      <div className="bg-white p-3 rounded">
        <h4 className="font-medium text-blue-800 mb-2">Data Schema Preview</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {claudeAnalysis.schema_preview.map((table, index) => (
            <div key={index} className="bg-blue-100 p-3 rounded">
              <h5 className="font-medium text-blue-800 mb-1">{table.table_name}</h5>
              <div className="flex flex-wrap gap-1">
                {table.columns.map((column, colIndex) => (
                  <span key={colIndex} className="text-xs bg-white text-blue-800 px-2 py-1 rounded">
                    {column}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
