import { useEffect, useState, createContext, useContext } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { Toaster, toast } from "sonner";

// Pages
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AuthCallback from "./pages/AuthCallback";
import Dashboard from "./pages/Dashboard";
import JobBoard from "./pages/JobBoard";
import JobDetail from "./pages/JobDetail";
import PostJob from "./pages/PostJob";
import WorkerProfiles from "./pages/WorkerProfiles";
import ProfileDetail from "./pages/ProfileDetail";
import CreateProfile from "./pages/CreateProfile";
import Shop from "./pages/Shop";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import CheckoutSuccess from "./pages/CheckoutSuccess";
import MarketData from "./pages/MarketData";
import MarketDataSuccess from "./pages/MarketDataSuccess";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

// Auth Context
export const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

// API instance
export const api = axios.create({
  baseURL: API,
  withCredentials: true,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Protected Route Component
const ProtectedRoute = ({ children, requiredType = null }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredType && user.user_type !== requiredType) {
    toast.error(`This page requires ${requiredType} access`);
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// App Router with session_id detection
function AppRouter() {
  const location = useLocation();
  
  // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
  // Check URL fragment for session_id (Emergent OAuth callback)
  if (location.hash?.includes('session_id=')) {
    return <AuthCallback />;
  }

  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      
      {/* Job Board - Public */}
      <Route path="/jobs" element={<JobBoard />} />
      <Route path="/jobs/:jobId" element={<JobDetail />} />
      
      {/* Worker Profiles - Public */}
      <Route path="/workers" element={<WorkerProfiles />} />
      <Route path="/workers/:profileId" element={<ProfileDetail />} />
      
      {/* Shop - Public */}
      <Route path="/shop" element={<Shop />} />
      <Route path="/shop/:productId" element={<ProductDetail />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/checkout/success" element={<CheckoutSuccess />} />
      
      {/* Market Data - Public */}
      <Route path="/market-data" element={<MarketData />} />
      <Route path="/market-data/success" element={<MarketDataSuccess />} />
      
      {/* Protected Routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      <Route path="/post-job" element={
        <ProtectedRoute requiredType="contractor">
          <PostJob />
        </ProtectedRoute>
      } />
      <Route path="/create-profile" element={
        <ProtectedRoute requiredType="subcontractor">
          <CreateProfile />
        </ProtectedRoute>
      } />
      
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

// Auth Provider
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get("/auth/me");
      setUser(response.data);
    } catch (error) {
      setUser(null);
      localStorage.removeItem("token");
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", response.data.access_token);
    setUser(response.data.user);
    return response.data;
  };

  const register = async (data) => {
    const response = await api.post("/auth/register", data);
    localStorage.setItem("token", response.data.access_token);
    setUser(response.data.user);
    return response.data;
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout");
    } catch (error) {
      console.error("Logout error:", error);
    }
    localStorage.removeItem("token");
    setUser(null);
  };

  const updateUserType = async (userType) => {
    await api.put("/auth/update-type", { user_type: userType });
    setUser({ ...user, user_type: userType });
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, login, register, logout, checkAuth, updateUserType }}>
      {children}
    </AuthContext.Provider>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <AppRouter />
          <Toaster position="top-right" richColors closeButton />
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
