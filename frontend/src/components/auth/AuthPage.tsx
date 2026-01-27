import { useState } from 'react'
import { useNavigate, useSearchParams, Link } from 'react-router-dom'
import { LogIn, UserPlus, Loader2 } from 'lucide-react'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs'
import { login, register } from '../../services/api'

export const AuthPage = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const redirectUrl = searchParams.get('redirect') || '/'

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Login form state
  const [loginEmail, setLoginEmail] = useState('')
  const [loginPassword, setLoginPassword] = useState('')

  // Register form state
  const [registerEmail, setRegisterEmail] = useState('')
  const [registerPassword, setRegisterPassword] = useState('')
  const [registerName, setRegisterName] = useState('')

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const tokenData = await login(loginEmail, loginPassword)
      localStorage.setItem('token', tokenData.access_token)
      navigate(redirectUrl)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      await register(registerEmail, registerPassword, registerName)
      // Auto-login after registration
      const tokenData = await login(registerEmail, registerPassword)
      localStorage.setItem('token', tokenData.access_token)
      navigate(redirectUrl)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center py-16 px-4">
      <Card className="max-w-md w-full bg-slate-900/50 backdrop-blur border-slate-700">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl text-white">Welcome</CardTitle>
          <CardDescription className="text-slate-400">
            Sign in to access Market Data Intelligence
          </CardDescription>
        </CardHeader>

        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-slate-800">
              <TabsTrigger value="login" className="data-[state=active]:bg-slate-700">
                <LogIn className="h-4 w-4 mr-2" />
                Sign In
              </TabsTrigger>
              <TabsTrigger value="register" className="data-[state=active]:bg-slate-700">
                <UserPlus className="h-4 w-4 mr-2" />
                Register
              </TabsTrigger>
            </TabsList>

            <TabsContent value="login">
              <form onSubmit={handleLogin} className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label htmlFor="login-email" className="text-slate-300">Email</Label>
                  <Input
                    id="login-email"
                    data-testid="login-email-input"
                    type="email"
                    placeholder="you@example.com"
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    required
                    className="bg-slate-800 border-slate-600 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="login-password" className="text-slate-300">Password</Label>
                  <Input
                    id="login-password"
                    data-testid="login-password-input"
                    type="password"
                    placeholder="••••••••"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    required
                    className="bg-slate-800 border-slate-600 text-white"
                  />
                </div>
                <Button
                  type="submit"
                  data-testid="login-submit-btn"
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Signing in...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </Button>
              </form>
            </TabsContent>

            <TabsContent value="register">
              <form onSubmit={handleRegister} className="space-y-4 mt-4">
                <div className="space-y-2">
                  <Label htmlFor="register-name" className="text-slate-300">Full Name</Label>
                  <Input
                    id="register-name"
                    data-testid="register-name-input"
                    type="text"
                    placeholder="John Doe"
                    value={registerName}
                    onChange={(e) => setRegisterName(e.target.value)}
                    required
                    className="bg-slate-800 border-slate-600 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-email" className="text-slate-300">Email</Label>
                  <Input
                    id="register-email"
                    data-testid="register-email-input"
                    type="email"
                    placeholder="you@example.com"
                    value={registerEmail}
                    onChange={(e) => setRegisterEmail(e.target.value)}
                    required
                    className="bg-slate-800 border-slate-600 text-white"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="register-password" className="text-slate-300">Password</Label>
                  <Input
                    id="register-password"
                    data-testid="register-password-input"
                    type="password"
                    placeholder="••••••••"
                    value={registerPassword}
                    onChange={(e) => setRegisterPassword(e.target.value)}
                    required
                    minLength={6}
                    className="bg-slate-800 border-slate-600 text-white"
                  />
                </div>
                <Button
                  type="submit"
                  data-testid="register-submit-btn"
                  className="w-full bg-green-600 hover:bg-green-700"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Creating account...
                    </>
                  ) : (
                    'Create Account'
                  )}
                </Button>
              </form>
            </TabsContent>
          </Tabs>

          <div className="mt-6 text-center">
            <Link to="/" className="text-slate-400 hover:text-blue-400 text-sm">
              ← Back to Home
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AuthPage
