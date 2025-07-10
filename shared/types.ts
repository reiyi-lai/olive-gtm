export interface Company {
  id: string;
  name: string;
  website: string;
  industry?: string;
  status: 'pending' | 'scraping' | 'analyzing' | 'generating' | 'completed' | 'failed';
}

export interface ScrapedData {
  company: Company;
  websiteContent: string;
  businessType: string;
  keyFeatures: string[];
  description: string;
  timestamp: string;
}

export interface DatabaseTable {
  name: string;
  columns: DatabaseColumn[];
  primaryKey: string;
  description: string;
}

export interface DatabaseColumn {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'date' | 'json';
  nullable: boolean;
  description: string;
}

export interface DatabaseRelationship {
  fromTable: string;
  fromColumn: string;
  toTable: string;
  toColumn: string;
  type: 'one-to-one' | 'one-to-many' | 'many-to-many' | 'many-to-one';
}

export interface DatabaseSchema {
  tables: DatabaseTable[];
  relationships: DatabaseRelationship[];
  description: string;
}

export interface SampleData {
  [tableName: string]: Record<string, any>[];
}

export interface GeneratedPrompt {
  prompt: string;
  expectedDashboard: string;
  confidence: number;
  reasoning: string;
}

export interface GTMResult {
  company: Company;
  scrapedData: ScrapedData;
  schema: DatabaseSchema;
  sampleData: SampleData;
  generatedPrompt: GeneratedPrompt;
}

export interface ProcessingStatus {
  companyId: string;
  currentStep: string;
  progress: number;
  error?: string;
}