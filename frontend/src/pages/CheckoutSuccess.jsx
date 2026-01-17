import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { CheckCircle, XCircle, Loader2, ShoppingBag, ArrowRight } from "lucide-react";

export default function CheckoutSuccess() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id");
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

      // Continue polling
      setPollCount((prev) => prev + 1);
      setTimeout(pollPaymentStatus, pollInterval);
    } catch (error) {
      console.error("Error checking payment status:", error);
      setStatus("error");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50" data-testid="checkout-success">
      <Navbar />
      
      <div className="max-w-2xl mx-auto px-4 py-16">
        <Card className="border border-slate-200 rounded-sm">
          <CardContent className="py-12 text-center">
            {status === "loading" && (
              <>
                <Loader2 className="w-16 h-16 text-orange-500 mx-auto mb-4 animate-spin" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  Processing Payment
                </h1>
                <p className="text-slate-600">Please wait while we confirm your payment...</p>
              </>
            )}

            {status === "success" && (
              <>
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  Payment Successful!
                </h1>
                <p className="text-slate-600 mb-6">
                  Thank you for your order. We'll process it right away.
                </p>
                {paymentData && (
                  <div className="bg-slate-50 p-4 rounded-sm mb-6 text-left">
                    <p className="text-sm text-slate-600">
                      <span className="font-medium">Amount Paid:</span> ${(paymentData.amount_total / 100).toFixed(2)} {paymentData.currency?.toUpperCase()}
                    </p>
                  </div>
                )}
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to="/shop">
                    <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm">
                      <ShoppingBag className="w-4 h-4 mr-2" />
                      Continue Shopping
                    </Button>
                  </Link>
                  <Link to="/dashboard">
                    <Button variant="outline" className="rounded-sm">
                      Go to Dashboard
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </>
            )}

            {(status === "error" || status === "expired" || status === "timeout") && (
              <>
                <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                <h1 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-2">
                  {status === "expired" ? "Payment Expired" : "Payment Issue"}
                </h1>
                <p className="text-slate-600 mb-6">
                  {status === "expired"
                    ? "Your payment session has expired. Please try again."
                    : "We couldn't confirm your payment. Please check your email for confirmation."}
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link to="/cart">
                    <Button className="bg-slate-900 hover:bg-slate-800 text-white rounded-sm">
                      Return to Cart
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
