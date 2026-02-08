import { useState, useEffect } from 'react'
import { Search, Loader2, MapPin, DollarSign, Calendar, Star, Target, AlertCircle, Database, Landmark, Clock, ExternalLink, Lock } from 'lucide-react'
import { Card, CardContent } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

const ALL_STATES = [
  'AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA',
  'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM',
  'NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA',
  'WV','WI','WY','PR','GU','VI'
]

interface Opportunity {
  opportunity_id: string
  title: string
  agency: string
  naics: string
  place_of_performance_state: string
  place_of_performance_city: string | null
  estimated_value: number | null
  response_deadline: string | null
  notice_type: string
  url: string
  source: string
  proprietary_analysis?: {
    match_score: number
    win_probability: number
    required_trades: string[]
    estimated_timeline_months: number
    opportunity_score: number
    recommendation: string
  }
}

export const FederalOpportunities = () => {
  const [opps, setOpps] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [state, setState] = useState('')
  const [meta, setMeta] = useState<any>(null)

  const search = async () => {
    setLoading(true)
    setError(null)
    try {
      const params: any = { limit: 50 }
      if (state) params.state = state
      const res = await api.get('/procurement/federal', { params })
      setOpps(res.data.opportunities || [])
      setMeta(res.data)
    } catch (err: any) {
      const detail = err.response?.data?.detail || ''
      if (err.response?.status === 403) {
        setError('upgrade')
      } else {
        setError(detail || 'Failed to load federal opportunities')
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { search() }, [])

  if (error === 'upgrade') {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-16 text-center">
              <Lock className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <h2 className="text-white text-xl font-bold mb-2">Pro Subscription Required</h2>
              <p className="text-slate-400 text-sm mb-4">Federal procurement intelligence is available for Pro ($149/mo) and Enterprise ($399/mo) subscribers.</p>
              <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => window.location.href = '/pricing'} data-testid="upgrade-btn">
                Upgrade Now
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12" data-testid="federal-opportunities">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-3 mb-1">
          <Landmark className="h-6 w-6 text-amber-500" />
          <h1 className="text-2xl font-bold text-white">Federal Contracts</h1>
        </div>
        <p className="text-slate-500 text-sm mb-5">AI-scored government construction opportunities - Patent Pending</p>

        {/* Search */}
        <Card className="bg-slate-900 border-slate-700 mb-6">
          <CardContent className="pt-4 pb-4">
            <div className="flex flex-wrap gap-3 items-end">
              <div>
                <label className="text-slate-400 text-xs block mb-1">State (Place of Performance)</label>
                <select value={state} onChange={e => setState(e.target.value)}
                  className="p-2 bg-slate-800 border border-slate-600 rounded-lg text-white text-sm"
                  data-testid="fed-state-select">
                  <option value="">All States</option>
                  {ALL_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <Button onClick={search} disabled={loading} className="bg-amber-600 hover:bg-amber-700" data-testid="fed-search-btn">
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <><Search className="h-4 w-4 mr-1" /> Search</>}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Sources */}
        {meta && (
          <div className="flex flex-wrap gap-3 mb-4 text-xs">
            {meta.data_sources?.map((src: string, i: number) => (
              <span key={i} className="inline-flex items-center gap-1 px-2 py-1 bg-slate-800 rounded text-slate-400">
                <Database className="h-3 w-3" />{src}
              </span>
            ))}
            <span className="px-2 py-1 bg-amber-500/10 rounded text-amber-400">{meta.count} results ({meta.tier})</span>
          </div>
        )}

        {error && error !== 'upgrade' && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm flex items-center gap-2">
            <AlertCircle className="h-4 w-4" />{error}
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-8 w-8 text-amber-500 animate-spin" />
          </div>
        )}

        {!loading && opps.length === 0 && !error && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-16 text-center">
              <Landmark className="h-14 w-14 text-slate-700 mx-auto mb-4" />
              <h3 className="text-white text-lg font-medium mb-2">No Federal Opportunities Found</h3>
              <p className="text-slate-400 text-sm">Try selecting a different state or broadening your search.</p>
            </CardContent>
          </Card>
        )}

        {/* Opportunity Cards */}
        <div className="space-y-3">
          {opps.map((o, i) => {
            const ai = o.proprietary_analysis
            const score = ai?.opportunity_score || 0
            return (
              <Card key={`${o.opportunity_id}-${i}`} className={`bg-slate-900 border-slate-700 ${
                score >= 70 ? 'border-l-4 border-l-green-500' :
                score >= 50 ? 'border-l-4 border-l-amber-500' :
                score >= 30 ? 'border-l-4 border-l-blue-500' : ''
              }`} data-testid={`fed-opp-${i}`}>
                <CardContent className="pt-4 pb-4">
                  <div className="flex gap-4">
                    <div className="shrink-0 w-16 text-center">
                      <div className={`text-2xl font-bold ${
                        score >= 70 ? 'text-green-400' : score >= 50 ? 'text-amber-400' :
                        score >= 30 ? 'text-blue-400' : 'text-slate-500'
                      }`}>{score.toFixed(0)}</div>
                      <p className="text-slate-600 text-[10px]">OPP SCORE</p>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <div>
                          <p className="text-white font-medium text-sm">{o.title || 'Federal Opportunity'}</p>
                          <p className="text-slate-500 text-xs flex items-center gap-2">
                            <span className="flex items-center gap-0.5"><Landmark className="h-3 w-3" />{o.agency}</span>
                            {o.place_of_performance_state && (
                              <span className="flex items-center gap-0.5"><MapPin className="h-3 w-3" />{o.place_of_performance_city ? `${o.place_of_performance_city}, ` : ''}{o.place_of_performance_state}</span>
                            )}
                          </p>
                        </div>
                        {o.estimated_value && o.estimated_value > 0 && (
                          <span className="text-green-400 text-sm font-medium shrink-0 flex items-center gap-0.5">
                            <DollarSign className="h-3 w-3" />
                            {o.estimated_value >= 1_000_000
                              ? `${(o.estimated_value / 1_000_000).toFixed(1)}M`
                              : `${(o.estimated_value / 1_000).toFixed(0)}k`}
                          </span>
                        )}
                      </div>

                      {ai && (
                        <div className="flex flex-wrap gap-2 mt-2 items-center">
                          <span className="text-xs px-2 py-0.5 rounded bg-green-500/10 text-green-400 flex items-center gap-1">
                            <Target className="h-3 w-3" /> Match {ai.match_score.toFixed(0)}%
                          </span>
                          <span className="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 flex items-center gap-1">
                            <Star className="h-3 w-3" /> Win {ai.win_probability.toFixed(0)}%
                          </span>
                          <span className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300 flex items-center gap-1">
                            <Clock className="h-3 w-3" /> ~{ai.estimated_timeline_months}mo
                          </span>
                          {o.naics && <span className="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-400">NAICS {o.naics}</span>}
                          {ai.required_trades.slice(0, 3).map((t, j) => (
                            <span key={j} className="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 capitalize">{t}</span>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between mt-2">
                        <p className={`text-xs font-medium ${
                          ai && ai.opportunity_score >= 60 ? 'text-green-400' : 'text-slate-400'
                        }`}>{ai?.recommendation || ''}</p>
                        <div className="flex items-center gap-3 text-[10px] text-slate-600">
                          {o.response_deadline && <span className="flex items-center gap-0.5"><Calendar className="h-2.5 w-2.5" />Due: {o.response_deadline.slice(0, 10)}</span>}
                          {o.notice_type && <span className="uppercase">{o.notice_type}</span>}
                          {o.url && (
                            <a href={o.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 flex items-center gap-0.5">
                              View <ExternalLink className="h-2.5 w-2.5" />
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {opps.length > 0 && (
          <p className="text-slate-600 text-[10px] mt-6 text-center">
            Federal procurement data from official U.S. government systems. All AI analysis is Patent Pending, Proprietary of Poor Dude Holdings LLC.
          </p>
        )}
      </div>
    </div>
  )
}

export default FederalOpportunities
