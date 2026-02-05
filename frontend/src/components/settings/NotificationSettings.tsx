import { useState, useEffect } from 'react'
import { Bell, Mail, Clock, Filter, Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
// @ts-ignore - Switch component exists but lacks type definitions
import { Switch } from '../ui/switch'
import {
  getNotificationPreferences,
  updateNotificationPreferences,
  getNotificationOptions,
  sendTestNotification,
  getNotificationHistory,
  NotificationPreferences
} from '../../services/api'

interface NotificationOption {
  id: string
  name: string
  description: string
}

interface NotificationHistory {
  id: number
  type: string
  subject: string
  status: string
  projects_count: number
  sent_at: string | null
  created_at: string
}

export const NotificationSettings = () => {
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    email_enabled: false,
    frequency: 'daily',
    min_project_value: 1000000,
    preferred_sectors: [],
    preferred_regions: [],
    match_type: 'any'
  })
  const [options, setOptions] = useState<{
    sectors: string[]
    regions: string[]
    frequencies: NotificationOption[]
    match_types: NotificationOption[]
  } | null>(null)
  const [history, setHistory] = useState<NotificationHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [testing, setTesting] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [prefs, opts, hist] = await Promise.all([
        getNotificationPreferences(),
        getNotificationOptions(),
        getNotificationHistory(10)
      ])
      setPreferences(prefs)
      setOptions(opts)
      setHistory(hist)
    } catch (err) {
      console.error('Failed to load notification settings:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    setMessage(null)
    try {
      await updateNotificationPreferences(preferences)
      setMessage({ type: 'success', text: 'Notification preferences saved!' })
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to save preferences' })
    } finally {
      setSaving(false)
    }
  }

  const handleTestNotification = async () => {
    setTesting(true)
    setMessage(null)
    try {
      const result = await sendTestNotification()
      if (result.status === 'success') {
        setMessage({ type: 'success', text: `Test email sent to your inbox!` })
        // Refresh history
        const hist = await getNotificationHistory(10)
        setHistory(hist)
      } else {
        setMessage({ type: 'error', text: result.error || 'Failed to send test notification' })
      }
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to send test notification' })
    } finally {
      setTesting(false)
    }
  }

  const toggleSector = (sector: string) => {
    setPreferences(prev => ({
      ...prev,
      preferred_sectors: prev.preferred_sectors.includes(sector)
        ? prev.preferred_sectors.filter(s => s !== sector)
        : [...prev.preferred_sectors, sector]
    }))
  }

  const toggleRegion = (region: string) => {
    setPreferences(prev => ({
      ...prev,
      preferred_regions: prev.preferred_regions.includes(region)
        ? prev.preferred_regions.filter(r => r !== region)
        : [...prev.preferred_regions, region]
    }))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Notification Settings</h1>
          <p className="mt-2 text-slate-400">
            Configure alerts for projects matching your preferences
          </p>
        </div>

        {message && (
          <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
            message.type === 'success' ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'
          }`}>
            {message.type === 'success' ? (
              <CheckCircle className="h-5 w-5 text-green-400" />
            ) : (
              <AlertCircle className="h-5 w-5 text-red-400" />
            )}
            <span className={message.type === 'success' ? 'text-green-400' : 'text-red-400'}>
              {message.text}
            </span>
          </div>
        )}

        <div className="space-y-6">
          {/* Enable/Disable */}
          <Card className="bg-slate-900 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Bell className="h-5 w-5 text-blue-500" />
                Email Notifications
              </CardTitle>
              <CardDescription className="text-slate-400">
                Receive email alerts when new projects match your criteria
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-white font-medium">Enable Notifications</div>
                  <div className="text-sm text-slate-400">Get notified about matching projects</div>
                </div>
                <Switch
                  checked={preferences.email_enabled}
                  onCheckedChange={(checked: boolean) => setPreferences(prev => ({ ...prev, email_enabled: checked }))}
                />
              </div>
            </CardContent>
          </Card>

          {preferences.email_enabled && (
            <>
              {/* Frequency */}
              <Card className="bg-slate-900 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Clock className="h-5 w-5 text-purple-500" />
                    Notification Frequency
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-3">
                    {options?.frequencies.map((freq) => (
                      <button
                        key={freq.id}
                        onClick={() => setPreferences(prev => ({ ...prev, frequency: freq.id }))}
                        className={`p-4 rounded-lg border text-left transition ${
                          preferences.frequency === freq.id
                            ? 'border-blue-500 bg-blue-500/10'
                            : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                        }`}
                      >
                        <div className={`font-medium ${preferences.frequency === freq.id ? 'text-blue-400' : 'text-white'}`}>
                          {freq.name}
                        </div>
                        <div className="text-xs text-slate-400 mt-1">{freq.description}</div>
                      </button>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Value Threshold */}
              <Card className="bg-slate-900 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Filter className="h-5 w-5 text-green-500" />
                    Project Criteria
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Set minimum value and preferred sectors/regions
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Min Value */}
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Minimum Project Value
                    </label>
                    <select
                      value={preferences.min_project_value}
                      onChange={(e) => setPreferences(prev => ({ ...prev, min_project_value: Number(e.target.value) }))}
                      className="w-full p-3 bg-slate-800 border border-slate-600 rounded-lg text-white"
                    >
                      <option value={500000}>$500K+</option>
                      <option value={1000000}>$1M+</option>
                      <option value={5000000}>$5M+</option>
                      <option value={10000000}>$10M+</option>
                      <option value={25000000}>$25M+</option>
                      <option value={50000000}>$50M+</option>
                    </select>
                  </div>

                  {/* Sectors */}
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Preferred Sectors
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {options?.sectors.map((sector) => (
                        <button
                          key={sector}
                          onClick={() => toggleSector(sector)}
                          className={`px-3 py-1.5 rounded-full text-sm transition ${
                            preferences.preferred_sectors.includes(sector)
                              ? 'bg-blue-600 text-white'
                              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                          }`}
                        >
                          {sector}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Regions */}
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Preferred Regions
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {options?.regions.map((region) => (
                        <button
                          key={region}
                          onClick={() => toggleRegion(region)}
                          className={`px-3 py-1.5 rounded-full text-sm transition ${
                            preferences.preferred_regions.includes(region)
                              ? 'bg-green-600 text-white'
                              : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                          }`}
                        >
                          {region}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Match Type */}
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Match Logic
                    </label>
                    <div className="grid md:grid-cols-2 gap-3">
                      {options?.match_types.map((type) => (
                        <button
                          key={type.id}
                          onClick={() => setPreferences(prev => ({ ...prev, match_type: type.id }))}
                          className={`p-3 rounded-lg border text-left transition ${
                            preferences.match_type === type.id
                              ? 'border-purple-500 bg-purple-500/10'
                              : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                          }`}
                        >
                          <div className={`font-medium ${preferences.match_type === type.id ? 'text-purple-400' : 'text-white'}`}>
                            {type.name}
                          </div>
                          <div className="text-xs text-slate-400 mt-1">{type.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {/* Actions */}
          <div className="flex gap-4">
            <Button
              onClick={handleSave}
              disabled={saving}
              className="bg-blue-600 hover:bg-blue-700"
              data-testid="save-preferences-btn"
            >
              {saving ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : null}
              Save Preferences
            </Button>
            {preferences.email_enabled && (
              <Button
                onClick={handleTestNotification}
                disabled={testing}
                variant="outline"
                className="border-slate-600 text-slate-300 hover:bg-slate-800"
                data-testid="test-notification-btn"
              >
                {testing ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Send className="h-4 w-4 mr-2" />}
                Send Test Email
              </Button>
            )}
          </div>

          {/* History */}
          {history.length > 0 && (
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Mail className="h-5 w-5 text-amber-500" />
                  Notification History
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {history.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-3 bg-slate-800 rounded-lg"
                    >
                      <div>
                        <div className="text-white text-sm">{item.subject}</div>
                        <div className="text-slate-400 text-xs">
                          {item.projects_count} project{item.projects_count !== 1 ? 's' : ''} • {item.type}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`text-sm ${
                          item.status === 'sent' ? 'text-green-400' : 
                          item.status === 'failed' ? 'text-red-400' : 'text-yellow-400'
                        }`}>
                          {item.status}
                        </div>
                        <div className="text-slate-500 text-xs">
                          {item.sent_at ? new Date(item.sent_at).toLocaleDateString() : 'Pending'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default NotificationSettings
