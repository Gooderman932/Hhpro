/*
 * Analytics Dashboard Component
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import { useQuery } from '@tanstack/react-query'
import { getAnalyticsSummary, getRegionalAnalysis } from '../../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

const Analytics = () => {
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: getAnalyticsSummary,
  })

  const { data: regionalData, isLoading: regionalLoading } = useQuery({
    queryKey: ['regional-analysis'],
    queryFn: getRegionalAnalysis,
  })

  const sectorData = summary?.sector_distribution
    ? Object.entries(summary.sector_distribution).map(([name, value]) => ({
        name,
        value,
      }))
    : []

  const regionData = regionalData?.regions
    ? regionalData.regions.slice(0, 10).map((r: any) => ({
        state: r.state,
        projects: r.project_count,
        value: r.total_value / 1000000, // Convert to millions
      }))
    : []

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
        {summaryLoading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : sectorData.length > 0 ? (
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
                {sectorData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-8 text-gray-500">No data available</div>
        )}
      </div>

      {/* Regional Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Top Regions by Project Count</h2>
        {regionalLoading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : regionData.length > 0 ? (
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
          <div className="text-center py-8 text-gray-500">No data available</div>
        )}
      </div>
    </div>
  )
}

export default Analytics
