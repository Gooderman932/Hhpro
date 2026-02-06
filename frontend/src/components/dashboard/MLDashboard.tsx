import { useState, useEffect } from 'react'
import { TrendingUp, Target, MapPin, Loader2, AlertCircle, Shield, Zap, Brain, ArrowUpRight, ArrowDownRight, Minus, ChevronRight, Lock, Database, ExternalLink, Plus } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import {
  getCurrentSubscription,
  getMyProjects,
  getMLWinProbability,
  getMLDemandForecast,
  getMLRegionalOutlook,
  getMLCompetitiveLandscape,
  getMLProjectMatching
} from '../../services/api'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

export const MLDashboard = () => {
  const [subscription, setSubscription] = useState<any>(null)
  const [activeTab, setActiveTab] = useState('win')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dataSources, setDataSources] = useState<any>(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    Promise.all([
      getCurrentSubscription(),
      fetch(`${API_BASE}/data-sources`, { headers: { Authorization: `Bearer ${token}` } })
        .then(r => r.ok ? r.json() : null)
        .catch(() => null)
    ])
      .then(([sub, ds]) => { setSubscription(sub); setDataSources(ds) })
      .catch(() => setError('Failed to load data'))
      .finally(() => setLoading(false))
  }, [])

  const canAccess = subscription && ['professional', 'enterprise'].includes(subscription.tier_id)

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" data-testid="ml-loading" />
      </div>
    )
  }

  if (!canAccess) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="text-center">
              <Lock className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <CardTitle className="text-white" data-testid="upgrade-prompt">Professional Subscription Required</CardTitle>
              <CardDescription className="text-slate-400">
                Proprietary AI/ML models are available for Professional and Enterprise subscribers.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => window.location.href = '/pricing'} data-testid="upgrade-btn">
                Upgrade Now
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  const tabs = [
    { id: 'win', label: 'Win Probability', icon: Target, color: 'text-green-500' },
    { id: 'demand', label: 'Demand Forecast', icon: TrendingUp, color: 'text-blue-500' },
    { id: 'compete', label: 'Competitive Intel', icon: Shield, color: 'text-red-500' },
    { id: 'match', label: 'Project Matching', icon: Zap, color: 'text-amber-500' },
  ]

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12" data-testid="ml-dashboard">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-3 mb-2">
          <Brain className="h-7 w-7 text-blue-500" />
          <h1 className="text-3xl font-bold text-white">AI Intelligence Hub</h1>
        </div>
        <p className="text-slate-500 text-sm mb-6">Proprietary models by Poor Dude Holdings LLC - Patent Pending</p>

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">{error}</div>
        )}

        {/* Data Source Status Banner */}
        {dataSources && <DataSourceBanner dataSources={dataSources} />}

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {tabs.map(t => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              data-testid={`tab-${t.id}`}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium whitespace-nowrap transition ${
                activeTab === t.id
                  ? 'bg-slate-800 text-white border border-slate-600'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <t.icon className={`h-4 w-4 ${activeTab === t.id ? t.color : ''}`} />
              {t.label}
            </button>
          ))}
        </div>

        {activeTab === 'win' && <WinProbabilityTab />}
        {activeTab === 'demand' && <DemandForecastTab />}
        {activeTab === 'compete' && <CompetitiveIntelTab />}
        {activeTab === 'match' && <ProjectMatchingTab />}
      </div>
    </div>
  )
}

