import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { TradeBadge } from "../components/TradeBadge";
import { ArrowLeft, MapPin, Clock, Award, Mail, DollarSign, Calendar } from "lucide-react";

export default function ProfileDetail() {
  const { profileId } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, [profileId]);

  const fetchProfile = async () => {
    try {
      const response = await api.get(`/profiles/${profileId}`);
      setProfile(response.data);
    } catch (error) {
      console.error("Error fetching profile:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="flex items-center justify-center py-20">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">Profile not found</h1>
          <Link to="/workers">
            <Button variant="outline" className="rounded-sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Workers
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50" data-testid="profile-detail">
      <Navbar />
      
      {/* Header */}
      <div className="bg-slate-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link to="/workers" className="inline-flex items-center text-slate-400 hover:text-white mb-4 transition-colors">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Workers
          </Link>
          <div className="flex items-start gap-6">
            <div className="w-20 h-20 bg-slate-700 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-3xl font-bold text-white">
                {profile.name?.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <h1 className="text-3xl font-bold font-['Oswald'] uppercase tracking-tight mb-1">
                {profile.name}
              </h1>
              <p className="text-xl text-slate-300">{profile.headline}</p>
              <div className="flex items-center gap-4 mt-2 text-slate-400">
                <span className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {profile.city}, {profile.state}
                </span>
                <Badge className={`status-${profile.status}`}>{profile.status}</Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="md:col-span-2 space-y-6">
            <Card className="border border-slate-200 rounded-sm">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                  About
                </h2>
                <p className="text-slate-600 whitespace-pre-wrap">{profile.bio}</p>
              </CardContent>
            </Card>

            <Card className="border border-slate-200 rounded-sm">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                  Trade Codes
                </h2>
                <div className="flex flex-wrap gap-2">
                  {profile.trade_codes.map((code) => (
                    <TradeBadge key={code} code={code} />
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border border-slate-200 rounded-sm">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                  Skills
                </h2>
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="rounded-sm">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {profile.certifications.length > 0 && (
              <Card className="border border-slate-200 rounded-sm">
                <CardContent className="p-6">
                  <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                    Certifications
                  </h2>
                  <div className="flex flex-wrap gap-2">
                    {profile.certifications.map((cert) => (
                      <Badge key={cert} variant="outline" className="flex items-center gap-1">
                        <Award className="w-3 h-3" />
                        {cert}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="border border-slate-200 rounded-sm">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                  Details
                </h2>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <Clock className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Experience</p>
                      <p className="font-medium text-slate-900">{profile.experience_years} years</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Calendar className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Availability</p>
                      <p className="font-medium text-slate-900 capitalize">
                        {profile.availability.replace("_", " ")}
                      </p>
                    </div>
                  </div>
                  {(profile.hourly_rate_min || profile.hourly_rate_max) && (
                    <div className="flex items-start gap-3">
                      <DollarSign className="w-5 h-5 text-slate-400 mt-0.5" />
                      <div>
                        <p className="text-sm text-slate-500">Rate Range</p>
                        <p className="font-medium text-slate-900">
                          ${profile.hourly_rate_min || "—"}
                          {profile.hourly_rate_max && ` - $${profile.hourly_rate_max}`}/hr
                        </p>
                      </div>
                    </div>
                  )}
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Location</p>
                      <p className="font-medium text-slate-900">{profile.location}</p>
                      <p className="text-sm text-slate-600">{profile.city}, {profile.state}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-2 border-orange-500 rounded-sm bg-orange-50">
              <CardContent className="p-6 text-center">
                <Mail className="w-8 h-8 text-orange-500 mx-auto mb-3" />
                <h3 className="font-semibold text-slate-900 mb-2">Want to hire this worker?</h3>
                <p className="text-sm text-slate-600 mb-4">
                  Contact our team to connect with this subcontractor
                </p>
                <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white rounded-sm" data-testid="contact-btn">
                  Contact Us to Connect
                </Button>
                <p className="text-xs text-slate-500 mt-3">
                  info@hdrywallrepair.com
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
