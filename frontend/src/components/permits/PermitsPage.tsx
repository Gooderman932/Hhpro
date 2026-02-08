import { useState, useEffect } from 'react'
import { Search, Loader2, MapPin, DollarSign, Calendar, Star, Target, AlertCircle, Database, Shield, Clock } from 'lucide-react'
import { Card, CardContent } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

const ALL_STATES = [
  'AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA',
  'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM',
  'NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA',
  'WV','WI','WY','PR','GU','VI'
]

interface Permit {
  permit_id: string
  address: string
  city: string
  state: string
  work_type: string
  estimated_cost: number | null
  filing_date: string
  status: string
  contractor_name: string | null
  description: string
  source: string
  proprietary_analysis?: {
    match_score: number
    win_probability: number
    required_trades: string[]
    estimated_timeline_months: number
    opportunity_score: number
    recommendation: string
    legal_notice: string
  }
}

export const PermitsDashboard = () => {
  const [permits, setPermits] = useState<Permit[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [state, setState] = useState('')
  const [location, setLocation] = useState('')
  const [meta, setMeta] = useState<any>(null)

  const search = async () => {
    setLoading(true)
    setError(null)
    try {
      const params: any = { limit: 50 }
      if (state) params.state = state
      if (location) params.location = location
      const res = await api.get('/permits/search', { params })
      setPermits(res.data.permits || [])
      setMeta(res.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load permits')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { search() }, [])

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12" data-testid="permits-dashboard">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-3 mb-1">
          <Shield className="h-6 w-6 text-blue-500" />
          <h1 className="text-2xl font-bold text-white">Permit Intelligence</h1>
        </div>
        <p className="text-slate-500 text-sm mb-5">AI-scored construction opportunities - Patent Pending</p>

        {/* Search Bar */}
        <Card className="bg-slate-900 border-slate-700 mb-6">
          <CardContent className="pt-4 pb-4">
            <div className="flex flex-wrap gap-3 items-end">
              <div className="flex-1 min-w-[200px]">
                <label className="text-slate-400 text-xs block mb-1">Location / City</label>
                <input value={location} onChange={e => setLocation(e.target.value)}
                  placeholder="e.g. Austin, Miami..."
                  className="w-full p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm placeholder:text-slate-500"
                  data-testid="search-location" />
              </div>
              <div>
                <label className="text-slate-400 text-xs block mb-1">State</label>
                <select value={state} onChange={e => setState(e.target.value)}
                  className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm"
                  data-testid="search-state">
                  <option value="">All States</option>
                  {ALL_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <Button onClick={search} disabled={loading} className="bg-blue-600 hover:bg-blue-700" data-testid="search-btn">
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <><Search className="h-4 w-4 mr-1" /> Search</>}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Data Sources & Tier Info */}
        {meta && (
          <div className="flex flex-wrap gap-3 mb-4 text-xs">
            {meta.data_sources?.map((src: string, i: number) => (
              <span key={i} className="inline-flex items-center gap-1 px-2 py-1 bg-slate-800 rounded text-slate-400">
                <Database className="h-3 w-3" />{src}
              </span>
            ))}
            <span className="px-2 py-1 bg-blue-500/10 rounded text-blue-400">{meta.count} results ({meta.tier})</span>
          </div>
        )}

        {error && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm flex items-center gap-2">
            <AlertCircle className="h-4 w-4" />{error}
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
          </div>
        )}

        {!loading && permits.length === 0 && !error && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-16 text-center">
              <Shield className="h-14 w-14 text-slate-700 mx-auto mb-4" />
              <h3 className="text-white text-lg font-medium mb-2">No Permits Found</h3>
              <p className="text-slate-400 text-sm max-w-md mx-auto">
                {meta?.data_sources?.includes('No permit sources configured')
                  ? 'Connect a paid permit source (Shovels.ai or BatchData) for nationwide coverage. NYC open data is included free.'
                  : 'Try adjusting your search filters or broadening your location.'}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Permit Cards */}
        <div className="space-y-3">
          {permits.map((p, i) => {
            const ai = p.proprietary_analysis
            const oppScore = ai?.opportunity_score || 0
            return (
              <Card key={`${p.permit_id}-${i}`} className={`bg-slate-900 border-slate-700 ${
                oppScore >= 70 ? 'border-l-4 border-l-green-500' :
                oppScore >= 50 ? 'border-l-4 border-l-blue-500' :
                oppScore >= 30 ? 'border-l-4 border-l-yellow-500' : ''
              }`} data-testid={`permit-${i}`}>
                <CardContent className="pt-4 pb-4">
                  <div className="flex gap-4">
                    {/* Score Column */}
                    <div className="shrink-0 w-16 text-center">
                      <div className={`text-2xl font-bold ${
                        oppScore >= 70 ? 'text-green-400' :
                        oppScore >= 50 ? 'text-blue-400' :
                        oppScore >= 30 ? 'text-yellow-400' : 'text-slate-500'
                      }`}>
                        {oppScore.toFixed(0)}
                      </div>
                      <p className="text-slate-600 text-[10px]">OPP SCORE</p>
                    </div>

                    {/* Main Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <div>
                          <p className="text-white font-medium text-sm truncate">
                            {p.description || p.work_type || 'Construction Permit'}
                          </p>
                          <p className="text-slate-500 text-xs flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {p.address ? `${p.address}, ` : ''}{p.city}, {p.state}
                          </p>
                        </div>
                        {p.estimated_cost && p.estimated_cost > 0 && (
                          <span className="text-green-400 text-sm font-medium shrink-0 flex items-center gap-0.5">
                            <DollarSign className="h-3 w-3" />
                            {p.estimated_cost >= 1_000_000
                              ? `${(p.estimated_cost / 1_000_000).toFixed(1)}M`
                              : `${(p.estimated_cost / 1_000).toFixed(0)}k`}
                          </span>
                        )}
                      </div>

                      {/* AI Analysis Row */}
                      {ai && (
                        <div className="flex flex-wrap gap-2 mt-2 items-center">
                          <span className="text-xs px-2 py-0.5 rounded bg-green-500/10 text-green-400 flex items-center gap-1" data-testid={`match-${i}`}>
                            <Target className="h-3 w-3" /> Match {ai.match_score.toFixed(0)}%
                          </span>
                          <span className="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 flex items-center gap-1" data-testid={`win-${i}`}>
                            <Star className="h-3 w-3" /> Win {ai.win_probability.toFixed(0)}%
                          </span>
                          {ai.estimated_timeline_months > 0 && (
                            <span className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300 flex items-center gap-1">
                              <Clock className="h-3 w-3" /> ~{ai.estimated_timeline_months}mo
                            </span>
                          )}
                          {ai.required_trades.map((t, j) => (
                            <span key={j} className="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 capitalize">{t}</span>
                          ))}
                        </div>
                      )}

                      {/* Recommendation + Meta */}
                      <div className="flex items-center justify-between mt-2">
                        <p className={`text-xs font-medium ${
                          ai && ai.opportunity_score >= 70 ? 'text-green-400' :
                          ai && ai.opportunity_score >= 50 ? 'text-blue-400' :
                          'text-slate-400'
                        }`}>
                          {ai?.recommendation || ''}
                        </p>
                        <div className="flex items-center gap-3 text-[10px] text-slate-600">
                          {p.filing_date && <span className="flex items-center gap-0.5"><Calendar className="h-2.5 w-2.5" />{p.filing_date.slice(0, 10)}</span>}
                          <span className="uppercase">{p.source.replace(/_/g, ' ')}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Legal Footer */}
        {permits.length > 0 && (
          <p className="text-slate-600 text-[10px] mt-6 text-center">
            Government data belongs to respective agencies. All AI analysis is Patent Pending, Proprietary of Poor Dude Holdings LLC.
          </p>
        )}
      </div>
    </div>
  )
}

export default PermitsDashboard
