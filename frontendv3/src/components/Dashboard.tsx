import React, { useState } from 'react';
import { JobState } from '../types';
import { ProgressBar } from './ProgressBar';
import { ClaudeAnalysisView } from './ClaudeAnalysisView';
import { ToolSuggestionsView } from './ToolSuggestionsView';
import { api } from '../services/api';

export const Dashboard: React.FC = () => {
  const [jobStates, setJobStates] = useState<Map<string, JobState>>(new Map());
  const [formData, setFormData] = useState({ name: '', website: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentView, setCurrentView] = useState<'analysis' | 'suggestions'>('analysis');
  const [showModal, setShowModal] = useState(false);
  const [selectedJobState, setSelectedJobState] = useState<JobState | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.website) return;

    setIsSubmitting(true);
    try {
      const response = await api.startAnalysis(formData.name, formData.website);
      
      // Initialize job state
      const initialJobState: JobState = {
        job_id: response.job_id,
        company_name: formData.name,
        status: 'analyzing',
        progress: 0,
        current_step: 'Starting analysis...'
      };
      
      setJobStates(prev => new Map(prev).set(response.job_id, initialJobState));

      // Reset view state for new job
      setCurrentView('analysis');
      setShowModal(false);

      // Start polling for updates
      pollJobStatus(response.job_id);
      
      setFormData({ name: '', website: '' });
    } catch (error) {
      console.error('Error starting analysis:', error);
      alert('Failed to start analysis. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const interval = setInterval(async () => {
      try {
        const jobState = await api.getJobStatus(jobId);
        setJobStates(prev => new Map(prev).set(jobId, jobState));

        // Auto-switch to suggestions view when tool suggestions are ready
        if (jobState.tool_suggestions && currentView === 'analysis') {
          setCurrentView('suggestions');
        }

        if (jobState.status === 'completed' || jobState.status === 'failed') {
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Error polling job status:', error);
        clearInterval(interval);
      }
    }, 2000); // Poll every 2 seconds
  };

  const jobStatesArray = Array.from(jobStates.values()).reverse(); // Show newest first

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mt-20 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Olive Custom Demo!
          </h1>
        </div>

        {/* Form */}
        <div className="max-w-md mx-auto mb-8">
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Add New Company
            </h2>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Name
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-olive-500"
                required
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Website URL
              </label>
              <input
                type="url"
                value={formData.website}
                onChange={(e) => setFormData(prev => ({ ...prev, website: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-olive-500"
                required
              />
            </div>
            
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-olive-600 text-white py-2 px-4 rounded-md hover:bg-olive-700 disabled:opacity-50 transition-colors"
            >
              {isSubmitting ? 'Starting Analysis...' : 'Start Analysis'}
            </button>
          </form>
        </div>

        {/* Job Results */}
        <div className="max-w-xl ml-0 space-y-6">
          {jobStatesArray.map((jobState) => (
            <div key={jobState.job_id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{jobState.company_name}</h3>
                  {/* <p className="text-sm text-gray-500">Job ID: {jobState.job_id}</p> */}
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  jobState.status === 'completed' ? 'bg-green-100 text-green-800' :
                  jobState.status === 'failed' ? 'bg-red-100 text-red-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {jobState.status}
                </span>
              </div>

              {/* Progress Bar */}
              {jobState.status !== 'failed' && (
                <div className="mb-6">
                  <ProgressBar
                    progress={jobState.progress}
                    currentStep={jobState.current_step}
                    error={jobState.error}
                  />
                </div>
              )}

              {/* Error Display */}
              {jobState.error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-700">
                    <strong>Error:</strong> {jobState.error}
                  </p>
                </div>
              )}

              {/* Stage Results */}
              <div className="space-y-4">
                {/* Current View */}
                {currentView === 'analysis' ? (
                  <ClaudeAnalysisView claudeAnalysis={jobState.claude_analysis} />
                ) : (
                  <ToolSuggestionsView toolSuggestions={jobState.tool_suggestions} />
                )}

                {/* Action Buttons */}
                <div className="flex justify-end">
                  {jobState.app_urls && (
                    <button
                      onClick={() => {
                        setSelectedJobState(jobState);
                        setShowModal(true);
                      }}
                      className="px-4 py-2 bg-olive-600 text-white rounded hover:bg-olive-700 transition-colors"
                    >
                      View Olive Apps
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Modal for Olive Apps */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">
                    GTM Results
                  </h2>
                  <button
                    onClick={() => setShowModal(false)}
                    className="text-gray-500 hover:text-gray-700 text-xl"
                  >
                    ×
                  </button>
                </div>
                {selectedJobState && selectedJobState.app_urls && (
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                    <h3 className="font-semibold text-purple-900 mb-3">
                      🎉 Your Olive Apps are Ready!
                    </h3>
                    <p className="text-purple-700 mb-4">
                      {selectedJobState.total_tools} internal tools have been created for {selectedJobState.company_name}
                    </p>

                    <div className="space-y-3">
                      {selectedJobState.app_urls.map((url, index) => (
                        <div key={index} className="bg-white p-4 rounded border">
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="text-sm font-medium text-gray-700">
                                Tool {index + 1}: {selectedJobState.tool_suggestions?.[index]?.title || `App ${index + 1}`}
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
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
