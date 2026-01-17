import { useState, useEffect } from "react";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { toast } from "sonner";
import { Check, BarChart3, Loader2 } from "lucide-react";

export default function MarketData() {
  const [tiers, setTiers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [subscribingTier, setSubscribingTier] = useState(null);

  useEffect(() => {
    fetchTiers();
  }, []);

  const fetchTiers = async () => {
    try {
      const response = await api.get("/market-data/tiers");
      setTiers(response.data);
    } catch (error) {
      console.error("Error fetching tiers:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (tierId) => {
    setSubscribingTier(tierId);
    try {
      const response = await api.post("/market-data/subscribe", {
        tier_id: tierId,
        origin_url: window.location.origin
      });
      window.location.href = response.data.url;
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to start subscription");
      setSubscribingTier(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50" data-testid="market-data-page">
      <Navbar />
      
      {/* Header */}
      <div className="bg-gradient-to-br from-slate-900 to-slate-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/30 mb-4">
            For Enterprise
          </Badge>
          <h1 className="text-4xl md:text-5xl font-bold font-['Oswald'] uppercase tracking-tight mb-4">
            Market Data Analytics
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Comprehensive construction industry intelligence to power your business decisions
          </p>
        </div>
      </div>

      {/* Tiers */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="spinner"></div>
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-8">
            {tiers.map((tier, index) => (
              <Card 
                key={tier.tier_id}
                className={`border rounded-sm relative ${
                  index === 1 
                    ? "border-2 border-orange-500 shadow-lg scale-105" 
                    : "border-slate-200"
                }`}
                data-testid={`tier-card-${tier.tier_id}`}
              >
                {index === 1 && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-orange-500 text-white">MOST POPULAR</Badge>
                  </div>
                )}
                <CardContent className="p-8">
                  <div className="text-center mb-6">
                    <div className="w-14 h-14 bg-slate-100 rounded-sm flex items-center justify-center mx-auto mb-4">
                      <BarChart3 className={`w-7 h-7 ${index === 1 ? "text-orange-500" : "text-slate-600"}`} />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 font-['Oswald'] uppercase mb-1">
                      {tier.name}
                    </h3>
                    <p className="text-sm text-slate-600">{tier.description}</p>
                  </div>

                  <div className="text-center mb-6">
                    <span className="text-4xl font-bold text-slate-900">${tier.price.toFixed(0)}</span>
                    <span className="text-slate-500">/{tier.billing_period}</span>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {tier.features.map((feature) => (
                      <li key={feature} className="flex items-start gap-2 text-sm">
                        <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                        <span className="text-slate-600">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <Button
                    onClick={() => handleSubscribe(tier.tier_id)}
                    disabled={subscribingTier === tier.tier_id}
                    className={`w-full rounded-sm py-6 ${
                      index === 1 
                        ? "bg-orange-500 hover:bg-orange-600 text-white" 
                        : "bg-slate-900 hover:bg-slate-800 text-white"
                    }`}
                    data-testid={`subscribe-${tier.tier_id}`}
                  >
                    {subscribingTier === tier.tier_id ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : null}
                    Subscribe Now
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Features Section */}
        <div className="mt-20 text-center">
          <h2 className="text-2xl font-bold text-slate-900 font-['Oswald'] uppercase mb-8">
            What's Included
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { title: "Labor Trends", desc: "Regional and national workforce analytics" },
              { title: "Wage Data", desc: "Real-time compensation benchmarks" },
              { title: "Market Reports", desc: "Monthly industry insights" },
              { title: "Custom Analysis", desc: "Tailored data for your needs" }
            ].map((item) => (
              <div key={item.title} className="bg-white p-6 border border-slate-200 rounded-sm">
                <h4 className="font-semibold text-slate-900 mb-2">{item.title}</h4>
                <p className="text-sm text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
