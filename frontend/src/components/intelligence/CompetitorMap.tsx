import { useQuery } from '@tanstack/react-query'
import { getCompetitors } from '../../services/api'
import { Loader2, AlertCircle, Users } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'

interface Competitor {
  name: string
  company_type?: string
  market_share?: number
  win_rate?: number
  project_count?: number
  wins?: number
}

interface CompetitorResponse {
  competitors: Competitor[]
  subscription_tier?: string
}

const CompetitorMap = () => {
  const { 
    data: competitorData, 
    isLoading, 
    isError, 
    error 
  } = useQuery<CompetitorResponse>({
    queryKey: ['competitors'],
    queryFn: async () => {
      const response = await getCompetitors(20)
      // Handle both array and object responses
      if (Array.isArray(response)) {
        return { competitors: response }
      }
      return response as CompetitorResponse
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  if (isError) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <CardTitle className="text-white">Error Loading Data</CardTitle>
              <CardDescription className="text-slate-400">
                {error?.message || 'Failed to load competitor data. Professional subscription may be required.'}
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  const competitors = competitorData?.competitors || []

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Competitor Intelligence</h1>
          <p className="mt-2 text-slate-400">
            Track and analyze competitor activity in the market
          </p>
        </div>

        <Card className="bg-slate-900 border-slate-700" data-testid="competitors-card">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Users className="h-5 w-5 text-purple-500" />
              Top Competitors
            </CardTitle>
            <CardDescription className="text-slate-400">
              Market share and win rate analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            {competitors.length > 0 ? (
              <div className="space-y-4">
                {competitors.map((competitor, index) => (
                  <div 
                    key={index}
                    className="flex items-center justify-between p-4 bg-slate-800 rounded-lg"
                    data-testid={`competitor-${index}`}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-purple-600/20 flex items-center justify-center text-purple-400 font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <div className="font-semibold text-white">{competitor.name}</div>
                        <div className="text-sm text-slate-400">
                          {competitor.company_type || 'Contractor'}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      {competitor.market_share !== undefined && (
                        <div className="text-center">
                          <div className="text-lg font-semibold text-blue-400">
                            {competitor.market_share.toFixed(1)}%
                          </div>
                          <div className="text-xs text-slate-400">Market Share</div>
                        </div>
                      )}
                      {competitor.win_rate !== undefined && (
                        <div className="text-center">
                          <div className="text-lg font-semibold text-green-400">
                            {(competitor.win_rate * 100).toFixed(0)}%
                          </div>
                          <div className="text-xs text-slate-400">Win Rate</div>
                        </div>
                      )}
                      {competitor.project_count !== undefined && (
                        <div className="text-center">
                          <div className="text-lg font-semibold text-amber-400">
                            {competitor.project_count}
                          </div>
                          <div className="text-xs text-slate-400">Projects</div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500">
                No competitor data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default CompetitorMap
