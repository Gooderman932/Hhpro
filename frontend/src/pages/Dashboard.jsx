import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth, api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { TradeBadge } from "../components/TradeBadge";
import { Briefcase, Users, Plus, MapPin, Clock, DollarSign, Edit } from "lucide-react";
import { toast } from "sonner";

export default function Dashboard() {
  const { user, updateUserType } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [user]);

  const fetchData = async () => {
    try {
      if (user?.user_type === "contractor") {
        const response = await api.get("/my-jobs");
        setJobs(response.data);
      } else if (user?.user_type === "subcontractor") {
        const response = await api.get("/my-profile");
        setProfile(response.data);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSwitchType = async (newType) => {
    try {
      await updateUserType(newType);
      toast.success(`Switched to ${newType} account`);
      fetchData();
    } catch (error) {
      toast.error("Failed to switch account type");
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

  return (
    <div className="min-h-screen bg-slate-50" data-testid="dashboard">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight">
              Dashboard
            </h1>
            <p className="text-slate-600 mt-1">
              Welcome back, {user?.name}
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex items-center gap-3">
            <Badge variant="outline" className="capitalize px-3 py-1">
              {user?.user_type}
            </Badge>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleSwitchType(user?.user_type === "contractor" ? "subcontractor" : "contractor")}
              data-testid="switch-type-btn"
            >
              Switch to {user?.user_type === "contractor" ? "Subcontractor" : "Contractor"}
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {user?.user_type === "contractor" ? (
            <>
              <Link to="/post-job">
                <Card className="bg-orange-500 text-white border-0 rounded-sm hover:bg-orange-600 transition-colors cursor-pointer" data-testid="quick-post-job">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className="w-12 h-12 bg-white/20 rounded-sm flex items-center justify-center">
                      <Plus className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-semibold font-['Oswald'] uppercase">Post a Job</h3>
                      <p className="text-sm text-orange-100">Find skilled workers</p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
              <Link to="/workers">
                <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors cursor-pointer" data-testid="quick-find-workers">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center">
                      <Users className="w-6 h-6 text-slate-900" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-900 font-['Oswald'] uppercase">Find Workers</h3>
                      <p className="text-sm text-slate-600">Browse profiles</p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            </>
          ) : (
            <>
              <Link to="/create-profile">
                <Card className="bg-orange-500 text-white border-0 rounded-sm hover:bg-orange-600 transition-colors cursor-pointer" data-testid="quick-create-profile">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className="w-12 h-12 bg-white/20 rounded-sm flex items-center justify-center">
                      {profile ? <Edit className="w-6 h-6" /> : <Plus className="w-6 h-6" />}
                    </div>
                    <div>
                      <h3 className="font-semibold font-['Oswald'] uppercase">
                        {profile ? "Edit Profile" : "Create Profile"}
                      </h3>
                      <p className="text-sm text-orange-100">Showcase your skills</p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
              <Link to="/jobs">
                <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors cursor-pointer" data-testid="quick-find-jobs">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center">
                      <Briefcase className="w-6 h-6 text-slate-900" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-900 font-['Oswald'] uppercase">Find Jobs</h3>
                      <p className="text-sm text-slate-600">Browse opportunities</p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            </>
          )}
          <Link to="/shop">
            <Card className="bg-white border border-slate-200 rounded-sm hover:border-orange-500 transition-colors cursor-pointer" data-testid="quick-shop">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-12 h-12 bg-slate-100 rounded-sm flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-slate-900" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 font-['Oswald'] uppercase">Pro Shop</h3>
                  <p className="text-sm text-slate-600">Tools & supplies</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Content based on user type */}
        {user?.user_type === "contractor" ? (
          <Card className="border border-slate-200 rounded-sm">
            <CardHeader>
              <CardTitle className="font-['Oswald'] uppercase tracking-tight flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-orange-500" />
                My Job Listings ({jobs.length})
              </CardTitle>
            </CardHeader>
            <CardContent>
              {jobs.length === 0 ? (
                <div className="text-center py-12">
                  <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                  <p className="text-slate-600 mb-4">You haven't posted any jobs yet</p>
                  <Link to="/post-job">
                    <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm" data-testid="empty-post-job">
                      Post Your First Job
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {jobs.map((job) => (
                    <Link to={`/jobs/${job.job_id}`} key={job.job_id}>
                      <div className="p-4 border border-slate-200 rounded-sm hover:border-orange-500 transition-colors" data-testid={`job-item-${job.job_id}`}>
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-semibold text-slate-900">{job.title}</h3>
                          <Badge className={`status-${job.status} text-xs`}>{job.status}</Badge>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-2">
                          {job.trade_codes.map((code) => (
                            <TradeBadge key={code} code={code} showCode={false} />
                          ))}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-slate-600">
                          <span className="flex items-center gap-1">
                            <MapPin className="w-4 h-4" />
                            {job.city}, {job.state}
                          </span>
                          <span className="flex items-center gap-1">
                            <DollarSign className="w-4 h-4" />
                            {job.pay_rate}/{job.pay_type}
                          </span>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        ) : (
          <Card className="border border-slate-200 rounded-sm">
            <CardHeader>
              <CardTitle className="font-['Oswald'] uppercase tracking-tight flex items-center gap-2">
                <Users className="w-5 h-5 text-orange-500" />
                My Profile
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!profile ? (
                <div className="text-center py-12">
                  <Users className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                  <p className="text-slate-600 mb-4">Create your profile to get discovered by contractors</p>
                  <Link to="/create-profile">
                    <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm" data-testid="empty-create-profile">
                      Create Your Profile
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4" data-testid="profile-preview">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-xl font-semibold text-slate-900">{profile.headline}</h3>
                      <p className="text-slate-600 flex items-center gap-1 mt-1">
                        <MapPin className="w-4 h-4" />
                        {profile.city}, {profile.state}
                      </p>
                    </div>
                    <Badge className={`status-${profile.status}`}>{profile.status}</Badge>
                  </div>
                  <p className="text-slate-600">{profile.bio}</p>
                  <div className="flex flex-wrap gap-2">
                    {profile.trade_codes.map((code) => (
                      <TradeBadge key={code} code={code} />
                    ))}
                  </div>
                  <div className="flex items-center gap-6 text-sm text-slate-600">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {profile.experience_years} years experience
                    </span>
                    <span className="capitalize">{profile.availability.replace("_", " ")} availability</span>
                  </div>
                  <Link to="/create-profile">
                    <Button variant="outline" className="rounded-sm" data-testid="edit-profile-btn">
                      <Edit className="w-4 h-4 mr-2" />
                      Edit Profile
                    </Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>

      <Footer />
    </div>
  );
}
