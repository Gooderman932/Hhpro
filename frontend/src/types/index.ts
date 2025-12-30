/*
 * TypeScript Type Definitions
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

export interface Project {
  id: number
  title: string
  description: string | null
  project_type: string
  sector: string | null
  status: string
  value: number | null
  city: string | null
  state: string | null
  created_at: string
}

export interface Company {
  id: number
  name: string
  company_type: string
  industry: string | null
  city: string | null
  state: string | null
}

export interface OpportunityScore {
  id: number
  project_id: number
  overall_score: number
  value_score: number
  fit_score: number
  competition_score: number
  timing_score: number
  risk_score: number
}

export interface AnalyticsSummary {
  total_projects: number
  active_projects: number
  total_value: number
  sector_distribution: Record<string, number>
}

export interface Competitor {
  id: number
  name: string
  company_type: string
  project_count: number
  wins: number
  win_rate: number
}

export interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  tenant_id: number
}

export interface AuthToken {
  access_token: string
  token_type: string
}
