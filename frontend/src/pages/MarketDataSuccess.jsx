import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { CheckCircle, XCircle, Loader2, BarChart3, ArrowRight } from "lucide-react";

export default function MarketDataSuccess() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const tierId = searchParams.get("tier");
  const [status, setStatus] = useState("loading");
  const [paymentData, setPaymentData] = useState(null);
  const [pollCount, setPollCount] = useState(0);

  useEffect(() => {
    if (sessionId) {
      pollPaymentStatus();
    } else {
      setStatus("error");
    }
  }, [sessionId]);

  const pollPaymentStatus = async () => {
    const maxAttempts = 5;
    const pollInterval = 2000;

    if (pollCount >= maxAttempts) {
      setStatus("timeout");
      return;
    }

    try {
      const response = await api.get(`/checkout/status/${sessionId}`);
      setPaymentData(response.data);

      if (response.data.payment_status === "paid") {
        setStatus("success");
        return;
      } else if (response.data.status === "expired") {
        setStatus("expired");
        return;
      }

      setPollCount((prev) => prev + 1);
      setTimeout(pollPaymentStatus, pollInterval);
    } catch (error) {
      console.error("Error checking payment status:", error);
      setStatus("error");
    }
  };

  const tierNames = {
    basic: "Basic Analytics",
    professional: "Professional Suite",
    enterprise: "Enterprise Platform"
  };

  return (
    <div className="min-h-screen bg-slate-50" data-testid="market-data-success">
      <Navbar />
      
      <div className="max-w-2xl mx-auto px-4 py-16">
        <Card className="border border-slate-200 rounded-sm">
          <CardContent className="py-12 text-center">
            {status === "loading" && (
              <>
                <Loader2 className="w-16 h-16 text-orange-500 mx-auto mb-4 animate-spin" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  Processing Subscription
                </h1>
                <p className="text-slate-600">Please wait while we confirm your subscription...</p>
              </>
            )}

            {status === "success" && (
              <>
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  Subscription Activated!
                </h1>
                <p className="text-slate-600 mb-6">
                  Welcome to {tierNames[tierId] || "Market Data Analytics"}. Your subscription is now active.
                </p>
                {paymentData && (
                  <div className="bg-slate-50 p-4 rounded-sm mb-6 text-left">
                    <p className="text-sm text-slate-600">
                      <span className="font-medium">Tier:</span> {tierNames[tierId] || tierId}
                    </p>
                    <p className="text-sm text-slate-600">
                      <span className="font-medium">Amount:</span> ${(paymentData.amount_total / 100).toFixed(2)}/month
                    </p>
                  </div>
                )}
                <div className="bg-orange-50 border border-orange-200 p-4 rounded-sm mb-6 text-left">
                  <h3 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-orange-500" />
                    What's Next?
                  </h3>
                  <p className="text-sm text-slate-600">
                    Our team will reach out within 24 hours to set up your analytics dashboard and provide your login credentials.
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to="/dashboard">
                    <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm">
                      Go to Dashboard
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                  <Link to="/">
                    <Button variant="outline" className="rounded-sm">
                      Return Home
                    </Button>
                  </Link>
                </div>
              </>
            )}

            {(status === "error" || status === "expired" || status === "timeout") && (
              <>
                <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  {status === "expired" ? "Session Expired" : "Subscription Issue"}
                </h1>
                <p className="text-slate-600 mb-6">
                  {status === "expired"
                    ? "Your session has expired. Please try subscribing again."
                    : "We couldn't confirm your subscription. Please contact support if you were charged."}
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to="/market-data">
                    <Button className="bg-slate-900 hover:bg-slate-800 text-white rounded-sm">
                      Try Again
                    </Button>
                  </Link>
                  <Link to="/">
                    <Button variant="outline" className="rounded-sm">
                      Go Home
                    </Button>
                  </Link>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      <Footer />
    </div>
  );
}
