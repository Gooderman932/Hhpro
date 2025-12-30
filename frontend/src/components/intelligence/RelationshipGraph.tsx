import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getRelationshipGraph } from '../../services/api'

const RelationshipGraph = () => {
  const [companyId, setCompanyId] = useState<number>(1)

  const { data: graphData, isLoading } = useQuery({
    queryKey: ['relationship-graph', companyId],
    queryFn: () => getRelationshipGraph(companyId),
    enabled: !!companyId,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Relationship Graph</h1>
        <p className="mt-2 text-gray-600">
          Visualize business relationships and project networks
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-4">
          <label htmlFor="companyId" className="block text-sm font-medium text-gray-700 mb-2">
            Select Company ID
          </label>
          <input
            type="number"
            id="companyId"
            value={companyId}
            onChange={(e) => setCompanyId(Number(e.target.value))}
            className="block w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {isLoading ? (
          <div className="text-center py-12 text-gray-500">Loading...</div>
        ) : graphData && graphData.company ? (
          <div className="space-y-6">
            <div className="border-b pb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {graphData.company.name}
              </h3>
              <p className="text-sm text-gray-600 mt-1">Company ID: {graphData.company.id}</p>
            </div>

            <div>
              <h4 className="text-md font-medium text-gray-900 mb-4">Connected Companies</h4>
              {graphData.relationships && graphData.relationships.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {graphData.relationships.map((rel: any) => (
                    <div
                      key={rel.company_id}
                      className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                    >
                      <h5 className="font-medium text-gray-900">{rel.company_name}</h5>
                      <p className="text-sm text-gray-600 mt-1">
                        {rel.shared_projects} shared project{rel.shared_projects !== 1 ? 's' : ''}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No relationships found</p>
              )}
            </div>
          </div>
        ) : graphData?.error ? (
          <div className="text-center py-12 text-red-500">{graphData.error}</div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            Enter a company ID to view relationships
          </div>
        )}
      </div>
    </div>
  )
}

export default RelationshipGraph
