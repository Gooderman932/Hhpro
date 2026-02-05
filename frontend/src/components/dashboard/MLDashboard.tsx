import { useState, useEffect } from 'react'
import { TrendingUp, Target, MapPin, Loader2, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { 
  getWinProbability, 
  getDemandForecast, 
  getRegionalOutlook,
  getProjectsList,
  getCurrentSubscription
} from '../../services/api'

interface Project {
  id: number
  title: string
  sector: string
  value: number
  city: string
  state: string
}

interface Forecast {
  date: string
  month: string
  predicted_demand: number
  confidence_lower: number
  confidence_upper: number
}

export const MLDashboard = () => {
  const [subscription, setSubscription] = useState<any>(null)
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [winPrediction, setWinPrediction] = useState<any>(null)
  const [demandForecast, setDemandForecast] = useState<any>(null)
  const [regionalOutlook, setRegionalOutlook] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [predictionLoading, setPredictionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Forecast params
  const [forecastSector, setForecastSector] = useState('Commercial')
  const [forecastRegion, setForecastRegion] = useState('TX')

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      const [sub, proj] = await Promise.all([
        getCurrentSubscription(),
        getProjectsList(20)
      ])
      setSubscription(sub)
      setProjects(proj)
      
      if (sub && ['professional', 'enterprise'].includes(sub.tier_id)) {
        const [forecast, outlook] = await Promise.all([
          getDemandForecast(forecastSector, forecastRegion, 6),
          getRegionalOutlook()
        ])
        setDemandForecast(forecast)
        setRegionalOutlook(outlook)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const loadWinProbability = async (projectId: number) => {
    setPredictionLoading(true)
    setSelectedProject(projectId)
    try {
      const result = await getWinProbability(projectId)
      setWinPrediction(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get prediction')
    } finally {
      setPredictionLoading(false)
    }
  }

  const refreshForecast = async () => {
    setPredictionLoading(true)
    try {
      const forecast = await getDemandForecast(forecastSector, forecastRegion, 6)
      setDemandForecast(forecast)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get forecast')
    } finally {
      setPredictionLoading(false)
    }
  }

  const canAccessPredictions = subscription && ['professional', 'enterprise'].includes(subscription.tier_id)

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  if (!canAccessPredictions) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <CardTitle className="text-white">Professional Subscription Required</CardTitle>
              <CardDescription className="text-slate-400">
                ML predictions are available for Professional and Enterprise subscribers.
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
        <h1 className="text-3xl font-bold text-white mb-8">ML Predictions Dashboard</h1>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Win Probability Section */}
          <Card className="bg-slate-900 border-slate-700" data-testid="win-probability-card">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Target className="h-5 w-5 text-green-500" />
                Win Probability Predictor
              </CardTitle>
              <CardDescription className="text-slate-400">
                Select a project to predict win likelihood
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <select
                  className="w-full p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                  value={selectedProject || ''}
                  onChange={(e) => loadWinProbability(Number(e.target.value))}
                  data-testid="project-select"
                >
                  <option value="">Select a project...</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.title} - ${(p.value / 1000000).toFixed(1)}M
                    </option>
                  ))}
                </select>

                {predictionLoading && (
                  <div className="flex justify-center py-8">
                    <Loader2 className="h-6 w-6 text-blue-500 animate-spin" />
                  </div>
                )}

                {winPrediction && !predictionLoading && (
                  <div className="space-y-4 pt-4">
                    <div className="text-center">
                      <div className="text-5xl font-bold text-green-400">
                        {(winPrediction.win_probability * 100).toFixed(1)}%
                      </div>
                      <div className="text-slate-400 mt-1">Win Probability</div>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-center">
                      <div className="bg-slate-800 p-3 rounded-lg">
                        <div className="text-2xl font-semibold text-blue-400">
                          {(winPrediction.confidence * 100).toFixed(0)}%
                        </div>
                        <div className="text-slate-400 text-sm">Confidence</div>
                      </div>
                      <div className="bg-slate-800 p-3 rounded-lg">
                        <div className="text-lg font-semibold text-purple-400">
                          v{winPrediction.model_version}
                        </div>
                        <div className="text-slate-400 text-sm">Model</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Demand Forecast Section */}
          <Card className="bg-slate-900 border-slate-700" data-testid="demand-forecast-card">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-blue-500" />
                Demand Forecast
              </CardTitle>
              <CardDescription className="text-slate-400">
                6-month demand projection by sector and region
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <select
                    className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm"
                    value={forecastSector}
                    onChange={(e) => setForecastSector(e.target.value)}
                  >
                    <option value="Commercial">Commercial</option>
                    <option value="Residential">Residential</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Infrastructure">Infrastructure</option>
                    <option value="Industrial">Industrial</option>
                  </select>
                  <select
                    className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm"
                    value={forecastRegion}
                    onChange={(e) => setForecastRegion(e.target.value)}
                  >
                    <option value="TX">Texas</option>
                    <option value="FL">Florida</option>
                    <option value="CA">California</option>
                    <option value="AZ">Arizona</option>
                    <option value="WA">Washington</option>
                  </select>
                </div>
                <Button 
                  onClick={refreshForecast} 
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  disabled={predictionLoading}
                >
                  {predictionLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Get Forecast'}
                </Button>

                {demandForecast && (
                  <div className="space-y-3 pt-2">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Trend:</span>
                      <span className={`font-semibold ${demandForecast.trend === 'increasing' ? 'text-green-400' : 'text-red-400'}`}>
                        {demandForecast.trend} ({demandForecast.trend_percentage > 0 ? '+' : ''}{demandForecast.trend_percentage}%)
                      </span>
                    </div>
                    <div className="space-y-2">
                      {demandForecast.forecasts?.slice(0, 4).map((f: Forecast, i: number) => (
                        <div key={i} className="flex justify-between items-center bg-slate-800 p-2 rounded">
                          <span className="text-slate-300 text-sm">{f.month}</span>
                          <span className="text-white font-medium">${(f.predicted_demand).toFixed(0)}M</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Regional Outlook */}
          <Card className="bg-slate-900 border-slate-700 lg:col-span-2" data-testid="regional-outlook-card">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <MapPin className="h-5 w-5 text-amber-500" />
                Regional Market Outlook
              </CardTitle>
              <CardDescription className="text-slate-400">
                Growth indicators by region
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-5 gap-4">
                {regionalOutlook.map((region, i) => (
                  <div 
                    key={i} 
                    className="bg-slate-800 p-4 rounded-lg text-center"
                  >
                    <div className="text-2xl font-bold text-white">{region.region}</div>
                    <div className={`text-sm font-medium mt-1 ${
                      region.growth_indicator === 'high' ? 'text-green-400' :
                      region.growth_indicator === 'moderate' ? 'text-yellow-400' : 'text-slate-400'
                    }`}>
                      {region.growth_indicator.toUpperCase()}
                    </div>
                    <div className="text-slate-400 text-xs mt-2">
                      {region.top_sectors?.slice(0, 2).join(', ')}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default MLDashboard
