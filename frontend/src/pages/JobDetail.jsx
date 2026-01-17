import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { TradeBadge } from "../components/TradeBadge";
import { ArrowLeft, MapPin, DollarSign, Clock, Calendar, Award, Briefcase, Mail } from "lucide-react";

export default function JobDetail() {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchJob();
  }, [jobId]);

  const fetchJob = async () => {
    try {
      const response = await api.get(`/jobs/${jobId}`);
      setJob(response.data);
    } catch (error) {
      console.error("Error fetching job:", error);
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

  if (!job) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">Job not found</h1>
          <Link to="/jobs">
            <Button variant="outline" className="rounded-sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Jobs
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50" data-testid="job-detail">
      <Navbar />
      
      {/* Header */}
      <div className="bg-slate-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link to="/jobs" className="inline-flex items-center text-slate-400 hover:text-white mb-4 transition-colors">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Job Board
          </Link>
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold font-['Oswald'] uppercase tracking-tight mb-2">
                {job.title}
              </h1>
              <p className="text-slate-400">Posted by {job.contractor_name}</p>
            </div>
            <div className="text-right">
              <div className="price-tag text-xl mb-2">
                ${job.pay_rate}
                <span className="text-sm font-normal">/{job.pay_type}</span>
              </div>
              <Badge className="status-active">{job.status}</Badge>
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
                  Job Description
                </h2>
                <p className="text-slate-600 whitespace-pre-wrap">{job.description}</p>
              </CardContent>
            </Card>

            <Card className="border border-slate-200 rounded-sm">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                  Trade Codes
                </h2>
                <div className="flex flex-wrap gap-2">
                  {job.trade_codes.map((code) => (
                    <TradeBadge key={code} code={code} />
                  ))}
                </div>
              </CardContent>
            </Card>

            {job.certifications_required.length > 0 && (
              <Card className="border border-slate-200 rounded-sm">
                <CardContent className="p-6">
                  <h2 className="text-lg font-semibold text-slate-900 mb-4 font-['Oswald'] uppercase">
                    Required Certifications
                  </h2>
                  <div className="flex flex-wrap gap-2">
                    {job.certifications_required.map((cert) => (
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
                  Job Details
                </h2>
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Location</p>
                      <p className="font-medium text-slate-900">{job.location}</p>
                      <p className="text-sm text-slate-600">{job.city}, {job.state}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Clock className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Duration</p>
                      <p className="font-medium text-slate-900">{job.duration}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <DollarSign className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Pay Rate</p>
                      <p className="font-medium text-slate-900">${job.pay_rate}/{job.pay_type}</p>
                    </div>
                  </div>
                  {job.experience_years > 0 && (
                    <div className="flex items-start gap-3">
                      <Briefcase className="w-5 h-5 text-slate-400 mt-0.5" />
                      <div>
                        <p className="text-sm text-slate-500">Experience</p>
                        <p className="font-medium text-slate-900">{job.experience_years}+ years required</p>
                      </div>
                    </div>
                  )}
                  <div className="flex items-start gap-3">
                    <Calendar className="w-5 h-5 text-slate-400 mt-0.5" />
                    <div>
                      <p className="text-sm text-slate-500">Posted</p>
                      <p className="font-medium text-slate-900">
                        {new Date(job.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-2 border-orange-500 rounded-sm bg-orange-50">
              <CardContent className="p-6 text-center">
                <Mail className="w-8 h-8 text-orange-500 mx-auto mb-3" />
                <h3 className="font-semibold text-slate-900 mb-2">Interested in this job?</h3>
                <p className="text-sm text-slate-600 mb-4">
                  Contact our team to connect with this contractor
                </p>
                <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white rounded-sm" data-testid="contact-btn">
                  Contact Us to Apply
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
