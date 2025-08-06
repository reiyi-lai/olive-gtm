import React from 'react';
import { GTMResult } from '../types/index.ts';

interface ResultsViewProps {
  result: GTMResult;
  onClose: () => void;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ result, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              GTM Results: {result.company_id}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ×
            </button>
          </div>

          <div className="space-y-6">
            {result.connection_string && (
              <div className="bg-purple-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-purple-800 mb-3">
                  Neon PostgreSQL Database
                </h3>
                <div className="bg-white p-4 rounded border">
                  <div className="flex items-center space-x-2">
                    <code className="px-2 py-1 bg-gray-100 rounded text-sm font-mono flex-1">
                      {result.connection_string}
                    </code>
                    <button
                      onClick={() => navigator.clipboard.writeText(result.connection_string)}
                      className="px-3 py-1 bg-purple-600 text-white text-xs rounded hover:bg-purple-700 transition-colors"
                      title="Copy connection string"
                    >
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            )}
            
            {result.markdown_output && (
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                  Complete GTM Analysis Report
                </h3>
                <div className="bg-white p-4 rounded border overflow-x-auto max-h-96">
                  <pre className="text-sm text-gray-800 whitespace-pre-wrap font-sans">
                    {result.markdown_output}
                  </pre>
                </div>
              </div>
            )}

            <div className="bg-green-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-green-800 mb-3">
                Status: {result.status}
              </h3>
              <p className="text-green-700">
                Your GTM analysis is complete! The database has been created with sample data and is ready for use.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};