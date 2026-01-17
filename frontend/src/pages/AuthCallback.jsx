import { useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth, api } from "../App";
import { toast } from "sonner";

export default function AuthCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setUser } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    // Use ref to prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      // Extract session_id from URL fragment
      const hash = location.hash || window.location.hash;
      const params = new URLSearchParams(hash.replace('#', ''));
      const sessionId = params.get('session_id');

      if (!sessionId) {
        toast.error("No session found");
        navigate("/login");
        return;
      }

      try {
        // Exchange session_id for user data
        const response = await api.post("/auth/session", { session_id: sessionId });
        setUser(response.data);
        
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
        
        toast.success(`Welcome, ${response.data.name}!`);
        navigate("/dashboard", { replace: true, state: { user: response.data } });
      } catch (error) {
        console.error("Auth callback error:", error);
        toast.error("Authentication failed");
        navigate("/login");
      }
    };

    processAuth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="text-center">
        <div className="spinner mx-auto mb-4"></div>
        <p className="text-slate-600">Completing sign in...</p>
      </div>
    </div>
  );
}