// ==========================================
// Data Source Status Banner
// ==========================================
const DataSourceBanner = ({ dataSources }: { dataSources: any }) => {
  const ud = dataSources?.user_data
  const es = dataSources?.external_sources
  const needsSetup = !ud?.profile_complete || !es?.permits?.configured || !es?.economic_indicators?.configured

  if (!needsSetup) return null

  return (
    <div className="mb-6 p-4 bg-amber-500/5 border border-amber-500/20 rounded-lg" data-testid="data-source-banner">
      <div className="flex items-center gap-2 mb-3">
        <Database className="h-4 w-4 text-amber-500" />
        <p className="text-amber-400 text-sm font-medium">Data Sources Setup</p>
      </div>
      <div className="grid md:grid-cols-3 gap-3 text-xs">
        {!ud?.profile_complete && (
          <a href="/onboarding" className="flex items-center gap-2 p-2 bg-slate-800/80 rounded text-slate-300 hover:text-white transition">
            <span className="w-2 h-2 rounded-full bg-red-500" />
            Complete your business profile
            <ChevronRight className="h-3 w-3 ml-auto" />
          </a>
        )}
        {!es?.permits?.configured && (
          <div className="flex items-center gap-2 p-2 bg-slate-800/80 rounded text-slate-400">
            <span className="w-2 h-2 rounded-full bg-yellow-500" />
            <span>Permit data: Not connected</span>
          </div>
        )}
        {!es?.economic_indicators?.configured && (
          <div className="flex items-center gap-2 p-2 bg-slate-800/80 rounded text-slate-400">
            <span className="w-2 h-2 rounded-full bg-yellow-500" />
            <span>FRED economic data: Not connected</span>
          </div>
        )}
      </div>
    </div>
  )
}

// ==========================================
// Source Label Component
// ==========================================
const SourceLabel = ({ source, className = '' }: { source: string; className?: string }) => (
  <span className={`inline-flex items-center gap-1 text-[10px] text-slate-500 ${className}`}>
    <Database className="h-2.5 w-2.5" />
    {source}
  </span>
)

