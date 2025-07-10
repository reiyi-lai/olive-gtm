export interface Company {
  id: string;
  name: string;
  website: string;
  industry?: string;
  status: 'pending' | 'scraping' | 'analyzing' | 'generating' | 'completed' | 'failed';
}

export interface ProcessingStatus {
  companyId: string;
  currentStep: string;
  progress: number;
  error?: string;
}

export interface GTMResult {
  company: Company;
  scrapedData: any;
  schema: any;
  sampleData: any;
  generatedPrompt: {
    prompt: string;
    expectedDashboard: string;
    confidence: number;
    reasoning: string;
  };
}