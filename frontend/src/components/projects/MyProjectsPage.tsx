import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Trash2, Edit2, Loader2, Briefcase, DollarSign, MapPin, Calendar, X } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import api from '../../services/api'

interface UserProject {
  id: number
  name: string
  description: string
  value: number
  sector: string
  status: string
  city: string
  state: string
  bid_date: string | null
  bidding_competitors: string[]
  ai_insights: string
  ai_category: string
  created_at: string
}

const SECTORS = ['Commercial', 'Residential', 'Healthcare', 'Education', 'Industrial', 'Retail']
const STATUSES = ['bidding', 'won', 'lost', 'in_progress', 'completed']
const STATES = ['AZ', 'CA', 'CO', 'FL', 'GA', 'NV', 'OH', 'TN', 'TX', 'WA']

export const MyProjectsPage = () => {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [editingProject, setEditingProject] = useState<UserProject | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    value: '',
    sector: '',
    status: 'bidding',
    city: '',
    state: '',
    bid_date: '',
    bidding_competitors: ''
  })

  const { data: projects, isLoading } = useQuery<UserProject[]>({
    queryKey: ['my-projects'],
    queryFn: async () => {
      const response = await api.get('/my-projects')
      return response.data
    }
  })

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/my-projects', {
        ...data,
        value: data.value ? parseFloat(data.value) : null,
        bidding_competitors: data.bidding_competitors ? data.bidding_competitors.split(',').map((c: string) => c.trim()) : []
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-projects'] })
      resetForm()
    }
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/my-projects/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-projects'] })
    }
  })

  const resetForm = () => {
    setFormData({
      name: '', description: '', value: '', sector: '', status: 'bidding',
      city: '', state: '', bid_date: '', bidding_competitors: ''
    })
    setShowForm(false)
    setEditingProject(null)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData)
  }

  const totalValue = projects?.reduce((sum, p) => sum + (p.value || 0), 0) || 0
  const wonProjects = projects?.filter(p => p.status === 'won').length || 0

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 pt-20 flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 pt-20 px-4 pb-12">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-white">My Projects</h1>
            <p className="mt-1 text-slate-400">Track and manage your projects</p>
          </div>
          <Button onClick={() => setShowForm(true)} className="bg-blue-600 hover:bg-blue-700">
            <Plus className="h-4 w-4 mr-2" />
            Add Project
          </Button>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">Total Projects</p>
                  <p className="text-3xl font-bold text-white">{projects?.length || 0}</p>
                </div>
                <Briefcase className="h-10 w-10 text-blue-500 opacity-50" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">Total Value</p>
                  <p className="text-3xl font-bold text-green-400">${(totalValue / 1000000).toFixed(1)}M</p>
                </div>
                <DollarSign className="h-10 w-10 text-green-500 opacity-50" />
              </div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">Won Projects</p>
                  <p className="text-3xl font-bold text-purple-400">{wonProjects}</p>
                </div>
                <div className="text-purple-500 text-4xl">🏆</div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Add/Edit Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
            <Card className="bg-slate-900 border-slate-700 w-full max-w-lg max-h-[90vh] overflow-y-auto">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Add New Project</CardTitle>
                  <button onClick={resetForm} className="text-slate-400 hover:text-white">
                    <X className="h-5 w-5" />
                  </button>
                </div>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="text-slate-400 text-sm">Project Name *</label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData(f => ({ ...f, name: e.target.value }))}
                      className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      required
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-slate-400 text-sm">Value ($)</label>
                      <input
                        type="number"
                        value={formData.value}
                        onChange={(e) => setFormData(f => ({ ...f, value: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                        placeholder="1000000"
                      />
                    </div>
                    <div>
                      <label className="text-slate-400 text-sm">Sector</label>
                      <select
                        value={formData.sector}
                        onChange={(e) => setFormData(f => ({ ...f, sector: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      >
                        <option value="">Select...</option>
                        {SECTORS.map(s => <option key={s} value={s}>{s}</option>)}
                      </select>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-slate-400 text-sm">City</label>
                      <input
                        type="text"
                        value={formData.city}
                        onChange={(e) => setFormData(f => ({ ...f, city: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      />
                    </div>
                    <div>
                      <label className="text-slate-400 text-sm">State</label>
                      <select
                        value={formData.state}
                        onChange={(e) => setFormData(f => ({ ...f, state: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      >
                        <option value="">Select...</option>
                        {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                      </select>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-slate-400 text-sm">Status</label>
                      <select
                        value={formData.status}
                        onChange={(e) => setFormData(f => ({ ...f, status: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      >
                        {STATUSES.map(s => (
                          <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1).replace('_', ' ')}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="text-slate-400 text-sm">Bid Date</label>
                      <input
                        type="date"
                        value={formData.bid_date}
                        onChange={(e) => setFormData(f => ({ ...f, bid_date: e.target.value }))}
                        className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-slate-400 text-sm">Bidding Competitors (comma-separated)</label>
                    <input
                      type="text"
                      value={formData.bidding_competitors}
                      onChange={(e) => setFormData(f => ({ ...f, bidding_competitors: e.target.value }))}
                      className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      placeholder="Company A, Company B"
                    />
                  </div>
                  
                  <div>
                    <label className="text-slate-400 text-sm">Description</label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData(f => ({ ...f, description: e.target.value }))}
                      className="w-full mt-1 p-2 bg-slate-800 border border-slate-600 rounded text-white"
                      rows={3}
                    />
                  </div>
                  
                  <div className="flex gap-3 pt-4">
                    <Button type="button" variant="outline" onClick={resetForm} className="border-slate-600">
                      Cancel
                    </Button>
                    <Button 
                      type="submit" 
                      disabled={createMutation.isPending}
                      className="flex-1 bg-blue-600 hover:bg-blue-700"
                    >
                      {createMutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Save Project'}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Projects List */}
        <div className="space-y-4">
          {projects?.map(project => (
            <Card key={project.id} className="bg-slate-900 border-slate-700">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold text-white">{project.name}</h3>
                      <span className={`px-2 py-0.5 rounded text-xs ${
                        project.status === 'won' ? 'bg-green-500/20 text-green-400' :
                        project.status === 'lost' ? 'bg-red-500/20 text-red-400' :
                        project.status === 'bidding' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {project.status.replace('_', ' ')}
                      </span>
                    </div>
                    
                    <div className="flex flex-wrap gap-4 mt-2 text-sm text-slate-400">
                      {project.city && project.state && (
                        <span className="flex items-center gap-1">
                          <MapPin className="h-4 w-4" />
                          {project.city}, {project.state}
                        </span>
                      )}
                      {project.sector && (
                        <span className="flex items-center gap-1">
                          <Briefcase className="h-4 w-4" />
                          {project.sector}
                        </span>
                      )}
                      {project.bid_date && (
                        <span className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          Bid: {new Date(project.bid_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    
                    {project.ai_insights && (
                      <p className="mt-2 text-sm text-blue-400 bg-blue-500/10 p-2 rounded">
                        💡 {project.ai_insights}
                      </p>
                    )}
                    
                    {project.bidding_competitors?.length > 0 && (
                      <div className="mt-2">
                        <span className="text-slate-500 text-sm">Competitors: </span>
                        {project.bidding_competitors.map((c, i) => (
                          <span key={i} className="text-slate-400 text-sm">
                            {c}{i < project.bidding_competitors.length - 1 ? ', ' : ''}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex items-start gap-4">
                    {project.value && (
                      <div className="text-right">
                        <p className="text-2xl font-bold text-green-400">
                          ${(project.value / 1000000).toFixed(1)}M
                        </p>
                      </div>
                    )}
                    <button
                      onClick={() => deleteMutation.mutate(project.id)}
                      className="text-slate-500 hover:text-red-400 p-1"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {(!projects || projects.length === 0) && (
          <Card className="bg-slate-900 border-slate-700">
            <CardContent className="py-12 text-center">
              <Briefcase className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <p className="text-slate-400">No projects yet</p>
              <p className="text-slate-500 text-sm mt-1">Add your first project to start tracking</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default MyProjectsPage