// ==========================================
// Win Probability Tab
// ==========================================
const WinProbabilityTab = () => {
  const [projects, setProjects] = useState<any[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [prediction, setPrediction] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [initLoading, setInitLoading] = useState(true)

  useEffect(() => {
    getMyProjects()
      .then(setProjects)
      .catch(() => {})
      .finally(() => setInitLoading(false))
  }, [])

  const runPrediction = async (id: number) => {
    setSelectedId(id)
    setLoading(true)
    setPrediction(null)
    try {
      const result = await getMLWinProbability(id)
      setPrediction(result)
    } catch (err: any) {
      setPrediction({ error: err.response?.data?.detail || 'Prediction failed' })
    } finally {
      setLoading(false)
    }
  }

  if (initLoading) return <LoadingBlock />

  return (
    <div className="grid lg:grid-cols-5 gap-6" data-testid="win-probability-section">
      {/* Left: Project Selection */}
      <div className="lg:col-span-2 space-y-4">
        <Card className="bg-slate-900 border-slate-700">
          <CardHeader className="pb-3">
            <CardTitle className="text-white text-lg">Select Project</CardTitle>
            <CardDescription className="text-slate-400">Choose one of your projects to predict win probability</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2 max-h-[400px] overflow-y-auto">
            {projects.length === 0 && (
              <div className="text-center py-6">
                <Target className="h-10 w-10 text-slate-700 mx-auto mb-3" />
                <p className="text-slate-400 text-sm mb-1">No projects yet</p>
                <p className="text-slate-500 text-xs mb-4">Add your real projects to get AI-powered win probability predictions.</p>
                <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-sm" onClick={() => window.location.href = '/my-projects'} data-testid="add-project-btn">
                  <Plus className="h-3 w-3 mr-1" /> Add Your Projects
                </Button>
              </div>
            )}
            {projects.map((p: any) => (
              <button
                key={p.id}
                onClick={() => runPrediction(p.id)}
                data-testid={`project-${p.id}`}
                className={`w-full text-left p-3 rounded-lg transition ${
                  selectedId === p.id ? 'bg-green-500/10 border border-green-500/40' : 'bg-slate-800 hover:bg-slate-750 border border-transparent'
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-white text-sm font-medium">{p.name}</p>
                    <p className="text-slate-500 text-xs">{p.sector} {p.city ? `· ${p.city}, ${p.state}` : ''}</p>
                  </div>
                  {p.value && <span className="text-green-400 text-sm font-medium">${(p.value / 1000000).toFixed(1)}M</span>}
                </div>
              </button>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Right: Prediction Result */}
      <div className="lg:col-span-3">
        {loading && <LoadingBlock />}
        {!loading && prediction && !prediction.error && (
          <div className="space-y-4">
            <Card className="bg-slate-900 border-slate-700">
              <CardContent className="pt-6">
                <SourceLabel source="AI prediction based on your project data" className="mb-3" />
                <div className="text-center mb-6">
                  <div className="text-6xl font-bold text-green-400" data-testid="win-probability-value">
                    {(prediction.probability * 100).toFixed(1)}%
                  </div>
                  <p className="text-slate-400 mt-1">Win Probability</p>
                  <span className={`inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium ${
                    prediction.recommendation === 'STRONG PURSUE' ? 'bg-green-500/20 text-green-400' :
                    prediction.recommendation === 'PURSUE' ? 'bg-blue-500/20 text-blue-400' :
                    prediction.recommendation === 'EVALUATE' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  }`} data-testid="win-recommendation">
                    {prediction.recommendation}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-slate-800 p-3 rounded-lg text-center">
                    <p className="text-2xl font-bold text-blue-400">{(prediction.confidence * 100).toFixed(0)}%</p>
                    <p className="text-slate-500 text-xs">Confidence</p>
                  </div>
                  <div className="bg-slate-800 p-3 rounded-lg text-center">
                    <p className="text-sm font-medium text-slate-300 truncate">{prediction.model_version}</p>
                    <p className="text-slate-500 text-xs">Model</p>
                  </div>
                </div>

                <p className="text-slate-400 text-sm mb-4">{prediction.explanation}</p>

                {/* Factor Bars */}
                <div className="space-y-3">
                  <p className="text-white text-sm font-medium">Factor Breakdown</p>
                  {prediction.factors && Object.entries(prediction.factors).map(([key, val]: [string, any]) => (
                    <div key={key}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400 capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-slate-300">{(val * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full h-2 bg-slate-800 rounded-full">
                        <div className="h-2 bg-green-500 rounded-full transition-all" style={{ width: `${val * 100}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            <p className="text-slate-600 text-xs text-right">Watermark: {prediction.watermark}</p>
          </div>
        )}
        {!loading && prediction?.error && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6 text-center">
              <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <p className="text-red-400">{prediction.error}</p>
            </CardContent>
          </Card>
        )}
        {!loading && !prediction && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-16 text-center">
              <Target className="h-12 w-12 text-slate-700 mx-auto mb-3" />
              <p className="text-slate-500">
                {projects.length > 0
                  ? 'Select a project to generate a win probability prediction'
                  : 'Add your projects first, then get AI-powered win probability predictions'
                }
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

// ==========================================
// Demand Forecast Tab
// ==========================================
const DemandForecastTab = () => {
  const [region, setRegion] = useState('TX')
  const [sector, setSector] = useState('Commercial')
  const [forecast, setForecast] = useState<any>(null)
  const [outlook, setOutlook] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const loadForecast = async () => {
    setLoading(true)
    try {
      const [fc, ol] = await Promise.all([
        getMLDemandForecast(region, sector, 6),
        getMLRegionalOutlook(sector)
      ])
      setForecast(fc)
      setOutlook(ol)
    } catch (err: any) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadForecast() }, [])

  const TrendIcon = ({ trend }: { trend: string }) => {
    if (trend === 'INCREASING' || trend === 'UP') return <ArrowUpRight className="h-4 w-4 text-green-400" />
    if (trend === 'DECREASING' || trend === 'DOWN') return <ArrowDownRight className="h-4 w-4 text-red-400" />
    return <Minus className="h-4 w-4 text-slate-400" />
  }

  return (
    <div className="space-y-6" data-testid="demand-forecast-section">
      {/* Controls */}
      <Card className="bg-slate-900 border-slate-700">
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-4 items-end">
            <div>
              <label className="text-slate-400 text-xs block mb-1">Sector</label>
              <select value={sector} onChange={e => setSector(e.target.value)}
                className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm" data-testid="forecast-sector-select">
                {['Commercial','Residential','Healthcare','Industrial','Education','Retail','Data Center'].map(s =>
                  <option key={s} value={s}>{s}</option>
                )}
              </select>
            </div>
            <div>
              <label className="text-slate-400 text-xs block mb-1">Region</label>
              <select value={region} onChange={e => setRegion(e.target.value)}
                className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm" data-testid="forecast-region-select">
                {['TX','FL','AZ','CA','CO','GA','NC','TN','WA','OH','NV','PA','NY','IL'].map(r =>
                  <option key={r} value={r}>{r}</option>
                )}
              </select>
            </div>
            <Button onClick={loadForecast} disabled={loading} className="bg-blue-600 hover:bg-blue-700" data-testid="forecast-run-btn">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Generate Forecast'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {loading && <LoadingBlock />}

      {!loading && forecast && (
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Momentum Card */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-2">
              <CardTitle className="text-white text-lg">Market Momentum</CardTitle>
              <SourceLabel source="Proprietary demand model" />
            </CardHeader>
            <CardContent>
              <div className="text-center mb-4">
                <div className="text-5xl font-bold text-blue-400" data-testid="momentum-score">{forecast.momentum.score}</div>
                <p className="text-slate-500 text-sm mt-1">/ 100</p>
              </div>
              <div className="flex justify-center gap-2 mb-4">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  forecast.momentum.direction === 'UP' ? 'bg-green-500/20 text-green-400' :
                  forecast.momentum.direction === 'DOWN' ? 'bg-red-500/20 text-red-400' :
                  'bg-slate-700 text-slate-300'
                }`}>
                  {forecast.momentum.direction}
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-700 text-slate-300">
                  {forecast.momentum.strength}
                </span>
              </div>
              {forecast.momentum.factors?.length > 0 && (
                <div className="space-y-1">
                  {forecast.momentum.factors.map((f: string, i: number) => (
                    <p key={i} className="text-slate-400 text-xs flex items-center gap-1">
                      <ChevronRight className="h-3 w-3 text-blue-500" />{f}
                    </p>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Forecast Timeline */}
          <Card className="bg-slate-900 border-slate-700 lg:col-span-2">
            <CardHeader className="pb-2">
              <CardTitle className="text-white text-lg">6-Month Forecast: {sector} in {region}</CardTitle>
              <SourceLabel source="Proprietary forecasting engine" />
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {forecast.forecasts?.map((f: any, i: number) => {
                  const max = Math.max(...forecast.forecasts.map((x: any) => x.predicted_demand))
                  const pct = (f.predicted_demand / max) * 100
                  return (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-slate-400 text-sm w-16 shrink-0">{f.period}</span>
                      <div className="flex-1 h-7 bg-slate-800 rounded relative overflow-hidden">
                        <div className="h-full bg-blue-600/60 rounded transition-all" style={{ width: `${pct}%` }} />
                        <span className="absolute inset-0 flex items-center px-2 text-xs text-white font-medium">
                          {f.predicted_demand.toFixed(0)}
                        </span>
                      </div>
                      <TrendIcon trend={f.trend} />
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Regional Outlook */}
      {!loading && outlook && (
        <Card className="bg-slate-900 border-slate-700">
          <CardHeader className="pb-2">
            <CardTitle className="text-white text-lg flex items-center gap-2">
              <MapPin className="h-5 w-5 text-amber-500" />Regional Outlook: {sector}
            </CardTitle>
            <SourceLabel source="Proprietary regional analysis" />
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {Object.entries(outlook.outlook || {}).map(([reg, data]: [string, any]) => (
                <div key={reg} className="bg-slate-800 p-3 rounded-lg text-center">
                  <p className="text-lg font-bold text-white">{reg}</p>
                  <p className={`text-xs font-medium ${
                    data.direction === 'UP' ? 'text-green-400' : data.direction === 'DOWN' ? 'text-red-400' : 'text-slate-400'
                  }`}>
                    {data.direction} - {data.strength}
                  </p>
                  <p className="text-blue-400 text-sm font-medium mt-1">{data.momentum_score}</p>
                  <p className="text-slate-600 text-xs">momentum</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// ==========================================
// Competitive Intelligence Tab
// ==========================================
const CompetitiveIntelTab = () => {
  const [landscape, setLandscape] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getMLCompetitiveLandscape()
      .then(setLandscape)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingBlock />

  const cai = landscape?.competitive_advantage_index
  const rankings = landscape?.rankings || []

  // Empty state when no competitors tracked
  if (rankings.length === 0) {
    return (
      <div data-testid="competitive-intel-section">
        <Card className="bg-slate-900 border-slate-700">
          <CardContent className="py-16 text-center">
            <Shield className="h-14 w-14 text-slate-700 mx-auto mb-4" />
            <h3 className="text-white text-lg font-medium mb-2">No Competitors Tracked</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto mb-6">
              Start tracking your real competitors to get AI-powered competitive intelligence, threat analysis, and market positioning insights.
            </p>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => window.location.href = '/competitors'} data-testid="add-competitors-btn">
              <Plus className="h-4 w-4 mr-2" /> Track Competitors
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6" data-testid="competitive-intel-section">
      {/* CAI Card */}
      {cai && (
        <Card className="bg-slate-900 border-slate-700">
          <CardHeader className="pb-2">
            <CardTitle className="text-white text-lg">Your Competitive Advantage Index</CardTitle>
            <SourceLabel source="Based on your tracked competitors" />
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-5xl font-bold text-blue-400" data-testid="cai-score">{cai.score}</div>
                <p className="text-slate-500 text-sm mt-1">/ 100</p>
                <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs font-medium ${
                  cai.position === 'MARKET LEADER' ? 'bg-green-500/20 text-green-400' :
                  cai.position === 'STRONG COMPETITOR' ? 'bg-blue-500/20 text-blue-400' :
                  'bg-slate-700 text-slate-300'
                }`} data-testid="cai-position">
                  {cai.position}
                </span>
              </div>
              <div>
                <p className="text-green-400 text-sm font-medium mb-2">Strengths</p>
                {cai.strengths.map((s: string, i: number) => (
                  <p key={i} className="text-slate-400 text-xs mb-1 flex items-center gap-1">
                    <ChevronRight className="h-3 w-3 text-green-500" />{s}
                  </p>
                ))}
              </div>
              <div>
                <p className="text-yellow-400 text-sm font-medium mb-2">Improve</p>
                {cai.improvement_areas.map((a: string, i: number) => (
                  <p key={i} className="text-slate-400 text-xs mb-1 flex items-center gap-1">
                    <ChevronRight className="h-3 w-3 text-yellow-500" />{a}
                  </p>
                ))}
              </div>
              <div>
                <p className="text-red-400 text-sm font-medium mb-2">Gaps</p>
                {cai.competitive_gaps.map((g: string, i: number) => (
                  <p key={i} className="text-slate-400 text-xs mb-1 flex items-center gap-1">
                    <ChevronRight className="h-3 w-3 text-red-500" />{g}
                  </p>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Competitor Rankings */}
      <Card className="bg-slate-900 border-slate-700">
        <CardHeader className="pb-2">
          <CardTitle className="text-white text-lg">Competitor Threat Rankings</CardTitle>
          <SourceLabel source={`Based on ${rankings.length} tracked competitor${rankings.length > 1 ? 's' : ''}`} />
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {rankings.map((r: any, i: number) => (
              <div key={i} className="bg-slate-800 p-4 rounded-lg flex items-center gap-4" data-testid={`competitor-${i}`}>
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                  r.threat_level === 'CRITICAL' ? 'bg-red-500/20 text-red-400' :
                  r.threat_level === 'HIGH' ? 'bg-orange-500/20 text-orange-400' :
                  r.threat_level === 'MODERATE' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-green-500/20 text-green-400'
                }`}>
                  {r.threat_score.toFixed(0)}
                </div>
                <div className="flex-1">
                  <p className="text-white font-medium">{r.competitor_name}</p>
                  <p className={`text-xs font-medium ${
                    r.threat_level === 'CRITICAL' ? 'text-red-400' :
                    r.threat_level === 'HIGH' ? 'text-orange-400' :
                    r.threat_level === 'MODERATE' ? 'text-yellow-400' :
                    'text-green-400'
                  }`}>{r.threat_level}</p>
                </div>
                <div className="flex gap-4 text-xs">
                  {r.strengths?.length > 0 && (
                    <div>
                      <p className="text-slate-500 mb-1">Strengths</p>
                      {r.strengths.slice(0, 2).map((s: string, j: number) => (
                        <p key={j} className="text-slate-400">{s}</p>
                      ))}
                    </div>
                  )}
                  {r.vulnerabilities?.length > 0 && (
                    <div>
                      <p className="text-slate-500 mb-1">Weaknesses</p>
                      {r.vulnerabilities.slice(0, 2).map((v: string, j: number) => (
                        <p key={j} className="text-green-400">{v}</p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// ==========================================
// Project Matching Tab
// ==========================================
const ProjectMatchingTab = () => {
  const [matches, setMatches] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getMLProjectMatching(20, 20)
      .then(data => {
        setMatches(data.matches || [])
        setTotal(data.total || 0)
      })
      .catch(err => {
        const detail = err?.response?.data?.detail
        if (detail?.includes('profile')) {
          setError('profile')
        } else {
          setError(detail || 'Failed to load matches')
        }
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingBlock />

  if (error === 'profile') {
    return (
      <div data-testid="project-matching-section">
        <Card className="bg-slate-900 border-slate-700">
          <CardContent className="py-16 text-center">
            <Zap className="h-14 w-14 text-slate-700 mx-auto mb-4" />
            <h3 className="text-white text-lg font-medium mb-2">Complete Your Profile First</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto mb-6">
              We need to know your trade specialty, service area, and project preferences to match you with relevant opportunities.
            </p>
            <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => window.location.href = '/onboarding'} data-testid="complete-profile-btn">
              Complete Profile
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <Card className="bg-slate-900 border-slate-700">
        <CardContent className="pt-6 text-center">
          <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
          <p className="text-red-400">{error}</p>
        </CardContent>
      </Card>
    )
  }

  if (matches.length === 0) {
    return (
      <div data-testid="project-matching-section">
        <Card className="bg-slate-900 border-slate-700">
          <CardContent className="py-16 text-center">
            <Zap className="h-14 w-14 text-slate-700 mx-auto mb-4" />
            <h3 className="text-white text-lg font-medium mb-2">No Matching Projects Found</h3>
            <p className="text-slate-400 text-sm max-w-md mx-auto mb-2">
              Connect a permit data source to discover real construction opportunities in your area that match your profile.
            </p>
            <p className="text-slate-500 text-xs">Requires PERMIT_API_KEY to be configured.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-4" data-testid="project-matching-section">
      <div className="flex justify-between items-center">
        <p className="text-slate-400 text-sm">{total} matching opportunities found</p>
        <SourceLabel source="Matched from live permit data + your profile" />
      </div>

      {matches.map((m: any, i: number) => (
        <Card key={i} className={`bg-slate-900 border-slate-700 ${
          m.fit_score >= 80 ? 'border-l-4 border-l-green-500' :
          m.fit_score >= 60 ? 'border-l-4 border-l-blue-500' : ''
        }`} data-testid={`match-${i}`}>
          <CardContent className="pt-5 pb-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-white font-medium">{m.project?.name || 'Unknown Project'}</h3>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    m.recommendation === 'HIGHLY RECOMMENDED' ? 'bg-green-500/20 text-green-400' :
                    m.recommendation === 'RECOMMENDED' ? 'bg-blue-500/20 text-blue-400' :
                    m.recommendation === 'CONSIDER' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-slate-700 text-slate-300'
                  }`}>
                    {m.recommendation}
                  </span>
                </div>
                <p className="text-slate-500 text-sm">
                  {m.project?.sector} {m.project?.city ? `· ${m.project.city}, ${m.project.state}` : ''}
                  {m.project?.value ? ` · $${(m.project.value / 1000000).toFixed(1)}M` : ''}
                </p>

                {m.match_reasons?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {m.match_reasons.map((r: string, j: number) => (
                      <span key={j} className="px-2 py-0.5 bg-blue-500/10 text-blue-400 text-xs rounded">{r}</span>
                    ))}
                  </div>
                )}
                {m.concerns?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-1">
                    {m.concerns.map((c: string, j: number) => (
                      <span key={j} className="px-2 py-0.5 bg-yellow-500/10 text-yellow-400 text-xs rounded">{c}</span>
                    ))}
                  </div>
                )}
              </div>
              <div className="text-right shrink-0">
                <div className={`text-3xl font-bold ${
                  m.fit_score >= 80 ? 'text-green-400' :
                  m.fit_score >= 60 ? 'text-blue-400' :
                  m.fit_score >= 40 ? 'text-yellow-400' : 'text-slate-500'
                }`}>
                  {m.fit_score.toFixed(0)}
                </div>
                <p className="text-slate-500 text-xs">fit score</p>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

// ==========================================
// Shared Loading Block
// ==========================================
const LoadingBlock = () => (
  <div className="flex items-center justify-center py-16">
    <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
  </div>
)

export default MLDashboard
