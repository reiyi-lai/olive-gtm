import React from 'react';
import { Company } from '../types/index.ts';

interface CompanyCardProps {
  company: Company;
  onViewResults: () => void;
  canViewResults: boolean;
}

export const CompanyCard: React.FC<CompanyCardProps> = ({ 
  company, 
  onViewResults, 
  canViewResults 
}) => {
  const getStatusColor = (status: Company['status']) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'pending': return 'bg-gray-100 text-gray-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{company.name}</h3>
          <p className="text-sm text-gray-600">{company.website}</p>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(company.status)}`}>
          {company.status}
        </span>
      </div>
      
      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500">
          {company.website}
        </span>
        
        {canViewResults && (
          <button
            onClick={onViewResults}
            className="px-4 py-2 bg-olive-600 text-white rounded-md hover:bg-olive-700 transition-colors text-sm"
          >
            View Results
          </button>
        )}
      </div>
    </div>
  );
};