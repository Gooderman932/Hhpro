import { useState, useEffect } from 'react'
import { History, Loader2, AlertCircle, Target, TrendingUp, BarChart3 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { 
  getWinProbability, 
  getDemandForecast, 
  scoreProject,
  getProjectsList,
  getCurrentSubscription 
} from '../../services/api'

interface PredictionRecord {
  id: string
  type: 'win_probability' | 'demand_forecast' | 'opportunity_score'
  projectId?: number
  projectTitle?: string
  sector?: string
  region?: string
  result: any
  timestamp: Date
}

export const PredictionHistory = () => {
  const [subscription, setSubscription] = useState<any>(null)
  const [history, setHistory] = useState<PredictionRecord[]>([])
  const [projects, setProjects] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Form state
  const [predictionType, setPredictionType] = useState<string>('win_probability')
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [sector, setSector] = useState('Commercial')
  const [region, setRegion] = useState('TX')

  useEffect(() => {
    loadInitialData()
    // Load history from localStorage
    const saved = localStorage.getItem('prediction_history')
    if (saved) {
      setHistory(JSON.parse(saved))
    }
  }, [])

  const loadInitialData = async () => {
    try {
      const [sub, proj] = await Promise.all([
        getCurrentSubscription(),
        getProjectsList(20)
      ])
      setSubscription(sub)
      setProjects(proj)
    } catch (err) {
      setError('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const runPrediction = async () => {
    setRunning(true)
    setError(null)

    try {
      let result: any
      let record: PredictionRecord

      if (predictionType === 'win_probability' && selectedProject) {
        result = await getWinProbability(selectedProject)
        const project = projects.find(p => p.id === selectedProject)
        record = {
          id: `wp-${Date.now()}`,
          type: 'win_probability',
          projectId: selectedProject,
          projectTitle: project?.title || `Project ${selectedProject}`,
          result,
          timestamp: new Date()
        }
      } else if (predictionType === 'demand_forecast') {
        result = await getDemandForecast(sector, region, 6)
        record = {
          id: `df-${Date.now()}`,
          type: 'demand_forecast',
          sector,
          region,
          result,
          timestamp: new Date()
        }
      } else if (predictionType === 'opportunity_score' && selectedProject) {
        result = await scoreProject(selectedProject)
        const project = projects.find(p => p.id === selectedProject)
        record = {
          id: `os-${Date.now()}`,
          type: 'opportunity_score',
          projectId: selectedProject,
          projectTitle: project?.title || `Project ${selectedProject}`,
          result,
          timestamp: new Date()
        }
      } else {
        setError('Please select required options')
        setRunning(false)
        return
      }

      const newHistory = [record, ...history].slice(0, 50) // Keep last 50
      setHistory(newHistory)
      localStorage.setItem('prediction_history', JSON.stringify(newHistory))
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed')
    } finally {
      setRunning(false)
    }
  }

  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('prediction_history')
  }

  const canAccess = subscription && ['professional', 'enterprise'].includes(subscription.tier_id)
  const isEnterprise = subscription?.tier_id === 'enterprise'

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  if (!canAccess) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <CardTitle className="text-white">Professional Subscription Required</CardTitle>
              <CardDescription className="text-slate-400">
                Prediction history tracking requires Professional or Enterprise subscription.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button 
                className="bg-purple-600 hover:bg-purple-700"
                onClick={() => window.location.href = '/pricing'}
              >
                Upgrade Now
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
            <h1 className="text-3xl font-bold text-white">Prediction History</h1>
            <p className="text-slate-400 mt-1">Track and review your ML predictions</p>
          </div>
          {history.length > 0 && (
            <Button 
              variant="outline" 
              className="border-slate-600 text-slate-300"
              onClick={clearHistory}
            >
              Clear History
            </Button>
          )}
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* New Prediction Form */}
        <Card className="bg-slate-900 border-slate-700 mb-8">
          <CardHeader>
            <CardTitle className="text-white">Run New Prediction</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4">
              <select
                className="p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                value={predictionType}
                onChange={(e) => setPredictionType(e.target.value)}
                data-testid="prediction-type-select"
              >
                <option value="win_probability">Win Probability</option>
                <option value="demand_forecast">Demand Forecast</option>
                {isEnterprise && <option value="opportunity_score">Opportunity Score</option>}
              </select>

              {(predictionType === 'win_probability' || predictionType === 'opportunity_score') && (
                <select
                  className="p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                  value={selectedProject || ''}
                  onChange={(e) => setSelectedProject(Number(e.target.value))}
                >
                  <option value="">Select project...</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>{p.title}</option>
                  ))}
                </select>
              )}

              {predictionType === 'demand_forecast' && (
                <>
                  <select
                    className="p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                    value={sector}
                    onChange={(e) => setSector(e.target.value)}
                  >
                    <option value="Commercial">Commercial</option>
                    <option value="Residential">Residential</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Infrastructure">Infrastructure</option>
                  </select>
                  <select
                    className="p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                    value={region}
                    onChange={(e) => setRegion(e.target.value)}
                  >
                    <option value="TX">Texas</option>
                    <option value="FL">Florida</option>
                    <option value="CA">California</option>
                    <option value="AZ">Arizona</option>
                    <option value="AL">Alabama</option>
                    <option value="AK">Alaska</option>
                    <option value="AR">Arkansas</option>
                    <option value="CO">Colorado</option>
                    <option value="CT">Connecticut</option>
                    <option value="DE">Delaware</option>
                    <option value="DC">Washington DC</option>
                    <option value="GA">Georgia</option>
                    <option value="HI">Hawaii</option>
                    <option value="ID">Idaho</option>
                    <option value="IL">Illinois</option>
                    <option value="IN">Indiana</option>
                    <option value="IA">Iowa</option>
                    <option value="KS">Kansas</option>
                    <option value="KY">Kentucky</option>
                    <option value="LA">Louisiana</option>
                    <option value="ME">Maine</option>
                    <option value="MD">Maryland</option>
                    <option value="MA">Massachusetts</option>
                    <option value="MI">Michigan</option>
                    <option value="MN">Minnesota</option>
                    <option value="MS">Mississippi</option>
                    <option value="MO">Missouri</option>
                    <option value="MT">Montana</option>
                    <option value="NE">Nebraska</option>
                    <option value="NV">Nevada</option>
                    <option value="NH">New Hampshire</option>
                    <option value="NJ">New Jersey</option>
                    <option value="NM">New Mexico</option>
                    <option value="NY">New York</option>
                    <option value="NC">North Carolina</option>
                    <option value="ND">North Dakota</option>
                    <option value="OH">Ohio</option>
                    <option value="OK">Oklahoma</option>
                    <option value="OR">Oregon</option>
                    <option value="PA">Pennsylvania</option>
                    <option value="RI">Rhode Island</option>
                    <option value="SC">South Carolina</option>
                    <option value="SD">South Dakota</option>
                    <option value="TN">Tennessee</option>
                    <option value="UT">Utah</option>
                    <option value="VT">Vermont</option>
                    <option value="VA">Virginia</option>
                    <option value="WA">Washington</option>
                    <option value="WV">West Virginia</option>
                    <option value="WI">Wisconsin</option>
                    <option value="WY">Wyoming</option>
                    <option value="PR">Puerto Rico</option>
                    <option value="GU">Guam</option>
                    <option value="VI">US Virgin Islands</option>
                    <option value="AS">American Samoa</option>
                    <option value="MP">N. Mariana Islands</option>
                  </select>
                </>
              )}

              <Button 
                onClick={runPrediction}
                className="bg-blue-600 hover:bg-blue-700"
                disabled={running}
                data-testid="run-prediction-btn"
              >
                {running ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Run Prediction'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* History List */}
        {history.length > 0 ? (
          <div className="space-y-4">
            {history.map((record) => (
              <Card key={record.id} className="bg-slate-900 border-slate-700" data-testid={`history-${record.id}`}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      {record.type === 'win_probability' && (
                        <div className="p-2 rounded-lg bg-green-500/20">
                          <Target className="h-5 w-5 text-green-400" />
                        </div>
                      )}
                      {record.type === 'demand_forecast' && (
                        <div className="p-2 rounded-lg bg-blue-500/20">
                          <TrendingUp className="h-5 w-5 text-blue-400" />
                        </div>
                      )}
                      {record.type === 'opportunity_score' && (
                        <div className="p-2 rounded-lg bg-amber-500/20">
                          <BarChart3 className="h-5 w-5 text-amber-400" />
                        </div>
                      )}
                      <div>
                        <h3 className="font-semibold text-white">
                          {record.type === 'win_probability' && `Win Probability: ${record.projectTitle}`}
                          {record.type === 'demand_forecast' && `Demand Forecast: ${record.sector} / ${record.region}`}
                          {record.type === 'opportunity_score' && `Opportunity Score: ${record.projectTitle}`}
                        </h3>
                        <p className="text-slate-400 text-sm">
                          {new Date(record.timestamp).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      {record.type === 'win_probability' && (
                        <div className="text-2xl font-bold text-green-400">
                          {(record.result.win_probability * 100).toFixed(1)}%
                        </div>
                      )}
                      {record.type === 'demand_forecast' && (
                        <div className="text-lg font-semibold text-blue-400">
                          {record.result.trend} {record.result.trend_percentage > 0 ? '+' : ''}{record.result.trend_percentage}%
                        </div>
                      )}
                      {record.type === 'opportunity_score' && (
                        <div>
                          <div className="text-2xl font-bold text-amber-400">
                            {(record.result.overall_score * 100).toFixed(0)}
                          </div>
                          <div className="text-sm text-slate-400">
                            {record.result.recommendation?.action}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-12 text-center">
              <History className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No prediction history yet. Run a prediction to get started.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default PredictionHistory
