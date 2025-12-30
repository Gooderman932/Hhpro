import { useQuery } from '@tanstack/react-query'
import { getProjects } from '../../services/api'
import DataTable from '../common/DataTable'
import type { Project } from '../../types'

const OpportunityList = () => {
  const { data: projects, isLoading } = useQuery({
    queryKey: ['opportunities'],
    queryFn: () => getProjects({ limit: 50 }),
  })

  const formatCurrency = (value: number | null) => {
    if (!value) return '-'
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
      render: (value: string | null) => (
        value ? (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {value}
          </span>
        ) : '-'
      ),
    },
    {
      key: 'project_type',
      header: 'Type',
    },
    {
      key: 'city',
      header: 'Location',
      render: (_: any, row: Project) => {
        if (row.city && row.state) {
          return `${row.city}, ${row.state}`
        }
        return row.city || row.state || '-'
      },
    },
    {
      key: 'value',
      header: 'Value',
      render: (value: number | null) => (
        <span className="font-medium">{formatCurrency(value)}</span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (value: string) => (
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          value === 'active'
            ? 'bg-green-100 text-green-800'
            : value === 'awarded'
            ? 'bg-blue-100 text-blue-800'
            : 'bg-gray-100 text-gray-800'
        }`}>
          {value}
        </span>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Opportunities</h1>
        <p className="mt-2 text-gray-600">
          Browse and analyze construction opportunities
        </p>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">All Projects</h2>
        </div>
        <DataTable
          data={projects || []}
          columns={columns}
          loading={isLoading}
        />
      </div>
    </div>
  )
}

export default OpportunityList
