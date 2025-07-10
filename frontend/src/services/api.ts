import axios from 'axios';
import { Company, ProcessingStatus, GTMResult } from '../types/index.ts';

const API_BASE_URL = 'http://localhost:8000/api/gtm';

export const api = {
  async processCompany(name: string, website: string): Promise<{ company_id: string; company: Company }> {
    const response = await axios.post(`${API_BASE_URL}/process-company`, {
      name,
      website
    });
    return response.data;
  },

  async getProcessingStatus(companyId: string): Promise<ProcessingStatus> {
    const response = await axios.get(`${API_BASE_URL}/status/${companyId}`);
    return response.data;
  },

  async getResult(companyId: string): Promise<GTMResult> {
    const response = await axios.get(`${API_BASE_URL}/result/${companyId}`);
    return response.data;
  }
};