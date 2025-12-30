import { useQuery } from '@tanstack/react-query'
import { getCompetitors } from '../../services/api'
import DataTable from '../common/DataTable'
import type { Competitor } from '../../types'

const CompetitorMap = () => {
  const { data: competitors, isLoading } = useQuery({
    queryKey: ['competitors'],
    queryFn: () => getCompetitors(20),
  })

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
          data={competitors || []}
          columns={columns}
          loading={isLoading}
        />
      </div>
    </div>
  )
}

export default CompetitorMap
