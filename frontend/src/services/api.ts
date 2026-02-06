/*
 * API Service - Backend Communication Layer
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import axios from 'axios'
import type { Project, AnalyticsSummary, Competitor, AuthToken, User } from '../types'
import type { PricingTier, CheckoutResponse, PaymentStatus, Subscription } from '../types/subscription'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Authentication
export const login = async (email: string, password: string): Promise<AuthToken> => {
  const response = await api.post<AuthToken>('/auth/token', {
    username: email,
    password: password
  })
  return response.data
}

export const register = async (email: string, password: string, fullName: string): Promise<User> => {
  const response = await api.post<User>('/auth/register', {
    email,
    password,
    full_name: fullName
  })
  return response.data
}

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>('/auth/me')
  return response.data
}

// Projects
export const getProjects = async (params?: {
  skip?: number
  limit?: number
  sector?: string
  status?: string
}): Promise<Project[]> => {
  const response = await api.get<Project[]>('/projects/', { params })
  return response.data
}

export const getProject = async (id: number): Promise<Project> => {
  const response = await api.get<Project>(`/projects/${id}`)
  return response.data
}

export const createProject = async (data: Partial<Project>): Promise<Project> => {
  const response = await api.post<Project>('/projects/', data)
  return response.data
}

// Analytics
export const getAnalyticsSummary = async (): Promise<AnalyticsSummary> => {
  const response = await api.get<AnalyticsSummary>('/analytics/summary')
  return response.data
}

export const getProjectTrends = async (days: number = 30) => {
  const response = await api.get('/analytics/trends', { params: { days } })
  return response.data
}

export const getRegionalAnalysis = async () => {
  const response = await api.get('/analytics/regions')
  return response.data
}

// Intelligence
export const getCompetitors = async (limit: number = 10): Promise<Competitor[]> => {
  const response = await api.get<Competitor[]>('/intelligence/competitors', {
    params: { limit },
  })
  return response.data
}

export const getMarketShare = async (sector?: string) => {
  const response = await api.get('/intelligence/market-share', {
    params: sector ? { sector } : {},
  })
  return response.data
}

export const getRelationshipGraph = async (companyId: number) => {
  const response = await api.get('/intelligence/relationships', {
    params: { company_id: companyId },
  })
  return response.data
}

// Pricing & Subscriptions
export const getPricingTiers = async (): Promise<PricingTier[]> => {
  const response = await api.get<PricingTier[]>('/pricing/tiers')
  return response.data
}

export const createCheckoutSession = async (tierId: string): Promise<CheckoutResponse> => {
  const originUrl = window.location.origin
  const response = await api.post<CheckoutResponse>('/subscriptions/checkout', {
    tier_id: tierId,
    origin_url: originUrl
  })
  return response.data
}

export const getPaymentStatus = async (sessionId: string): Promise<PaymentStatus> => {
  const response = await api.get<PaymentStatus>(`/subscriptions/status/${sessionId}`)
  return response.data
}

export const getCurrentSubscription = async (): Promise<Subscription | null> => {
  const response = await api.get<Subscription | null>('/subscriptions/current')
  return response.data
}

// ML Predictions
export const getWinProbability = async (projectId: number) => {
  const response = await api.get(`/predictions/win-probability/${projectId}`)
  return response.data
}

export const getDemandForecast = async (sector: string, region: string, months: number = 6) => {
  const response = await api.get('/predictions/demand-forecast', {
    params: { sector, region, months }
  })
  return response.data
}

export const getRegionalOutlook = async () => {
  const response = await api.get('/predictions/regional-outlook')
  return response.data
}

// Opportunity Scoring (Enterprise)
export const scoreProject = async (projectId: number) => {
  const response = await api.get(`/scoring/project/${projectId}`)
  return response.data
}

export const batchScoreProjects = async (limit: number = 20) => {
  const response = await api.get('/scoring/batch', { params: { limit } })
  return response.data
}

// Projects list
export const getProjectsList = async (limit: number = 50) => {
  const response = await api.get('/projects', { params: { limit } })
  return response.data
}

// Notifications
export interface NotificationPreferences {
  email_enabled: boolean
  frequency: string
  min_project_value: number
  preferred_sectors: string[]
  preferred_regions: string[]
  match_type: string
  last_notified_at?: string | null
}

export const getNotificationPreferences = async (): Promise<NotificationPreferences> => {
  const response = await api.get<NotificationPreferences>('/notifications/preferences')
  return response.data
}

export const updateNotificationPreferences = async (prefs: Partial<NotificationPreferences>) => {
  const response = await api.put('/notifications/preferences', prefs)
  return response.data
}

export const getNotificationOptions = async () => {
  const response = await api.get('/notifications/options')
  return response.data
}

export const sendTestNotification = async () => {
  const response = await api.post('/notifications/test')
  return response.data
}

export const getNotificationHistory = async (limit: number = 20) => {
  const response = await api.get('/notifications/history', { params: { limit } })
  return response.data
}

// User Profile
export interface UserProfile {
  onboarding_completed: boolean
  business_type: string | null
  trade_specialty: string | null
  company_size: string | null
  service_states: string[]
  service_cities: string[]
  service_radius_miles: number
  min_project_value: number
  max_project_value: number
  preferred_sectors: string[]
  saved_searches: any[]
}

export const getProfile = async (): Promise<UserProfile> => {
  const response = await api.get<UserProfile>('/profile')
  return response.data
}

export const updateProfile = async (profile: Partial<UserProfile>) => {
  const response = await api.put('/profile', profile)
  return response.data
}

// Permits
export const getPermits = async (params: {
  state?: string
  permit_type?: string
  min_value?: number
  max_value?: number
  limit?: number
}) => {
  const response = await api.get('/permits', { params })
  return response.data
}

// My Projects
export const getMyProjects = async () => {
  const response = await api.get('/my-projects')
  return response.data
}

export const createMyProject = async (project: any) => {
  const response = await api.post('/my-projects', project)
  return response.data
}

export const deleteMyProject = async (id: number) => {
  const response = await api.delete(`/my-projects/${id}`)
  return response.data
}

// Tracked Competitors
export const getMyCompetitors = async () => {
  const response = await api.get('/my-competitors')
  return response.data
}

export const addCompetitor = async (competitor: any) => {
  const response = await api.post('/my-competitors', competitor)
  return response.data
}

// Economic Indicators
export const getEconomicIndicators = async () => {
  const response = await api.get('/economic-indicators')
  return response.data
}

// Industry Benchmarks
export const getBenchmarks = async () => {
  const response = await api.get('/benchmarks')
  return response.data
}

// Smart Alerts
export const getAlerts = async (unreadOnly: boolean = false) => {
  const response = await api.get('/alerts', { params: { unread_only: unreadOnly } })
  return response.data
}

export const generateAlerts = async () => {
  const response = await api.post('/alerts/generate')
  return response.data
}

// AI Enrichment
export const enrichProject = async (projectData: any) => {
  const response = await api.post('/ai/enrich-project', projectData)
  return response.data
}

export const matchOpportunities = async (limit: number = 20) => {
  const response = await api.get('/ai/match-opportunities', { params: { limit } })
  return response.data
}

// Tier Features
export const getTierFeatures = async () => {
  const response = await api.get('/tier-features')
  return response.data
}

// ============================================
// Proprietary ML Model Endpoints
// © 2025 Poor Dude Holdings LLC
// ============================================

export const getMLModelsInfo = async () => {
  const response = await api.get('/ml/models-info')
  return response.data
}

export const getMLWinProbability = async (projectId?: number, project?: any) => {
  const response = await api.post('/ml/win-probability', {
    project_id: projectId,
    project
  })
  return response.data
}

export const getMLDemandForecast = async (region: string, sector: string, months: number = 6) => {
  const response = await api.post('/ml/demand-forecast', {
    region, sector, months_ahead: months
  })
  return response.data
}

export const getMLRegionalOutlook = async (sector: string = 'Commercial') => {
  const response = await api.get('/ml/regional-outlook', { params: { sector } })
  return response.data
}

export const getMLCompetitiveAnalysis = async (competitorId?: number, competitor?: any) => {
  const response = await api.post('/ml/competitive-analysis', {
    competitor_id: competitorId,
    competitor
  })
  return response.data
}

export const getMLCompetitiveLandscape = async () => {
  const response = await api.get('/ml/competitive-landscape')
  return response.data
}

export const getMLProjectMatching = async (minScore: number = 0, limit: number = 20) => {
  const response = await api.post('/ml/project-matching', {
    min_score: minScore, limit
  })
  return response.data
}

export default api
