import React, { useState } from 'react';
import { Company, ProcessingStatus, GTMResult } from '../types/index.ts';
import { CompanyCard } from './CompanyCard.tsx';
import { ProgressBar } from './ProgressBar.tsx';
import { ResultsView } from './ResultsView.tsx';
import { api } from '../services/api.ts';

export const Dashboard: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [processingStatuses, setProcessingStatuses] = useState<Map<string, ProcessingStatus>>(new Map());
  const [selectedResult, setSelectedResult] = useState<GTMResult | null>(null);
  const [formData, setFormData] = useState({ name: '', website: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.website) return;

    setIsSubmitting(true);
    try {
      const { company_id, company } = await api.processCompany(formData.name, formData.website);
      setCompanies(prev => [...prev, company]);
      
      pollProcessingStatus(company_id);
      
      setFormData({ name: '', website: '' });
    } catch (error) {
      console.error('Error processing company:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const pollProcessingStatus = async (companyId: string) => {
    const interval = setInterval(async () => {
      try {
        const status = await api.getProcessingStatus(companyId);
        setProcessingStatuses(prev => new Map(prev).set(companyId, status));
        
        if (status.progress >= 100 || status.error) {
          clearInterval(interval);
          
          setCompanies(prev => prev.map(company => 
            company.id === companyId 
              ? { ...company, status: status.error ? 'failed' : 'completed' }
              : company
          ));
        }
      } catch (error) {
        console.error('Error polling status:', error);
        clearInterval(interval);
      }
    }, 2000);
  };

  const handleViewResults = async (companyId: string) => {
    try {
      const result = await api.getResult(companyId);
      setSelectedResult(result);
    } catch (error) {
      console.error('Error fetching results:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mt-20 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Olive Outbound Workflow!
          </h1>
        </div>

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
              {isSubmitting ? 'Processing...' : 'Start Analysis'}
            </button>
          </form>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => {
            const status = processingStatuses.get(company.id);
            const canViewResults = company.status === 'completed';
            
            return (
              <div key={company.id} className="space-y-4">
                <CompanyCard
                  company={company}
                  onViewResults={() => handleViewResults(company.id)}
                  canViewResults={canViewResults}
                />
                
                {status && company.status !== 'completed' && company.status !== 'failed' && (
                  <ProgressBar
                    progress={status.progress}
                    currentStep={status.current_step}
                    error={status.error}
                  />
                )}
              </div>
            );
          })}
        </div>

        {selectedResult && (
          <ResultsView
            result={selectedResult}
            onClose={() => setSelectedResult(null)}
          />
        )}
      </div>
    </div>
  );
};