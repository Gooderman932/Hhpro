import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Building2, MapPin, Briefcase, Target, ArrowRight, Check, Loader2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

const BUSINESS_TYPES = [
  { id: 'gc', name: 'General Contractor', icon: '🏗️' },
  { id: 'subcontractor', name: 'Subcontractor', icon: '🔧' },
  { id: 'supplier', name: 'Material Supplier', icon: '📦' },
  { id: 'owner', name: 'Project Owner/Developer', icon: '🏢' },
  { id: 'other', name: 'Other', icon: '💼' }
]

const TRADES = [
  'Electrical', 'Plumbing', 'HVAC', 'Drywall', 'Roofing',
  'Concrete', 'Structural Steel', 'Flooring', 'Painting',
  'Landscaping', 'General Construction', 'Other'
]

const COMPANY_SIZES = [
  { id: '1-10', name: '1-10 employees' },
  { id: '11-50', name: '11-50 employees' },
  { id: '51-200', name: '51-200 employees' },
  { id: '200+', name: '200+ employees' }
]

const STATES = [
  'AZ', 'CA', 'CO', 'FL', 'GA', 'IL', 'NC', 'NV', 'NY', 'OH', 'PA', 'TN', 'TX', 'WA'
]

const SECTORS = [
  'Commercial', 'Residential', 'Healthcare', 'Education',
  'Industrial', 'Retail', 'Hospitality', 'Infrastructure'
]

