import { Link } from "react-router-dom";
import { useAuth } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { ArrowRight, Briefcase, Users, ShoppingBag, BarChart3, CheckCircle, Shield, Clock } from "lucide-react";

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      {/* Hero Section */}
      <section className="hero-section text-white py-20 md:py-32 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="animate-fade-in-up">
              <span className="inline-block px-4 py-1 bg-orange-500/20 text-orange-400 text-sm font-medium rounded-sm mb-6 uppercase tracking-wider">
                The Pro's Network
              </span>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight mb-6 font-['Oswald'] uppercase leading-tight">
                Connect With Skilled 
                <span className="text-orange-500"> Tradespeople</span>
              </h1>
              <p className="text-lg text-slate-300 mb-8 max-w-lg leading-relaxed">
                The premier platform for contractors seeking subcontractors and skilled workers looking for their next opportunity. Built by professionals, for professionals.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to={user ? "/dashboard" : "/register"}>
                  <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm px-8 py-6 text-lg font-medium uppercase tracking-wide" data-testid="hero-cta-primary">
                    Get Started
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </Button>
                </Link>
                <Link to="/jobs">
                  <Button variant="outline" className="border-2 border-white text-white hover:bg-white hover:text-slate-900 rounded-sm px-8 py-6 text-lg font-medium uppercase tracking-wide" data-testid="hero-cta-secondary">
                    Browse Jobs
                  </Button>
                </Link>
              </div>
            </div>
            <div className="hidden md:block animate-fade-in-up animation-delay-200">
              <img 
                src="https://images.unsplash.com/photo-1702392183172-17fdef8002b4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBkcnl3YWxsJTIwY29udHJhY3RvciUyMHdvcmtpbmd8ZW58MHx8fHwxNzY4NjM4OTg2fDA&ixlib=rb-4.1.0&q=85"
                alt="Professional contractor at work"
                className="rounded-sm shadow-2xl w-full h-[400px] object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: "500+", label: "Active Jobs" },
              { value: "2,000+", label: "Skilled Workers" },
              { value: "50+", label: "Trade Codes" },
              { value: "98%", label: "Satisfaction" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-slate-900 font-['Oswald']">{stat.value}</div>
                <div className="text-sm text-slate-500 uppercase tracking-wider mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight mb-4">
              Everything You Need
            </h2>
            <p className="text-slate-600 max-w-2xl mx-auto">
              From finding skilled workers to purchasing professional tools, we've got you covered.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Job Board */}
            <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors group" data-testid="service-jobs">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center mb-4 group-hover:bg-orange-500/10 transition-colors">
                  <Briefcase className="w-6 h-6 text-slate-900 group-hover:text-orange-500 transition-colors" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2 font-['Oswald'] uppercase">Job Board</h3>
                <p className="text-slate-600 text-sm mb-4">Find or post jobs by trade code, location, and pay rate.</p>
                <Link to="/jobs" className="text-orange-500 font-medium text-sm flex items-center gap-1 hover:gap-2 transition-all">
                  Browse Jobs <ArrowRight className="w-4 h-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Worker Profiles */}
            <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors group" data-testid="service-workers">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center mb-4 group-hover:bg-orange-500/10 transition-colors">
                  <Users className="w-6 h-6 text-slate-900 group-hover:text-orange-500 transition-colors" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2 font-['Oswald'] uppercase">Worker Profiles</h3>
                <p className="text-slate-600 text-sm mb-4">Browse skilled subcontractors by trade, experience, and availability.</p>
                <Link to="/workers" className="text-orange-500 font-medium text-sm flex items-center gap-1 hover:gap-2 transition-all">
                  Find Workers <ArrowRight className="w-4 h-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Pro Shop */}
            <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors group" data-testid="service-shop">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center mb-4 group-hover:bg-orange-500/10 transition-colors">
                  <ShoppingBag className="w-6 h-6 text-slate-900 group-hover:text-orange-500 transition-colors" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2 font-['Oswald'] uppercase">Pro Shop</h3>
                <p className="text-slate-600 text-sm mb-4">Professional-grade tools and supplies for contractors.</p>
                <Link to="/shop" className="text-orange-500 font-medium text-sm flex items-center gap-1 hover:gap-2 transition-all">
                  Shop Now <ArrowRight className="w-4 h-4" />
                </Link>
              </CardContent>
            </Card>

            {/* Market Data */}
            <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors group" data-testid="service-market-data">
              <CardContent className="p-6">
                <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center mb-4 group-hover:bg-orange-500/10 transition-colors">
                  <BarChart3 className="w-6 h-6 text-slate-900 group-hover:text-orange-500 transition-colors" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2 font-['Oswald'] uppercase">Market Data</h3>
                <p className="text-slate-600 text-sm mb-4">Construction industry analytics and market intelligence.</p>
                <Link to="/market-data" className="text-orange-500 font-medium text-sm flex items-center gap-1 hover:gap-2 transition-all">
                  View Tiers <ArrowRight className="w-4 h-4" />
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight mb-4">
              How It Works
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* For Contractors */}
            <div className="bg-slate-50 p-8 rounded-sm border border-slate-200">
              <h3 className="text-xl font-bold text-slate-900 font-['Oswald'] uppercase mb-6 flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-orange-500" />
                For Contractors
              </h3>
              <div className="space-y-4">
                {[
                  { step: "1", text: "Post your job with trade codes, location, and requirements" },
                  { step: "2", text: "Browse qualified subcontractor profiles" },
                  { step: "3", text: "Contact our team to connect with workers" },
                  { step: "4", text: "Build your project with skilled professionals" },
                ].map((item) => (
                  <div key={item.step} className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-slate-900 rounded-sm flex items-center justify-center flex-shrink-0">
                      <span className="text-white font-bold text-sm">{item.step}</span>
                    </div>
                    <p className="text-slate-600 pt-1">{item.text}</p>
                  </div>
                ))}
              </div>
              <Link to="/register" className="mt-6 inline-block">
                <Button className="bg-slate-900 hover:bg-slate-800 text-white rounded-sm" data-testid="contractor-cta">
                  Register as Contractor
                </Button>
              </Link>
            </div>

            {/* For Workers */}
            <div className="bg-slate-50 p-8 rounded-sm border border-slate-200">
              <h3 className="text-xl font-bold text-slate-900 font-['Oswald'] uppercase mb-6 flex items-center gap-2">
                <Users className="w-5 h-5 text-orange-500" />
                For Subcontractors
              </h3>
              <div className="space-y-4">
                {[
                  { step: "1", text: "Create your professional profile with skills and experience" },
                  { step: "2", text: "Browse available job opportunities" },
                  { step: "3", text: "Get matched with contractors through our team" },
                  { step: "4", text: "Start working on projects that match your skills" },
                ].map((item) => (
                  <div key={item.step} className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-orange-500 rounded-sm flex items-center justify-center flex-shrink-0">
                      <span className="text-white font-bold text-sm">{item.step}</span>
                    </div>
                    <p className="text-slate-600 pt-1">{item.text}</p>
                  </div>
                ))}
              </div>
              <Link to="/register" className="mt-6 inline-block">
                <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm" data-testid="worker-cta">
                  Register as Subcontractor
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Badges */}
      <section className="py-16 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Shield, title: "Verified Profiles", desc: "All workers and contractors are verified for quality" },
              { icon: Clock, title: "Quick Matching", desc: "Our team connects you with the right people fast" },
              { icon: CheckCircle, title: "Quality Guaranteed", desc: "We stand behind every connection we make" },
            ].map((item) => (
              <div key={item.title} className="flex items-start gap-4">
                <div className="w-12 h-12 bg-orange-500/20 rounded-sm flex items-center justify-center flex-shrink-0">
                  <item.icon className="w-6 h-6 text-orange-500" />
                </div>
                <div>
                  <h4 className="font-semibold mb-1 font-['Oswald'] uppercase">{item.title}</h4>
                  <p className="text-slate-400 text-sm">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight mb-4">
            Ready to Build Your Team?
          </h2>
          <p className="text-slate-600 max-w-xl mx-auto mb-8">
            Join thousands of contractors and skilled workers who trust HDrywall Repair for their workforce needs.
          </p>
          <Link to={user ? "/dashboard" : "/register"}>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm px-8 py-6 text-lg font-medium uppercase tracking-wide" data-testid="final-cta">
              Get Started Today
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  );
}
