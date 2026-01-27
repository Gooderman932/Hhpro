import { useQuery } from '@tanstack/react-query'
import { getCompetitors } from '../../services/api'
import DataTable from '../common/DataTable'
import type { Competitor } from '../../types'

const CompetitorMap = () => {
  const { 
    data: competitors, 
    isLoading, 
    isError, 
    error 
  } = useQuery<Competitor[]>({
    queryKey: ['competitors'],
    queryFn: () => getCompetitors(20),
  })

  if (isError) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Competitor Intelligence</h1>
          <p className="mt-2 text-gray-600">
            Track and analyze competitor activity in the market
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
              <h3 className="text-sm font-medium text-red-800">{error?.message || 'Failed to load competitor data'}</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>Please check your connection and try again.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const columns = [
    {
      key: 'name',
      header: 'Company',
      render: (value: string) => (
        <div className="font-medium text-gray-900">{value}</div>
      ),
    },
    {
      key: 'company_type',
      header: 'Type',
      render: (value: string) => (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
          {value}
        </span>
      ),
    },
    {
      key: 'project_count',
      header: 'Projects',
    },
    {
      key: 'wins',
      header: 'Wins',
    },
    {
      key: 'win_rate',
      header: 'Win Rate',
      render: (value: number) => (
        <div className="flex items-center">
          <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
            <div
              className="bg-green-500 h-2 rounded-full"
              style={{ width: `${value * 100}%` }}
            />
          </div>
          <span className="text-sm font-medium">{(value * 100).toFixed(0)}%</span>
        </div>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Competitor Intelligence</h1>
        <p className="mt-2 text-gray-600">
          Track and analyze competitor activity in the market
        </p>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Top Competitors</h2>
        </div>
        <DataTable
          data={competitors || []} // Safely fallback to empty array
          columns={columns}
          loading={isLoading}
        />
      </div>
    </div>
  )
}

export default CompetitorMap