export const Onboarding = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [profile, setProfile] = useState({
    business_type: '',
    trade_specialty: '',
    company_size: '',
    service_states: [] as string[],
    min_project_value: 100000,
    max_project_value: 10000000,
    preferred_sectors: [] as string[]
  })

  const toggleState = (state: string) => {
    setProfile(prev => ({
      ...prev,
      service_states: prev.service_states.includes(state)
        ? prev.service_states.filter(s => s !== state)
        : [...prev.service_states, state]
    }))
  }

  const toggleSector = (sector: string) => {
    setProfile(prev => ({
      ...prev,
      preferred_sectors: prev.preferred_sectors.includes(sector)
        ? prev.preferred_sectors.filter(s => s !== sector)
        : [...prev.preferred_sectors, sector]
    }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      await api.put('/profile', profile)
      navigate('/dashboard')
    } catch (err) {
      console.error('Failed to save profile:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white">Welcome to HHDrywall Pro</h1>
          <p className="mt-2 text-slate-400">Let's personalize your market intelligence experience</p>
          
          {/* Progress */}
          <div className="flex justify-center mt-6 gap-2">
            {[1, 2, 3, 4].map(s => (
              <div
                key={s}
                className={`w-12 h-1 rounded ${s <= step ? 'bg-blue-500' : 'bg-slate-700'}`}
              />
            ))}
          </div>
        </div>

        {/* Step 1: Business Type */}
        {step === 1 && (
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Building2 className="h-5 w-5 text-blue-500" />
                What type of business are you?
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {BUSINESS_TYPES.map(type => (
                <button
                  key={type.id}
                  onClick={() => setProfile(p => ({ ...p, business_type: type.id }))}
                  className={`w-full p-4 rounded-lg border text-left flex items-center gap-3 transition ${
                    profile.business_type === type.id
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                  }`}
                >
                  <span className="text-2xl">{type.icon}</span>
                  <span className={profile.business_type === type.id ? 'text-blue-400' : 'text-white'}>
                    {type.name}
                  </span>
                  {profile.business_type === type.id && (
                    <Check className="h-5 w-5 text-blue-400 ml-auto" />
                  )}
                </button>
              ))}
              
              <Button
                onClick={() => setStep(2)}
                disabled={!profile.business_type}
                className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
              >
                Continue <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Trade & Size */}
        {step === 2 && (
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Briefcase className="h-5 w-5 text-green-500" />
                Trade Specialty & Company Size
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="block text-white text-sm font-medium mb-3">Primary Trade</label>
                <div className="flex flex-wrap gap-2">
                  {TRADES.map(trade => (
                    <button
                      key={trade}
                      onClick={() => setProfile(p => ({ ...p, trade_specialty: trade.toLowerCase() }))}
                      className={`px-3 py-2 rounded-lg text-sm transition ${
                        profile.trade_specialty === trade.toLowerCase()
                          ? 'bg-green-600 text-white'
                          : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      {trade}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-white text-sm font-medium mb-3">Company Size</label>
                <div className="grid grid-cols-2 gap-3">
                  {COMPANY_SIZES.map(size => (
                    <button
                      key={size.id}
                      onClick={() => setProfile(p => ({ ...p, company_size: size.id }))}
                      className={`p-3 rounded-lg border text-center transition ${
                        profile.company_size === size.id
                          ? 'border-green-500 bg-green-500/10 text-green-400'
                          : 'border-slate-700 bg-slate-800 text-white hover:border-slate-600'
                      }`}
                    >
                      {size.name}
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => setStep(1)} className="border-slate-600">
                  Back
                </Button>
                <Button
                  onClick={() => setStep(3)}
                  disabled={!profile.trade_specialty || !profile.company_size}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Continue <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Service Area */}
        {step === 3 && (
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <MapPin className="h-5 w-5 text-purple-500" />
                Where do you operate?
              </CardTitle>
              <CardDescription className="text-slate-400">
                Select all states where you do business
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-2">
                {STATES.map(state => (
                  <button
                    key={state}
                    onClick={() => toggleState(state)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                      profile.service_states.includes(state)
                        ? 'bg-purple-600 text-white'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {state}
                  </button>
                ))}
              </div>
              
              <div className="pt-4">
                <label className="block text-white text-sm font-medium mb-3">Project Value Range</label>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-slate-400 text-xs">Minimum</label>
                    <select
                      value={profile.min_project_value}
                      onChange={(e) => setProfile(p => ({ ...p, min_project_value: Number(e.target.value) }))}
                      className="w-full p-2 bg-slate-800 border border-slate-600 rounded text-white"
                    >
                      <option value={50000}>$50K</option>
                      <option value={100000}>$100K</option>
                      <option value={250000}>$250K</option>
                      <option value={500000}>$500K</option>
                      <option value={1000000}>$1M</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-slate-400 text-xs">Maximum</label>
                    <select
                      value={profile.max_project_value}
                      onChange={(e) => setProfile(p => ({ ...p, max_project_value: Number(e.target.value) }))}
                      className="w-full p-2 bg-slate-800 border border-slate-600 rounded text-white"
                    >
                      <option value={1000000}>$1M</option>
                      <option value={5000000}>$5M</option>
                      <option value={10000000}>$10M</option>
                      <option value={25000000}>$25M</option>
                      <option value={50000000}>$50M+</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-3 pt-4">
                <Button variant="outline" onClick={() => setStep(2)} className="border-slate-600">
                  Back
                </Button>
                <Button
                  onClick={() => setStep(4)}
                  disabled={profile.service_states.length === 0}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  Continue <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 4: Preferred Sectors */}
        {step === 4 && (
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Target className="h-5 w-5 text-amber-500" />
                Target Sectors
              </CardTitle>
              <CardDescription className="text-slate-400">
                Select the project types you're interested in
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {SECTORS.map(sector => (
                  <button
                    key={sector}
                    onClick={() => toggleSector(sector)}
                    className={`p-4 rounded-lg border text-center transition ${
                      profile.preferred_sectors.includes(sector)
                        ? 'border-amber-500 bg-amber-500/10 text-amber-400'
                        : 'border-slate-700 bg-slate-800 text-white hover:border-slate-600'
                    }`}
                  >
                    {sector}
                  </button>
                ))}
              </div>
              
              <div className="flex gap-3 pt-4">
                <Button variant="outline" onClick={() => setStep(3)} className="border-slate-600">
                  Back
                </Button>
                <Button
                  onClick={handleSubmit}
                  disabled={loading || profile.preferred_sectors.length === 0}
                  className="flex-1 bg-green-600 hover:bg-green-700"
                >
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <>Complete Setup <Check className="h-4 w-4 ml-2" /></>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Onboarding
