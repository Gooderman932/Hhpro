import { useState, useEffect, useCallback } from 'react'
import { DollarSign, Users, TrendingUp, TrendingDown, AlertTriangle, RefreshCw, Download, Loader2, ShieldCheck, BarChart3, ArrowUpRight, ArrowDownRight, Clock } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

interface RevenueSummary {
  mrr: number
  arr: number
  total_active_subscribers: number
  arpu: number
  churn_rate_pct: number
  conversion_rate_pct: number
  total_users: number
  growth_rate_pct: number
  top_tier_by_revenue: string
}

interface RevenueData {
  summary: RevenueSummary
  tier_breakdown: { counts: Record<string, number>; revenue: Record<string, number> }
  ltv_by_tier: Record<string, number>
  revenue_trend: { date: string; revenue: number }[]
  recent_transactions: any[]
  recent_signups: any[]
  alerts: { failed_payments: number; cancelled_last_30d: number; past_due_accounts: any[] }
  period_days: number
}

export const AdminDashboard = () => {
  const [data, setData] = useState<RevenueData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [days, setDays] = useState(90)
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null)

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.get(`/admin/revenue?days=${days}`)
      setData(res.data)
      setLastRefresh(new Date())
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load revenue data')
    } finally {
      setLoading(false)
    }
  }, [days])

  useEffect(() => { loadData() }, [loadData])

  const handleExport = async () => {
    try {
      const res = await api.get('/admin/revenue/export', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const a = document.createElement('a')
      a.href = url
      a.download = `revenue_export_${new Date().toISOString().slice(0,10)}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch { /* silent */ }
  }

  if (error === 'Admin access required') {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4 flex items-center justify-center">
        <Card className="bg-slate-900 border-slate-700 max-w-md">
          <CardContent className="pt-8 pb-8 text-center">
            <ShieldCheck className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-white text-xl font-bold mb-2">Access Denied</h2>
            <p className="text-slate-400 text-sm">This page is restricted to administrators.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" data-testid="admin-loading" />
      </div>
    )
  }

  if (!data) return null
  const s = data.summary

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12" data-testid="admin-dashboard">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div>
            <div className="flex items-center gap-2">
              <BarChart3 className="h-6 w-6 text-blue-500" />
              <h1 className="text-2xl font-bold text-white">Revenue Dashboard</h1>
            </div>
            {lastRefresh && (
              <p className="text-slate-500 text-xs mt-1 flex items-center gap-1">
                <Clock className="h-3 w-3" /> Updated {lastRefresh.toLocaleTimeString()}
              </p>
            )}
          </div>
          <div className="flex items-center gap-3">
            <div className="flex bg-slate-800 rounded-lg overflow-hidden">
              {[30, 60, 90].map(d => (
                <button key={d} onClick={() => setDays(d)}
                  data-testid={`range-${d}`}
                  className={`px-3 py-1.5 text-xs font-medium transition ${days === d ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}>
                  {d}d
                </button>
              ))}
            </div>
            <Button size="sm" variant="outline" onClick={loadData} disabled={loading} data-testid="refresh-btn"
              className="border-slate-600 text-slate-300 hover:text-white">
              <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} /> Refresh
            </Button>
            <Button size="sm" onClick={handleExport} data-testid="export-btn"
              className="bg-slate-800 text-slate-300 hover:text-white border border-slate-600">
              <Download className="h-3 w-3 mr-1" /> CSV
            </Button>
          </div>
        </div>

        {/* Alerts Banner */}
        {(data.alerts.failed_payments > 0 || data.alerts.cancelled_last_30d > 0) && (
          <div className="mb-6 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-3" data-testid="alerts-banner">
            <AlertTriangle className="h-5 w-5 text-red-400 shrink-0" />
            <div className="text-sm">
              {data.alerts.failed_payments > 0 && (
                <span className="text-red-400 font-medium mr-4">{data.alerts.failed_payments} failed payment(s)</span>
              )}
              {data.alerts.cancelled_last_30d > 0 && (
                <span className="text-yellow-400 font-medium">{data.alerts.cancelled_last_30d} cancellation(s) last 30 days</span>
              )}
            </div>
          </div>
        )}

        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <KPICard label="MRR" value={`$${formatNum(s.mrr)}`} icon={DollarSign} color="text-green-400" bg="bg-green-500/10" testId="kpi-mrr" />
          <KPICard label="ARR" value={`$${formatNum(s.arr)}`} icon={TrendingUp} color="text-blue-400" bg="bg-blue-500/10" testId="kpi-arr" />
          <KPICard label="Active Subscribers" value={String(s.total_active_subscribers)} icon={Users} color="text-purple-400" bg="bg-purple-500/10" testId="kpi-subs" />
          <KPICard label="Churn Rate" value={`${s.churn_rate_pct}%`} icon={s.churn_rate_pct > 5 ? TrendingDown : TrendingUp}
            color={s.churn_rate_pct > 5 ? 'text-red-400' : 'text-green-400'}
            bg={s.churn_rate_pct > 5 ? 'bg-red-500/10' : 'bg-green-500/10'} testId="kpi-churn" />
        </div>

        {/* Secondary Metrics */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
          <MetricCard label="ARPU" value={`$${formatNum(s.arpu)}`} testId="metric-arpu" />
          <MetricCard label="Conversion" value={`${s.conversion_rate_pct.toFixed(1)}%`} subtext={`${s.total_users} total users`} testId="metric-conversion" />
          <MetricCard label="Growth Rate" value={`${s.growth_rate_pct >= 0 ? '+' : ''}${s.growth_rate_pct.toFixed(1)}%`}
            positive={s.growth_rate_pct >= 0} testId="metric-growth" />
          <MetricCard label="Top Tier" value={tierName(s.top_tier_by_revenue)} testId="metric-top-tier" />
          <MetricCard label="Total Users" value={String(s.total_users)} testId="metric-total-users" />
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-6">
          {/* Revenue by Tier (bar chart style) */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-base">Revenue by Tier</CardTitle>
            </CardHeader>
            <CardContent>
              {Object.entries(data.tier_breakdown.revenue).map(([tier, rev]) => {
                const maxRev = Math.max(...Object.values(data.tier_breakdown.revenue), 1)
                const pct = (rev / maxRev) * 100
                return (
                  <div key={tier} className="mb-4" data-testid={`tier-rev-${tier}`}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-300 capitalize">{tierName(tier)}</span>
                      <span className="text-white font-medium">${formatNum(rev)}</span>
                    </div>
                    <div className="w-full h-3 bg-slate-800 rounded-full">
                      <div className={`h-3 rounded-full ${tierColor(tier)}`} style={{ width: `${Math.max(pct, 2)}%` }} />
                    </div>
                    <p className="text-slate-500 text-xs mt-0.5">{data.tier_breakdown.counts[tier]} subscriber(s)</p>
                  </div>
                )
              })}
            </CardContent>
          </Card>

          {/* Subscriber Breakdown (pie-like) */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-base">Subscriber Mix</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center mb-4">
                <div className="relative w-32 h-32">
                  <svg viewBox="0 0 36 36" className="w-32 h-32 -rotate-90">
                    {renderPieSegments(data.tier_breakdown.counts, s.total_active_subscribers)}
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-2xl font-bold text-white">{s.total_active_subscribers}</span>
                    <span className="text-slate-500 text-xs">active</span>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                {Object.entries(data.tier_breakdown.counts).map(([tier, count]) => (
                  <div key={tier} className="flex items-center justify-between" data-testid={`tier-count-${tier}`}>
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${tierBg(tier)}`} />
                      <span className="text-slate-300 text-sm capitalize">{tierName(tier)}</span>
                    </div>
                    <span className="text-white text-sm font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* LTV by Tier */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-base">Lifetime Value (LTV)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(data.ltv_by_tier).map(([tier, ltv]) => (
                  <div key={tier} className="bg-slate-800 p-3 rounded-lg" data-testid={`ltv-${tier}`}>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-300 capitalize text-sm">{tierName(tier)}</span>
                      <span className="text-green-400 font-bold text-lg">${formatNum(ltv)}</span>
                    </div>
                    <p className="text-slate-500 text-xs mt-1">${TIER_PRICES_FE[tier]}/mo price</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Revenue Trend */}
        <Card className="bg-slate-900 border-slate-700 mb-6">
          <CardHeader className="pb-3">
            <CardTitle className="text-white text-base">Revenue Trend ({days} days)</CardTitle>
          </CardHeader>
          <CardContent>
            <RevenueTrendChart data={data.revenue_trend} />
          </CardContent>
        </Card>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Recent Transactions */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-base">Recent Transactions</CardTitle>
            </CardHeader>
            <CardContent>
              {data.recent_transactions.length === 0 ? (
                <p className="text-slate-500 text-sm text-center py-6">No transactions yet</p>
              ) : (
                <div className="space-y-2 max-h-[300px] overflow-y-auto">
                  {data.recent_transactions.map((tx: any) => (
                    <div key={tx.id} className="flex items-center justify-between p-2 bg-slate-800 rounded-lg" data-testid={`tx-${tx.id}`}>
                      <div>
                        <p className="text-white text-sm">{tx.email}</p>
                        <p className="text-slate-500 text-xs capitalize">{tierName(tx.tier)} - {tx.status}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-green-400 font-medium">${tx.amount}</p>
                        <p className="text-slate-600 text-xs">{tx.date ? new Date(tx.date).toLocaleDateString() : ''}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recent Signups */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-white text-base">Recent Signups</CardTitle>
            </CardHeader>
            <CardContent>
              {data.recent_signups.length === 0 ? (
                <p className="text-slate-500 text-sm text-center py-6">No signups yet</p>
              ) : (
                <div className="space-y-2 max-h-[300px] overflow-y-auto">
                  {data.recent_signups.map((u: any) => (
                    <div key={u.id} className="flex items-center justify-between p-2 bg-slate-800 rounded-lg" data-testid={`signup-${u.id}`}>
                      <div>
                        <p className="text-white text-sm">{u.email}</p>
                        <p className="text-slate-500 text-xs">{u.name || 'No name'}</p>
                      </div>
                      <p className="text-slate-400 text-xs">{u.date ? new Date(u.date).toLocaleDateString() : ''}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

// ==========================================
// Helper Components
// ==========================================

const TIER_PRICES_FE: Record<string, number> = { basic: 49, professional: 149, enterprise: 399 }

const formatNum = (n: number) => n >= 1000 ? `${(n / 1000).toFixed(1)}k` : n.toFixed(0)
const tierName = (t: string) => t === 'professional' ? 'Pro' : t === 'enterprise' ? 'Enterprise' : t === 'basic' ? 'Basic' : t
const tierColor = (t: string) => t === 'enterprise' ? 'bg-purple-500' : t === 'professional' ? 'bg-blue-500' : 'bg-green-500'
const tierBg = (t: string) => t === 'enterprise' ? 'bg-purple-500' : t === 'professional' ? 'bg-blue-500' : 'bg-green-500'

const KPICard = ({ label, value, icon: Icon, color, bg, testId }: any) => (
  <Card className="bg-slate-900 border-slate-700" data-testid={testId}>
    <CardContent className="pt-5 pb-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-500 text-xs mb-1">{label}</p>
          <p className={`text-2xl font-bold ${color}`}>{value}</p>
        </div>
        <div className={`p-2.5 rounded-lg ${bg}`}>
          <Icon className={`h-5 w-5 ${color}`} />
        </div>
      </div>
    </CardContent>
  </Card>
)

const MetricCard = ({ label, value, subtext, positive, testId }: any) => (
  <div className="bg-slate-900 border border-slate-700 rounded-lg p-3" data-testid={testId}>
    <p className="text-slate-500 text-xs mb-1">{label}</p>
    <p className={`text-lg font-bold ${positive === false ? 'text-red-400' : positive === true ? 'text-green-400' : 'text-white'}`}>
      {value}
    </p>
    {subtext && <p className="text-slate-600 text-xs">{subtext}</p>}
  </div>
)

const RevenueTrendChart = ({ data }: { data: { date: string; revenue: number }[] }) => {
  if (!data || data.length === 0) {
    return <p className="text-slate-500 text-sm text-center py-8">No revenue data in this period</p>
  }

  const maxRev = Math.max(...data.map(d => d.revenue), 1)
  const hasRevenue = data.some(d => d.revenue > 0)

  if (!hasRevenue) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-500 text-sm">No paid transactions recorded in this period.</p>
        <p className="text-slate-600 text-xs mt-1">Revenue will appear here after real payments are processed.</p>
      </div>
    )
  }

  // Show last 30 data points max for readability
  const chartData = data.slice(-30)

  return (
    <div className="flex items-end gap-1 h-40" data-testid="revenue-chart">
      {chartData.map((d, i) => {
        const h = Math.max((d.revenue / maxRev) * 100, 2)
        return (
          <div key={i} className="flex-1 group relative">
            <div className="bg-blue-600/60 rounded-t hover:bg-blue-500/80 transition-all cursor-pointer"
              style={{ height: `${h}%` }} />
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:block bg-slate-700 text-white text-xs p-1.5 rounded whitespace-nowrap z-10">
              {d.date}: ${d.revenue.toFixed(0)}
            </div>
          </div>
        )
      })}
    </div>
  )
}

const renderPieSegments = (counts: Record<string, number>, total: number) => {
  if (total === 0) {
    return <circle cx="18" cy="18" r="15.9" fill="none" stroke="#334155" strokeWidth="3" />
  }

  const colors: Record<string, string> = { basic: '#22c55e', professional: '#3b82f6', enterprise: '#a855f7' }
  const segments: JSX.Element[] = []
  let offset = 0

  Object.entries(counts).forEach(([tier, count]) => {
    if (count === 0) return
    const pct = (count / total) * 100
    const dashArray = `${pct} ${100 - pct}`
    segments.push(
      <circle key={tier} cx="18" cy="18" r="15.9" fill="none"
        stroke={colors[tier] || '#64748b'} strokeWidth="3"
        strokeDasharray={dashArray} strokeDashoffset={-offset}
        className="transition-all duration-500" />
    )
    offset += pct
  })

  return <>{segments}</>
}

export default AdminDashboard
