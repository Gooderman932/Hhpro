/*
 * API Service - Backend Communication Layer
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import axios from 'axios'
import type { Project, AnalyticsSummary, Competitor, AuthToken, User } from '../types'

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
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)
  
  const response = await api.post<AuthToken>('/auth/token', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
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

export default api
