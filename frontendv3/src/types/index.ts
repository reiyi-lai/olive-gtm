export interface JobState {
  job_id: string;
  company_name: string;
  status: 'analyzing' | 'completed' | 'failed';
  progress: number;
  current_step: string;
  claude_analysis?: {
    business_description: string;
    target_customers: string;
    likely_data_needs: string[];
    connection_string_masked: string;
    schema_preview: Array<{
      table_name: string;
      columns: string[];
    }>;
  };
  tool_suggestions?: Array<{
    title: string;
    prompt: string;
  }>;
  app_urls?: string[];
  total_tools?: number;
  error?: string;
}

export interface StartAnalysisRequest {
  name: string;
  website: string;
}

export interface StartAnalysisResponse {
  job_id: string;
  status: string;
}

