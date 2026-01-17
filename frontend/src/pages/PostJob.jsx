import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Checkbox } from "../components/ui/checkbox";
import { TRADE_CODES } from "../components/TradeBadge";
import { toast } from "sonner";
import { Loader2, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

const CERTIFICATIONS = [
  "OSHA 10",
  "OSHA 30",
  "First Aid/CPR",
  "Forklift Certified",
  "Scaffolding Certified",
  "Lead Paint Certified",
  "Asbestos Awareness",
  "Confined Space Entry"
];

export default function PostJob() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    trade_codes: [],
    location: "",
    city: "",
    state: "",
    pay_rate: "",
    pay_type: "hourly",
    duration: "",
    certifications_required: [],
    experience_years: 0
  });

  const handleTradeCodeToggle = (code) => {
    setFormData((prev) => ({
      ...prev,
      trade_codes: prev.trade_codes.includes(code)
        ? prev.trade_codes.filter((c) => c !== code)
        : [...prev.trade_codes, code]
    }));
  };

  const handleCertToggle = (cert) => {
    setFormData((prev) => ({
      ...prev,
      certifications_required: prev.certifications_required.includes(cert)
        ? prev.certifications_required.filter((c) => c !== cert)
        : [...prev.certifications_required, cert]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.trade_codes.length === 0) {
      toast.error("Please select at least one trade code");
      return;
    }

    setLoading(true);
    try {
      await api.post("/jobs", formData);
      toast.success("Job posted successfully!");
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to post job");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link to="/dashboard" className="inline-flex items-center text-slate-600 hover:text-slate-900 mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Dashboard
        </Link>

        <Card className="border border-slate-200 rounded-sm">
          <CardHeader>
            <CardTitle className="text-2xl font-bold font-['Oswald'] uppercase tracking-tight">
              Post a Job
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6" data-testid="post-job-form">
              {/* Title */}
              <div className="space-y-2">
                <Label htmlFor="title">Job Title *</Label>
                <Input
                  id="title"
                  placeholder="e.g., Drywall Installer Needed"
                  className="rounded-sm"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                  data-testid="job-title"
                />
              </div>

              {/* Description */}
              <div className="space-y-2">
                <Label htmlFor="description">Job Description *</Label>
                <Textarea
                  id="description"
                  placeholder="Describe the job requirements, responsibilities, and any other details..."
                  className="rounded-sm min-h-[150px]"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  data-testid="job-description"
                />
              </div>

              {/* Trade Codes */}
              <div className="space-y-2">
                <Label>Trade Codes * (Select all that apply)</Label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {Object.entries(TRADE_CODES).map(([code, name]) => (
                    <div
                      key={code}
                      className={`flex items-center space-x-2 p-3 border rounded-sm cursor-pointer transition-colors ${
                        formData.trade_codes.includes(code)
                          ? "border-orange-500 bg-orange-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                      onClick={() => handleTradeCodeToggle(code)}
                      data-testid={`trade-code-${code}`}
                    >
                      <Checkbox
                        checked={formData.trade_codes.includes(code)}
                        onCheckedChange={() => handleTradeCodeToggle(code)}
                      />
                      <span className="text-sm">{code} - {name}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Location */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="location">Site/Address *</Label>
                  <Input
                    id="location"
                    placeholder="123 Main St"
                    className="rounded-sm"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    required
                    data-testid="job-location"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="city">City *</Label>
                  <Input
                    id="city"
                    placeholder="Houston"
                    className="rounded-sm"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    required
                    data-testid="job-city"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="state">State *</Label>
                  <Input
                    id="state"
                    placeholder="TX"
                    className="rounded-sm"
                    value={formData.state}
                    onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                    required
                    data-testid="job-state"
                  />
                </div>
              </div>

              {/* Pay */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="pay_rate">Pay Rate *</Label>
                  <Input
                    id="pay_rate"
                    placeholder="25"
                    className="rounded-sm"
                    value={formData.pay_rate}
                    onChange={(e) => setFormData({ ...formData, pay_rate: e.target.value })}
                    required
                    data-testid="job-pay-rate"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pay_type">Pay Type *</Label>
                  <Select
                    value={formData.pay_type}
                    onValueChange={(value) => setFormData({ ...formData, pay_type: value })}
                  >
                    <SelectTrigger className="rounded-sm" data-testid="job-pay-type">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hourly">Hourly</SelectItem>
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem value="project">Per Project</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="duration">Duration *</Label>
                  <Input
                    id="duration"
                    placeholder="2 weeks"
                    className="rounded-sm"
                    value={formData.duration}
                    onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                    required
                    data-testid="job-duration"
                  />
                </div>
              </div>

              {/* Experience */}
              <div className="space-y-2">
                <Label htmlFor="experience">Minimum Years of Experience</Label>
                <Select
                  value={String(formData.experience_years)}
                  onValueChange={(value) => setFormData({ ...formData, experience_years: parseInt(value) })}
                >
                  <SelectTrigger className="rounded-sm w-48" data-testid="job-experience">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="0">No minimum</SelectItem>
                    <SelectItem value="1">1+ years</SelectItem>
                    <SelectItem value="2">2+ years</SelectItem>
                    <SelectItem value="3">3+ years</SelectItem>
                    <SelectItem value="5">5+ years</SelectItem>
                    <SelectItem value="10">10+ years</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Certifications */}
              <div className="space-y-2">
                <Label>Required Certifications (Optional)</Label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {CERTIFICATIONS.map((cert) => (
                    <div
                      key={cert}
                      className={`flex items-center space-x-2 p-2 border rounded-sm cursor-pointer transition-colors ${
                        formData.certifications_required.includes(cert)
                          ? "border-orange-500 bg-orange-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                      onClick={() => handleCertToggle(cert)}
                    >
                      <Checkbox
                        checked={formData.certifications_required.includes(cert)}
                        onCheckedChange={() => handleCertToggle(cert)}
                      />
                      <span className="text-xs">{cert}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Submit */}
              <div className="flex gap-4 pt-4">
                <Button
                  type="submit"
                  className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm flex-1"
                  disabled={loading}
                  data-testid="submit-job"
                >
                  {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                  Post Job
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  className="rounded-sm"
                  onClick={() => navigate("/dashboard")}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      <Footer />
    </div>
  );
}
