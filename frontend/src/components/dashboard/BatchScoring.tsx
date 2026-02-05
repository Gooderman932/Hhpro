import { useState, useEffect } from 'react'
import { ListChecks, AlertCircle, Loader2, ArrowUpDown, CheckCircle, XCircle, MinusCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { batchScoreProjects, getCurrentSubscription } from '../../services/api'

interface ScoredProject {
  project_id: number
  project_title: string
  project_value: number
  project_sector: string
  project_location: string
  overall_score: number
  scores: {
    value: number
    fit: number
    competition: number
    timing: number
    risk: number
  }
  recommendation: {
    action: string
    priority: string
    description: string
  }
}

export const BatchScoring = () => {
  const [subscription, setSubscription] = useState<any>(null)
  const [scoredProjects, setScoredProjects] = useState<ScoredProject[]>([])
  const [loading, setLoading] = useState(true)
  const [scoring, setScoring] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [limit, setLimit] = useState(10)

  useEffect(() => {
    checkSubscription()
  }, [])

  const checkSubscription = async () => {
    try {
      const sub = await getCurrentSubscription()
      setSubscription(sub)
    } catch (err) {
      setError('Failed to check subscription')
    } finally {
      setLoading(false)
    }
  }

  const runBatchScoring = async () => {
    setScoring(true)
    setError(null)
    try {
      const results = await batchScoreProjects(limit)
      setScoredProjects(results)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to score projects')
    } finally {
      setScoring(false)
    }
  }

  const getActionColor = (action: string) => {
    switch (action) {
      case 'PURSUE': return 'text-green-400 bg-green-400/10'
      case 'EVALUATE': return 'text-blue-400 bg-blue-400/10'
      case 'CONSIDER': return 'text-yellow-400 bg-yellow-400/10'
      case 'PASS': return 'text-red-400 bg-red-400/10'
      default: return 'text-slate-400 bg-slate-400/10'
    }
  }

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'PURSUE': return <CheckCircle className="h-4 w-4" />
      case 'EVALUATE': return <ArrowUpDown className="h-4 w-4" />
      case 'CONSIDER': return <MinusCircle className="h-4 w-4" />
      case 'PASS': return <XCircle className="h-4 w-4" />
      default: return null
    }
  }

  const isEnterprise = subscription?.tier_id === 'enterprise'

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  if (!isEnterprise) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <CardTitle className="text-white">Enterprise Subscription Required</CardTitle>
              <CardDescription className="text-slate-400">
                Batch opportunity scoring is available exclusively for Enterprise subscribers.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button 
                className="bg-amber-600 hover:bg-amber-700"
                onClick={() => window.location.href = '/pricing'}
              >
                Upgrade to Enterprise
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Batch Opportunity Scoring</h1>
            <p className="text-slate-400 mt-1">Score and rank multiple projects at once</p>
          </div>
          <div className="flex items-center gap-3">
            <select
              className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
            >
              <option value={10}>Top 10</option>
              <option value={20}>Top 20</option>
              <option value={50}>Top 50</option>
            </select>
            <Button 
              onClick={runBatchScoring}
              className="bg-amber-600 hover:bg-amber-700"
              disabled={scoring}
              data-testid="run-batch-scoring-btn"
            >
              {scoring ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Scoring...
                </>
              ) : (
                <>
                  <ListChecks className="h-4 w-4 mr-2" />
                  Run Batch Score
                </>
              )}
            </Button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {scoredProjects.length > 0 ? (
          <div className="space-y-4">
            {scoredProjects.map((project, index) => (
              <Card 
                key={project.project_id} 
                className="bg-slate-900 border-slate-700"
                data-testid={`scored-project-${project.project_id}`}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-lg font-bold text-white">
                        {index + 1}
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-white">{project.project_title}</h3>
                        <p className="text-slate-400 text-sm">
                          {project.project_sector} • {project.project_location} • ${(project.project_value / 1000000).toFixed(1)}M
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-white">
                        {(project.overall_score * 100).toFixed(0)}
                      </div>
                      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded text-sm font-medium ${getActionColor(project.recommendation.action)}`}>
                        {getActionIcon(project.recommendation.action)}
                        {project.recommendation.action}
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 grid grid-cols-5 gap-2">
                    {Object.entries(project.scores).map(([key, value]) => (
                      <div key={key} className="bg-slate-800 p-2 rounded text-center">
                        <div className="text-xs text-slate-400 capitalize">{key}</div>
                        <div className="text-sm font-semibold text-white">{(value * 100).toFixed(0)}</div>
                      </div>
                    ))}
                  </div>

                  <p className="mt-3 text-sm text-slate-400">
                    {project.recommendation.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-12 text-center">
              <ListChecks className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">Click "Run Batch Score" to analyze and rank your projects</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default BatchScoring
