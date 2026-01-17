import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { TradeBadge, TRADE_CODES } from "../components/TradeBadge";
import { Search, MapPin, DollarSign, Clock, Briefcase, Filter } from "lucide-react";

export default function JobBoard() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    trade_code: "",
    state: "",
    city: ""
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.trade_code && filters.trade_code !== "all") params.append("trade_code", filters.trade_code);
      if (filters.state) params.append("state", filters.state);
      if (filters.city) params.append("city", filters.city);
      
      const response = await api.get(`/jobs?${params.toString()}`);
      setJobs(response.data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchJobs();
  };

  const clearFilters = () => {
    setFilters({ trade_code: "", state: "", city: "" });
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      {/* Header */}
      <div className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-bold font-['Oswald'] uppercase tracking-tight mb-2">
            Job Board
          </h1>
          <p className="text-slate-400">
            Find your next project from contractors across the country
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b border-slate-200 py-4 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <Select
                value={filters.trade_code}
                onValueChange={(value) => setFilters({ ...filters, trade_code: value })}
              >
                <SelectTrigger className="rounded-sm" data-testid="filter-trade">
                  <SelectValue placeholder="All Trade Codes" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Trade Codes</SelectItem>
                  {Object.entries(TRADE_CODES).map(([code, name]) => (
                    <SelectItem key={code} value={code}>{code} - {name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Input
              placeholder="State"
              className="md:w-40 rounded-sm"
              value={filters.state}
              onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              data-testid="filter-state"
            />
            <Input
              placeholder="City"
              className="md:w-40 rounded-sm"
              value={filters.city}
              onChange={(e) => setFilters({ ...filters, city: e.target.value })}
              data-testid="filter-city"
            />
            <Button type="submit" className="bg-slate-900 hover:bg-slate-800 rounded-sm" data-testid="search-btn">
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
            {(filters.trade_code || filters.state || filters.city) && (
              <Button type="button" variant="ghost" onClick={clearFilters} data-testid="clear-filters">
                Clear
              </Button>
            )}
          </form>
        </div>
      </div>

      {/* Job Listings */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <p className="text-slate-600">
            {loading ? "Loading..." : `${jobs.length} jobs found`}
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="spinner"></div>
          </div>
        ) : jobs.length === 0 ? (
          <Card className="border border-slate-200 rounded-sm">
            <CardContent className="py-12 text-center">
              <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-900 mb-2">No jobs found</h3>
              <p className="text-slate-600">Try adjusting your filters or check back later</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <Link to={`/jobs/${job.job_id}`} key={job.job_id}>
                <Card className="job-card border border-slate-200 rounded-sm" data-testid={`job-card-${job.job_id}`}>
                  <CardContent className="p-6">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-start gap-3 mb-3">
                          <div className="w-10 h-10 bg-slate-100 rounded-sm flex items-center justify-center flex-shrink-0">
                            <Briefcase className="w-5 h-5 text-slate-600" />
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold text-slate-900 hover:text-orange-500 transition-colors">
                              {job.title}
                            </h3>
                            <p className="text-sm text-slate-500">Posted by {job.contractor_name}</p>
                          </div>
                        </div>
                        
                        <p className="text-slate-600 mb-4 line-clamp-2">{job.description}</p>
                        
                        <div className="flex flex-wrap gap-2 mb-4">
                          {job.trade_codes.map((code) => (
                            <TradeBadge key={code} code={code} />
                          ))}
                        </div>
                        
                        <div className="flex flex-wrap items-center gap-4 text-sm text-slate-600">
                          <span className="flex items-center gap-1">
                            <MapPin className="w-4 h-4" />
                            {job.city}, {job.state}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {job.duration}
                          </span>
                          {job.experience_years > 0 && (
                            <span>{job.experience_years}+ years required</span>
                          )}
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <div className="price-tag mb-2">
                          ${job.pay_rate}
                          <span className="text-sm font-normal">/{job.pay_type}</span>
                        </div>
                        <Badge className="status-active text-xs">{job.status}</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
