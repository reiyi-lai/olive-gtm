export interface Company {
  id: string;
  name: string;
  website: string;
  industry?: string;
  status: 'pending' | 'scraping' | 'analyzing' | 'generating' | 'completed' | 'failed';
}

export interface ProcessingStatus {
  company_id: string;
  current_step: string;
  progress: number;
  error?: string;
}

export interface GTMResult {
  company_id: string;
  markdown_output: string;
  connection_string: string;
  status: string;
}