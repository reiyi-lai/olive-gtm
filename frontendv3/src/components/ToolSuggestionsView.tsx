import React from 'react';
import { JobState } from '../types';

interface ToolSuggestionsViewProps {
  toolSuggestions: JobState['tool_suggestions'];
}

export const ToolSuggestionsView: React.FC<ToolSuggestionsViewProps> = ({ toolSuggestions }) => {
  if (!toolSuggestions || toolSuggestions.length === 0) return null;

  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
      <h3 className="font-semibold text-green-900 mb-3">✅ Tool Suggestions Generated</h3>
      <div className="space-y-3">
        {toolSuggestions.map((tool, index) => (
          <div key={index} className="bg-white p-3 rounded">
            <h4 className="font-medium text-green-700 mb-2">{tool.title}</h4>
            <div className="space-y-1">
              <p className="text-sm text-gray-700 font-medium">Prompt:</p>
              <p className="text-sm text-gray-600">
                {tool.prompt}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
