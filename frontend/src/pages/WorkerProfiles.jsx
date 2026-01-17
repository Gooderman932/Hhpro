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
import { Search, MapPin, Clock, Users, DollarSign } from "lucide-react";

const AVAILABILITY_OPTIONS = {
  immediate: "Immediate",
  "1_week": "1 Week",
  "2_weeks": "2 Weeks",
  flexible: "Flexible"
};

export default function WorkerProfiles() {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    trade_code: "",
    state: "",
    city: "",
    availability: ""
  });

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.trade_code) params.append("trade_code", filters.trade_code);
      if (filters.state) params.append("state", filters.state);
      if (filters.city) params.append("city", filters.city);
      if (filters.availability) params.append("availability", filters.availability);
      
      const response = await api.get(`/profiles?${params.toString()}`);
      setProfiles(response.data);
    } catch (error) {
      console.error("Error fetching profiles:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProfiles();
  };

  const clearFilters = () => {
    setFilters({ trade_code: "", state: "", city: "", availability: "" });
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      {/* Header */}
      <div className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-bold font-['Oswald'] uppercase tracking-tight mb-2">
            Worker Profiles
          </h1>
          <p className="text-slate-400">
            Browse skilled subcontractors available for your projects
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
                  <SelectItem value="">All Trade Codes</SelectItem>
                  {Object.entries(TRADE_CODES).map(([code, name]) => (
                    <SelectItem key={code} value={code}>{code} - {name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <Input
              placeholder="State"
              className="md:w-32 rounded-sm"
              value={filters.state}
              onChange={(e) => setFilters({ ...filters, state: e.target.value })}
              data-testid="filter-state"
            />
            <Input
              placeholder="City"
              className="md:w-32 rounded-sm"
              value={filters.city}
              onChange={(e) => setFilters({ ...filters, city: e.target.value })}
              data-testid="filter-city"
            />
            <Select
              value={filters.availability}
              onValueChange={(value) => setFilters({ ...filters, availability: value })}
            >
              <SelectTrigger className="md:w-40 rounded-sm" data-testid="filter-availability">
                <SelectValue placeholder="Availability" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Any Availability</SelectItem>
                {Object.entries(AVAILABILITY_OPTIONS).map(([value, label]) => (
                  <SelectItem key={value} value={value}>{label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button type="submit" className="bg-slate-900 hover:bg-slate-800 rounded-sm" data-testid="search-btn">
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
            {(filters.trade_code || filters.state || filters.city || filters.availability) && (
              <Button type="button" variant="ghost" onClick={clearFilters} data-testid="clear-filters">
                Clear
              </Button>
            )}
          </form>
        </div>
      </div>

      {/* Profiles */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <p className="text-slate-600">
            {loading ? "Loading..." : `${profiles.length} workers found`}
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="spinner"></div>
          </div>
        ) : profiles.length === 0 ? (
          <Card className="border border-slate-200 rounded-sm">
            <CardContent className="py-12 text-center">
              <Users className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-900 mb-2">No workers found</h3>
              <p className="text-slate-600">Try adjusting your filters or check back later</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {profiles.map((profile) => (
              <Link to={`/workers/${profile.profile_id}`} key={profile.profile_id}>
                <Card className="profile-card border border-slate-200 rounded-sm h-full" data-testid={`profile-card-${profile.profile_id}`}>
                  <CardContent className="p-6">
                    <div className="flex items-start gap-4 mb-4">
                      <div className="w-14 h-14 bg-slate-200 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-slate-600">
                          {profile.name?.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-slate-900 truncate">{profile.name}</h3>
                        <p className="text-sm text-slate-600 truncate">{profile.headline}</p>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-1.5 mb-4">
                      {profile.trade_codes.slice(0, 3).map((code) => (
                        <TradeBadge key={code} code={code} showCode={false} />
                      ))}
                      {profile.trade_codes.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{profile.trade_codes.length - 3}
                        </Badge>
                      )}
                    </div>

                    <div className="space-y-2 text-sm text-slate-600">
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-slate-400" />
                        <span>{profile.city}, {profile.state}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-slate-400" />
                        <span>{profile.experience_years} years experience</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-slate-400" />
                        <span className="capitalize">{profile.availability.replace("_", " ")} availability</span>
                      </div>
                      {profile.hourly_rate_min && (
                        <div className="flex items-center gap-2">
                          <DollarSign className="w-4 h-4 text-slate-400" />
                          <span>
                            ${profile.hourly_rate_min}
                            {profile.hourly_rate_max && ` - $${profile.hourly_rate_max}`}/hr
                          </span>
                        </div>
                      )}
                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-100">
                      <Badge className={`status-${profile.status} text-xs`}>{profile.status}</Badge>
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
