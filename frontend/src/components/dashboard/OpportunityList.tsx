import { useQuery } from '@tanstack/react-query'
import { getProjects } from '../../services/api'
import DataTable from '../common/DataTable'
import type { Project } from '../../types'
import { useState } from 'react'

const OpportunityList = () => {
  // Add error state tracking
  const [error, setError] = useState<string | null>(null)
  
  const { 
    data: projects, 
    isLoading, 
    isError, 
    error: queryError 
  } = useQuery({
    queryKey: ['opportunities'],
    queryFn: () => getProjects({ limit: 50 }),
    onError: (error) => {
      console.error('Failed to fetch projects:', error)
      setError('Failed to load project data. Please try again later.')
    }
  })

  const formatCurrency = (value: number | null | undefined) => {
    // Handle all null/undefined cases explicitly
    if (value === null || value === undefined || isNaN(value)) return '-'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const columns = [
    {
      key: 'title',
      header: 'Project',
      render: (value: string) => (
        <div className="font-medium text-gray-900">{value}</div>
      ),
    },
    {
      key: 'sector',
      header: 'Sector',
      render: (value: string | null | undefined) => {
        if (!value) return '-'
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {value}
          </span>
        )
      },
    },
    {
      key: 'project_type',
      header: 'Type',
    },
    {
      key: 'city',
      header: 'Location',
      render: (_: any, row: Project) => {
        // Safely handle potential null/undefined values
        if (row.city && row.state) {
          return `${row.city}, ${row.state}`
        }
        return row.city || row.state || '-'
      },
    },
    {
      key: 'value',
      header: 'Value',
      render: (value: number | null | undefined) => (
        <span className="font-medium">{formatCurrency(value)}</span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (value: string) => {
        // Add validation to prevent crashes
        if (!value) return '-'
        return (
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            value === 'active'
              ? 'bg-green-100 text-green-800'
              : value === 'awarded'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-gray-100 text-gray-800'
          }`}>
            {value}
          </span>
        )
      },
    },
  ]

  if (isLoading) {
    return <div className="text-center py-8">Loading opportunities...</div>
  }

  if (isError) {
    return (
      <div className="text-center py-8 text-red-600">
        {error || 'Failed to load opportunities'}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Opportunities</h2>
      <DataTable 
        data={projects || []} 
        columns={columns}
      />
    </div>
  )
}

export default OpportunityList
