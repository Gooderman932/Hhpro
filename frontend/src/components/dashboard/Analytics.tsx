/*
 * Analytics Dashboard Component
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import { useQuery } from '@tanstack/react-query'
import { getAnalyticsSummary, getRegionalAnalysis } from '../../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

interface AnalyticsSummary {
  sector_distribution?: Record<string, number>
}

interface RegionalData {
  regions?: Array<{
    state?: string
    project_count?: number
    total_value?: number
  }>
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

const Analytics = () => {
  const { 
    data: summary, 
    isLoading: summaryLoading, 
    isError: isSummaryError,
    error: summaryError 
  } = useQuery<AnalyticsSummary>({
    queryKey: ['analytics-summary'],
    queryFn: getAnalyticsSummary,
  })

  const { 
    data: regionalData, 
    isLoading: regionalLoading, 
    isError: isRegionalError,
    error: regionalError 
  } = useQuery<RegionalData>({
    queryKey: ['regional-analysis'],
    queryFn: getRegionalAnalysis,
  })

  // Safely extract sector data with fallbacks
  const sectorData = summary?.sector_distribution
    ? Object.entries(summary.sector_distribution).map(([name, value]) => ({
        name,
        value: Number(value),
      }))
    : []

  // Safely extract region data with fallbacks
  const regionData = regionalData?.regions
    ? regionalData.regions
        .slice(0, 10)
        .map((r: any) => ({
          state: r.state || 'Unknown',
          projects: r.project_count || 0,
          value: (r.total_value || 0) / 1000000, // Convert to millions
        }))
    : []

  // Handle both loading and error states for the entire dashboard
  if (summaryLoading || regionalLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="mt-2 text-gray-600">
            Market insights and trend analysis
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-center py-8 text-gray-500">Loading analytics data...</div>
        </div>
      </div>
    )
  }

  // Handle error states
  if (isSummaryError || isRegionalError) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="mt-2 text-gray-600">
            Market insights and trend analysis
          </p>
        </div>
        
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Data Loading Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>
                  {summaryError?.message || 'Failed to load summary data'} 
                  {regionalError && ' and '} 
                  {regionalError?.message || 'Failed to load regional data'}
                </p>
                <p className="mt-1">Please check your connection and try again.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="mt-2 text-gray-600">
          Market insights and trend analysis
        </p>
      </div>

      {/* Sector Distribution */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Sector Distribution</h2>
        {sectorData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sectorData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {sectorData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-8 text-gray-500">No sector data available</div>
        )}
      </div>

      {/* Regional Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Regions by Project Count</h2>
        {regionData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={regionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="state" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="projects" fill="#3B82F6" name="Project Count" />
              <Bar yAxisId="right" dataKey="value" fill="#10B981" name="Value ($M)" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-8 text-gray-500">No regional data available</div>
        )}
      </div>
    </div>
  )
}

export default Analytics
        
