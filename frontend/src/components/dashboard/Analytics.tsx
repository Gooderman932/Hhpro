/*
 * Analytics Dashboard Component
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import { useQuery } from '@tanstack/react-query'
import { getAnalyticsSummary, getRegionalAnalysis } from '../../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Loader2, AlertCircle, PieChart as PieChartIcon, MapPin } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { OnboardingWizard } from '../onboarding/OnboardingWizard'

interface AnalyticsSummary {
  sector_distribution?: Record<string, number>
  total_projects?: number
  total_value?: number
  subscription_tier?: string
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
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  // Handle error states
  if (isSummaryError || isRegionalError) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <CardTitle className="text-white">Error Loading Data</CardTitle>
              <CardDescription className="text-slate-400">
                {summaryError?.message || regionalError?.message || 'Failed to load analytics data'}
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Analytics Dashboard</h1>
          <p className="mt-2 text-slate-400">
            Market insights and trend analysis
          </p>
        </div>

        {/* Onboarding Wizard */}
        <OnboardingWizard />

        {/* Summary Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-400">{summary?.total_projects || 0}</div>
                <div className="text-slate-400 mt-1">Total Projects</div>
              </div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-400">
                  ${((summary?.total_value || 0) / 1000000).toFixed(1)}M
                </div>
                <div className="text-slate-400 mt-1">Total Value</div>
              </div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-400 capitalize">
                  {summary?.subscription_tier || 'N/A'}
                </div>
                <div className="text-slate-400 mt-1">Your Plan</div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Sector Distribution */}
          <Card className="bg-slate-900 border-slate-700" data-testid="sector-distribution-card">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <PieChartIcon className="h-5 w-5 text-blue-500" />
                Sector Distribution
              </CardTitle>
              <CardDescription className="text-slate-400">
                Projects by industry sector
              </CardDescription>
            </CardHeader>
            <CardContent>
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
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                      labelStyle={{ color: '#fff' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-slate-500">No sector data available</div>
              )}
            </CardContent>
          </Card>

          {/* Regional Analysis */}
          <Card className="bg-slate-900 border-slate-700" data-testid="regional-analysis-card">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <MapPin className="h-5 w-5 text-green-500" />
                Top Regions
              </CardTitle>
              <CardDescription className="text-slate-400">
                Project count and value by state
              </CardDescription>
            </CardHeader>
            <CardContent>
              {regionData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={regionData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="state" stroke="#94a3b8" />
                    <YAxis yAxisId="left" stroke="#94a3b8" />
                    <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                      labelStyle={{ color: '#fff' }}
                    />
                    <Legend />
                    <Bar yAxisId="left" dataKey="projects" fill="#3B82F6" name="Projects" />
                    <Bar yAxisId="right" dataKey="value" fill="#10B981" name="Value ($M)" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-slate-500">No regional data available</div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Analytics
        
