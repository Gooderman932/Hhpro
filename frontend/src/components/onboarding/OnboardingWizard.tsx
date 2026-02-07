import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Check, ChevronRight, CreditCard, User, Database, FolderPlus, X, Loader2 } from 'lucide-react'
import { Card, CardContent } from '../ui/card'
import { Button } from '../ui/button'
import { getOnboardingStatus, skipOnboarding } from '../../services/api'

interface OnboardingStep {
  id: string
  title: string
  completed: boolean
  description: string
}

export const OnboardingWizard = () => {
  const navigate = useNavigate()
  const [steps, setSteps] = useState<OnboardingStep[]>([])
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(true)
  const [dismissed, setDismissed] = useState(false)

  useEffect(() => {
    const wasDismissed = sessionStorage.getItem('onboarding_dismissed')
    if (wasDismissed) {
      setDismissed(true)
      setLoading(false)
      return
    }

    getOnboardingStatus()
      .then(data => {
        setSteps(data.steps)
        setProgress(data.progress)
        if (data.onboarding_completed) setDismissed(true)
      })
      .catch(() => {
        // Only dismiss on 401/403, show wizard otherwise
        setSteps([
          { id: 'subscription', title: 'Choose a Plan', completed: false, description: 'Select a subscription tier' },
          { id: 'profile', title: 'Business Profile', completed: false, description: 'Tell us about your business' },
          { id: 'data_sources', title: 'Connect Data', completed: false, description: 'Connect external data sources' },
          { id: 'first_project', title: 'Add a Project', completed: false, description: 'Add your first project' }
        ])
      })
      .finally(() => setLoading(false))
  }, [])

  const handleDismiss = () => {
    sessionStorage.setItem('onboarding_dismissed', 'true')
    skipOnboarding().catch(() => {})
    setDismissed(true)
  }

  const stepActions: Record<string, { label: string; path: string }> = {
    subscription: { label: 'View Plans', path: '/pricing' },
    profile: { label: 'Complete Profile', path: '/onboarding' },
    data_sources: { label: 'Connect Data', path: '/settings' },
    first_project: { label: 'Add Project', path: '/my-projects' }
  }

  const stepIcons: Record<string, any> = {
    subscription: CreditCard,
    profile: User,
    data_sources: Database,
    first_project: FolderPlus
  }

  if (loading || dismissed || progress === 100) return null

  const nextStep = steps.find(s => !s.completed)

  return (
    <div className="mb-6" data-testid="onboarding-wizard">
      <Card className="bg-slate-900 border-slate-700 overflow-hidden">
        {/* Progress Bar */}
        <div className="h-1 bg-slate-800">
          <div
            className="h-1 bg-blue-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>

        <CardContent className="p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-white font-medium">Getting Started</h3>
              <p className="text-slate-500 text-xs">{progress}% complete</p>
            </div>
            <button
              onClick={handleDismiss}
              className="text-slate-500 hover:text-white transition p-1"
              data-testid="dismiss-wizard-btn"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {steps.map(step => {
              const Icon = stepIcons[step.id] || ChevronRight
              const action = stepActions[step.id]
              return (
                <button
                  key={step.id}
                  onClick={() => !step.completed && action && navigate(action.path)}
                  data-testid={`wizard-step-${step.id}`}
                  className={`p-3 rounded-lg text-left transition ${
                    step.completed
                      ? 'bg-green-500/10 border border-green-500/30'
                      : step.id === nextStep?.id
                        ? 'bg-blue-500/10 border border-blue-500/30 cursor-pointer hover:border-blue-500/60'
                        : 'bg-slate-800 border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    {step.completed ? (
                      <Check className="h-4 w-4 text-green-400" />
                    ) : (
                      <Icon className={`h-4 w-4 ${step.id === nextStep?.id ? 'text-blue-400' : 'text-slate-500'}`} />
                    )}
                    <span className={`text-sm font-medium ${step.completed ? 'text-green-400' : 'text-white'}`}>
                      {step.title}
                    </span>
                  </div>
                  <p className="text-slate-500 text-xs">{step.description}</p>
                  {!step.completed && step.id === nextStep?.id && action && (
                    <span className="text-blue-400 text-xs mt-1 inline-flex items-center gap-1">
                      {action.label} <ChevronRight className="h-3 w-3" />
                    </span>
                  )}
                </button>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default OnboardingWizard
