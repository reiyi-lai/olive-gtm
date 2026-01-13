import axios from 'axios';
import { JobState, StartAnalysisRequest, StartAnalysisResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  async startAnalysis(name: string, website: string): Promise<StartAnalysisResponse> {
    const response = await axios.post<StartAnalysisResponse>(`${API_BASE_URL}/analyze-company`, {
      name,
      website
    } as StartAnalysisRequest);
    return response.data;
  },

  async getJobStatus(jobId: string): Promise<JobState> {
    const response = await axios.get<JobState>(`${API_BASE_URL}/job/${jobId}`);
    return response.data;
  }
};

