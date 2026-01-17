import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
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
import { Badge } from "../components/ui/badge";
import { TRADE_CODES } from "../components/TradeBadge";
import { toast } from "sonner";
import { Loader2, ArrowLeft, X } from "lucide-react";

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

export default function CreateProfile() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [existingProfile, setExistingProfile] = useState(null);
  const [skillInput, setSkillInput] = useState("");
  const [formData, setFormData] = useState({
    headline: "",
    bio: "",
    trade_codes: [],
    skills: [],
    experience_years: 1,
    certifications: [],
    location: "",
    city: "",
    state: "",
    availability: "immediate",
    hourly_rate_min: "",
    hourly_rate_max: ""
  });

  useEffect(() => {
    fetchExistingProfile();
  }, []);

  const fetchExistingProfile = async () => {
    try {
      const response = await api.get("/my-profile");
      if (response.data) {
        setExistingProfile(response.data);
        setFormData({
          ...response.data,
          hourly_rate_min: response.data.hourly_rate_min || "",
          hourly_rate_max: response.data.hourly_rate_max || ""
        });
      }
    } catch (error) {
      // No existing profile
    }
  };

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
      certifications: prev.certifications.includes(cert)
        ? prev.certifications.filter((c) => c !== cert)
        : [...prev.certifications, cert]
    }));
  };

  const addSkill = () => {
    if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
      setFormData((prev) => ({
        ...prev,
        skills: [...prev.skills, skillInput.trim()]
      }));
      setSkillInput("");
    }
  };

  const removeSkill = (skill) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((s) => s !== skill)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.trade_codes.length === 0) {
      toast.error("Please select at least one trade code");
      return;
    }
    if (formData.skills.length === 0) {
      toast.error("Please add at least one skill");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        ...formData,
        hourly_rate_min: formData.hourly_rate_min ? parseFloat(formData.hourly_rate_min) : null,
        hourly_rate_max: formData.hourly_rate_max ? parseFloat(formData.hourly_rate_max) : null
      };

      if (existingProfile) {
        await api.put("/profiles", payload);
        toast.success("Profile updated successfully!");
      } else {
        await api.post("/profiles", payload);
        toast.success("Profile created successfully!");
      }
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to save profile");
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
              {existingProfile ? "Edit Profile" : "Create Your Profile"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6" data-testid="create-profile-form">
              {/* Headline */}
              <div className="space-y-2">
                <Label htmlFor="headline">Professional Headline *</Label>
                <Input
                  id="headline"
                  placeholder="e.g., Experienced Drywall Installer & Finisher"
                  className="rounded-sm"
                  value={formData.headline}
                  onChange={(e) => setFormData({ ...formData, headline: e.target.value })}
                  required
                  data-testid="profile-headline"
                />
              </div>

              {/* Bio */}
              <div className="space-y-2">
                <Label htmlFor="bio">About You *</Label>
                <Textarea
                  id="bio"
                  placeholder="Tell contractors about your experience, specialties, and work ethic..."
                  className="rounded-sm min-h-[120px]"
                  value={formData.bio}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  required
                  data-testid="profile-bio"
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

              {/* Skills */}
              <div className="space-y-2">
                <Label>Skills *</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="Add a skill (e.g., Taping, Texturing, Framing)"
                    className="rounded-sm"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
                    data-testid="skill-input"
                  />
                  <Button type="button" onClick={addSkill} variant="outline" className="rounded-sm">
                    Add
                  </Button>
                </div>
                {formData.skills.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {formData.skills.map((skill) => (
                      <Badge
                        key={skill}
                        variant="secondary"
                        className="flex items-center gap-1 cursor-pointer"
                        onClick={() => removeSkill(skill)}
                      >
                        {skill}
                        <X className="w-3 h-3" />
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              {/* Experience */}
              <div className="space-y-2">
                <Label>Years of Experience *</Label>
                <Select
                  value={String(formData.experience_years)}
                  onValueChange={(value) => setFormData({ ...formData, experience_years: parseInt(value) })}
                >
                  <SelectTrigger className="rounded-sm w-48" data-testid="profile-experience">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30].map((year) => (
                      <SelectItem key={year} value={String(year)}>{year} {year === 1 ? "year" : "years"}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Location */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="location">Area/Neighborhood *</Label>
                  <Input
                    id="location"
                    placeholder="Downtown, Northside, etc."
                    className="rounded-sm"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    required
                    data-testid="profile-location"
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
                    data-testid="profile-city"
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
                    data-testid="profile-state"
                  />
                </div>
              </div>

              {/* Availability & Rate */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Availability *</Label>
                  <Select
                    value={formData.availability}
                    onValueChange={(value) => setFormData({ ...formData, availability: value })}
                  >
                    <SelectTrigger className="rounded-sm" data-testid="profile-availability">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="immediate">Immediate</SelectItem>
                      <SelectItem value="1_week">1 Week</SelectItem>
                      <SelectItem value="2_weeks">2 Weeks</SelectItem>
                      <SelectItem value="flexible">Flexible</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rate_min">Min Rate ($/hr)</Label>
                  <Input
                    id="rate_min"
                    type="number"
                    placeholder="20"
                    className="rounded-sm"
                    value={formData.hourly_rate_min}
                    onChange={(e) => setFormData({ ...formData, hourly_rate_min: e.target.value })}
                    data-testid="profile-rate-min"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rate_max">Max Rate ($/hr)</Label>
                  <Input
                    id="rate_max"
                    type="number"
                    placeholder="35"
                    className="rounded-sm"
                    value={formData.hourly_rate_max}
                    onChange={(e) => setFormData({ ...formData, hourly_rate_max: e.target.value })}
                    data-testid="profile-rate-max"
                  />
                </div>
              </div>

              {/* Certifications */}
              <div className="space-y-2">
                <Label>Certifications (Optional)</Label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {CERTIFICATIONS.map((cert) => (
                    <div
                      key={cert}
                      className={`flex items-center space-x-2 p-2 border rounded-sm cursor-pointer transition-colors ${
                        formData.certifications.includes(cert)
                          ? "border-orange-500 bg-orange-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                      onClick={() => handleCertToggle(cert)}
                    >
                      <Checkbox
                        checked={formData.certifications.includes(cert)}
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
                  data-testid="submit-profile"
                >
                  {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                  {existingProfile ? "Update Profile" : "Create Profile"}
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
