import React from 'react';
import { GTMResult } from '../types/index.ts';

interface ResultsViewProps {
  result: GTMResult;
  onClose: () => void;
}

export const ResultsView: React.FC<ResultsViewProps> = ({ result, onClose }) => {
  // Debug logging
  console.log('ResultsView result:', result);
  console.log('Generated prompt:', result?.generatedPrompt);
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              GTM Results: {result.company.name}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="space-y-6">
            {result.generatedPrompt ? (
              <div className="bg-olive-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-olive-800 mb-3">
                  Generated Olive Prompt
                </h3>
                <div className="bg-white p-4 rounded border">
                  <p className="text-gray-800 mb-4">{result.generatedPrompt.prompt}</p>
                  <div className="text-sm text-gray-600">
                    <p className="gray-50 rounded-lg p-4"><strong>Expected Dashboard:</strong> <br></br>{result.generatedPrompt.expectedDashboard}</p>
                    {/* <br></br> */}
                    {/* <p className="gray-50 rounded-lg p-4"><strong>Confidence:</strong> {(result.generatedPrompt.confidence * 100).toFixed(0)}%</p> */}
                    {/* <p><strong>Reasoning:</strong> {result.generatedPrompt.reasoning}</p> */}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-red-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-red-800 mb-3">
                  Generated Prompt Missing
                </h3>
                <p>Debug: {JSON.stringify(result, null, 2)}</p>
              </div>
            )}
            
            {result.scrapedData ? (
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                  Business Analysis
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p><strong>Business Type:</strong> {result.scrapedData.businessType || result.scrapedData.business_type || 'N/A'}</p>
                    <p><strong>Description:</strong> {result.scrapedData.description || 'N/A'}</p>
                  </div>
                  <div>
                    <p><strong>Key Features:</strong></p>
                    <ul className="list-disc list-inside text-sm text-gray-600">
                      {(result.scrapedData.keyFeatures || result.scrapedData.key_features || []).map((feature: string, index: number) => (
                        <li key={index}>{feature}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-yellow-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-yellow-800 mb-3">
                  Business Analysis Missing
                </h3>
                <p>Scraped data not available</p>
              </div>
            )}
            
            {result.schema && (
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-blue-800 mb-3">
                  Database Schema
                </h3>
                <div className="bg-white p-4 rounded border overflow-x-auto">
                  <pre className="text-sm text-gray-800">
                    {JSON.stringify(result.schema, null, 2)}
                  </pre>
                </div>
              </div>
            )}
            
            {result.sampleData && (
              <div className="bg-green-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-green-800 mb-3">
                  Sample Data Preview
                </h3>
                <div className="bg-white p-4 rounded border overflow-x-auto">
                  <pre className="text-sm text-gray-800">
                    {JSON.stringify(result.sampleData, null, 2).substring(0, 1000)}...
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};