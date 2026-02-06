import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { FileText, MapPin, DollarSign, Building2, Filter, Search, Loader2, AlertCircle, Star } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

interface Permit {
  permit_number: string
  permit_type: string
  sector: string
  project_name: string
  description: string
  estimated_value: number
  address: string
  city: string
  state: string
  owner_name: string
  contractor_name: string
  issue_date: string
  match_score?: number
  match_reasons?: string[]
}

const STATES = ['AZ', 'CA', 'CO', 'FL', 'GA', 'NV', 'OH', 'TN', 'TX', 'WA']
const PERMIT_TYPES = ['commercial', 'residential', 'industrial', 'renovation']

export const PermitsPage = () => {
  const [filters, setFilters] = useState({
    state: '',
    permit_type: '',
    min_value: '',
    max_value: ''
  })
  const [showFilters, setShowFilters] = useState(false)

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['permits', filters],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (filters.state) params.append('state', filters.state)
      if (filters.permit_type) params.append('permit_type', filters.permit_type)
      if (filters.min_value) params.append('min_value', filters.min_value)
      if (filters.max_value) params.append('max_value', filters.max_value)
      params.append('limit', '50')
      
      const response = await api.get(`/permits?${params.toString()}`)
      return response.data
    }
  })

  const permits: Permit[] = data?.permits || []
  const tierLimit = data?.tier_limit || 25
  const isConfigured = data?.configured !== false

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
              <CardTitle className="text-white">Error Loading Permits</CardTitle>
              <CardDescription className="text-slate-400">
                Please check your subscription status
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    )
  }

  if (!isConfigured || permits.length === 0) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12" data-testid="permits-page">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-white mb-6">Construction Permits</h1>
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-16 text-center">
              <FileText className="h-14 w-14 text-slate-700 mx-auto mb-4" />
              <h3 className="text-white text-lg font-medium mb-2">
                {!isConfigured ? 'Permit Data Source Not Connected' : 'No Permits Found'}
              </h3>
              <p className="text-slate-400 text-sm max-w-md mx-auto mb-4">
                {!isConfigured
                  ? 'Connect a permit data source to see real construction permits in your service area. This pulls live data from government building departments.'
                  : 'No permits match your current filters and service area. Try adjusting your filters or updating your profile.'}
              </p>
              {!isConfigured && (
                <div className="bg-slate-800 p-4 rounded-lg max-w-sm mx-auto text-left">
                  <p className="text-slate-300 text-sm font-medium mb-2">Setup Required</p>
                  <p className="text-slate-400 text-xs mb-1">1. Get an API key from a permit data provider</p>
                  <p className="text-slate-400 text-xs mb-1">2. Set <code className="text-blue-400">PERMIT_API_KEY</code> in environment</p>
                  <p className="text-slate-400 text-xs">3. Permits will auto-populate for your area</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-white">Construction Permits</h1>
            <p className="mt-1 text-slate-400">
              {permits.length} permits found • Tier limit: {tierLimit}/month
            </p>
          </div>
          <Button
            onClick={() => setShowFilters(!showFilters)}
            variant="outline"
            className="border-slate-600 text-slate-300"
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>

        {/* Filters */}
        {showFilters && (
          <Card className="bg-slate-900 border-slate-700 mb-6">
            <CardContent className="pt-6">
              <div className="grid md:grid-cols-4 gap-4">
                <div>
                  <label className="text-slate-400 text-sm">State</label>
                  <select
                    value={filters.state}
                    onChange={(e) => setFilters(f => ({ ...f, state: e.target.value }))}
                    className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                  >
                    <option value="">All States</option>
                    {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-slate-400 text-sm">Type</label>
                  <select
                    value={filters.permit_type}
                    onChange={(e) => setFilters(f => ({ ...f, permit_type: e.target.value }))}
                    className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                  >
                    <option value="">All Types</option>
                    {PERMIT_TYPES.map(t => (
                      <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-slate-400 text-sm">Min Value</label>
                  <select
                    value={filters.min_value}
                    onChange={(e) => setFilters(f => ({ ...f, min_value: e.target.value }))}
                    className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                  >
                    <option value="">Any</option>
                    <option value="100000">$100K+</option>
                    <option value="500000">$500K+</option>
                    <option value="1000000">$1M+</option>
                    <option value="5000000">$5M+</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <Button onClick={() => refetch()} className="w-full bg-blue-600 hover:bg-blue-700">
                    <Search className="h-4 w-4 mr-2" />
                    Apply Filters
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Permits Grid */}
        <div className="grid gap-4">
          {permits.map((permit) => (
            <Card 
              key={permit.permit_number} 
              className={`bg-slate-900 border-slate-700 ${
                permit.match_score && permit.match_score > 70 ? 'border-l-4 border-l-green-500' : ''
              }`}
            >
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold text-white">{permit.project_name}</h3>
                      {permit.match_score && permit.match_score > 70 && (
                        <span className="flex items-center gap-1 px-2 py-0.5 bg-green-500/20 text-green-400 text-xs rounded-full">
                          <Star className="h-3 w-3" />
                          {permit.match_score}% Match
                        </span>
                      )}
                    </div>
                    
                    <div className="flex flex-wrap gap-4 mt-2 text-sm text-slate-400">
                      <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {permit.city}, {permit.state}
                      </span>
                      <span className="flex items-center gap-1">
                        <Building2 className="h-4 w-4" />
                        {permit.sector}
                      </span>
                      <span className="flex items-center gap-1">
                        <FileText className="h-4 w-4" />
                        {permit.permit_type}
                      </span>
                    </div>
                    
                    {permit.match_reasons && permit.match_reasons.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-2">
                        {permit.match_reasons.map((reason, i) => (
                          <span key={i} className="px-2 py-1 bg-blue-500/10 text-blue-400 text-xs rounded">
                            {reason}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    <div className="mt-3 text-sm">
                      <p className="text-slate-500">
                        <span className="text-slate-400">Owner:</span> {permit.owner_name}
                      </p>
                      <p className="text-slate-500">
                        <span className="text-slate-400">Contractor:</span> {permit.contractor_name}
                      </p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="flex items-center gap-1 text-green-400">
                      <DollarSign className="h-5 w-5" />
                      <span className="text-2xl font-bold">
                        {(permit.estimated_value / 1000000).toFixed(1)}M
                      </span>
                    </div>
                    <p className="text-slate-500 text-sm mt-1">
                      {new Date(permit.issue_date).toLocaleDateString()}
                    </p>
                    <p className="text-slate-600 text-xs mt-1">
                      #{permit.permit_number}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {permits.length === 0 && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-12 text-center">
              <FileText className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No permits found matching your criteria</p>
              <p className="text-slate-500 text-sm mt-1">Try adjusting your filters</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default PermitsPage
