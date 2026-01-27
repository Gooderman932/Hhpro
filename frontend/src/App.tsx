import { useEffect, useState } from "react"
import "@/App.css"
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom"
import { Menu, X, LogOut, User, BarChart3 } from "lucide-react"
import { Button } from "./components/ui/button"
import { PricingPage } from "./components/pricing/PricingPage"
import { SubscriptionSuccess } from "./components/pricing/SubscriptionSuccess"
import { AuthPage } from "./components/auth/AuthPage"
import { getCurrentSubscription } from "./services/api"
import type { Subscription } from "./types/subscription"

// Navigation component
const Navigation = () => {
  const navigate = useNavigate()
  const [isOpen, setIsOpen] = useState(false)
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const isLoggedIn = !!localStorage.getItem('token')

  useEffect(() => {
    if (isLoggedIn) {
      getCurrentSubscription()
        .then(setSubscription)
        .catch(() => {})
    }
  }, [isLoggedIn])

  const handleLogout = () => {
    localStorage.removeItem('token')
    setSubscription(null)
    navigate('/')
    window.location.reload()
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-lg border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-blue-500" />
            <span className="text-xl font-bold text-white">HDrywall Pro</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/pricing" className="text-slate-300 hover:text-white transition">
              Pricing
            </Link>
            
            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                {subscription && (
                  <span className="text-sm text-green-400 bg-green-400/10 px-3 py-1 rounded-full">
                    {subscription.tier_name}
                  </span>
                )}
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="text-slate-300 hover:text-white"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </div>
            ) : (
              <Link to="/login">
                <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                  <User className="h-4 w-4 mr-2" />
                  Sign In
                </Button>
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-slate-300"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Nav */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-slate-800">
            <div className="flex flex-col space-y-4">
              <Link
                to="/pricing"
                className="text-slate-300 hover:text-white"
                onClick={() => setIsOpen(false)}
              >
                Pricing
              </Link>
              {isLoggedIn ? (
                <>
                  {subscription && (
                    <span className="text-sm text-green-400">
                      Plan: {subscription.tier_name}
                    </span>
                  )}
                  <button
                    onClick={handleLogout}
                    className="text-slate-300 hover:text-white text-left"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <Link
                  to="/login"
                  className="text-blue-400 hover:text-blue-300"
                  onClick={() => setIsOpen(false)}
                >
                  Sign In
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

// Home page component
const Home = () => {
  const navigate = useNavigate()
  const isLoggedIn = !!localStorage.getItem('token')

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      {/* Hero Section */}
      <div className="pt-32 pb-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6">
            Construction Market
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              {" "}Intelligence
            </span>
          </h1>
          <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
            Gain competitive advantage with real-time market analytics, competitor insights, 
            and demand forecasting for the construction industry.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              data-testid="hero-pricing-btn"
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 text-lg px-8"
              onClick={() => navigate('/pricing')}
            >
              View Pricing
            </Button>
            {!isLoggedIn && (
              <Button
                data-testid="hero-signin-btn"
                size="lg"
                variant="outline"
                className="border-slate-600 text-slate-300 hover:bg-slate-800 text-lg px-8"
                onClick={() => navigate('/login')}
              >
                Sign In
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 px-4 bg-slate-900/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            Why Choose HDrywall Pro?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Market Analytics",
                description: "Track regional trends, wage data, and project opportunities in real-time.",
                icon: "📊"
              },
              {
                title: "Competitor Intelligence",
                description: "Monitor competitor activity, win rates, and market positioning.",
                icon: "🎯"
              },
              {
                title: "Demand Forecasting",
                description: "Predict market demand by region and trade with AI-powered insights.",
                icon: "📈"
              }
            ].map((feature, idx) => (
              <div
                key={idx}
                className="p-6 bg-slate-800/50 rounded-xl border border-slate-700 hover:border-blue-500/50 transition"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to gain your competitive edge?
          </h2>
          <p className="text-slate-400 mb-8">
            Join hundreds of construction professionals using HDrywall Pro to win more projects.
          </p>
          <Button
            data-testid="cta-pricing-btn"
            size="lg"
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8"
            onClick={() => navigate('/pricing')}
          >
            Get Started Today
          </Button>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-slate-800">
        <div className="max-w-6xl mx-auto text-center text-slate-500 text-sm">
          <p>© 2025 HDrywall Pro. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/subscription/success" element={<SubscriptionSuccess />} />
        <Route path="/login" element={<AuthPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
