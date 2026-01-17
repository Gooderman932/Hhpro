import { Link } from "react-router-dom";
import { Mail, Phone, MapPin } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-white rounded-sm flex items-center justify-center">
                <span className="text-orange-500 font-bold text-xl font-['Oswald']">H</span>
              </div>
              <span className="text-lg font-bold font-['Oswald'] tracking-wide">HDRYWALL</span>
            </div>
            <p className="text-slate-400 text-sm">
              Connecting contractors with skilled tradespeople since 2024. Pride. Professionalism. Quality.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-4">
              For Contractors
            </h4>
            <ul className="space-y-2">
              <li>
                <Link to="/jobs" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Browse Jobs
                </Link>
              </li>
              <li>
                <Link to="/post-job" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Post a Job
                </Link>
              </li>
              <li>
                <Link to="/workers" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Find Workers
                </Link>
              </li>
            </ul>
          </div>

          {/* For Workers */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-4">
              For Workers
            </h4>
            <ul className="space-y-2">
              <li>
                <Link to="/jobs" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Find Work
                </Link>
              </li>
              <li>
                <Link to="/create-profile" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Create Profile
                </Link>
              </li>
              <li>
                <Link to="/shop" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Shop Tools
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-4">
              Contact Us
            </h4>
            <ul className="space-y-3">
              <li className="flex items-center gap-2 text-slate-400 text-sm">
                <Mail className="w-4 h-4" />
                info@hdrywallrepair.com
              </li>
              <li className="flex items-center gap-2 text-slate-400 text-sm">
                <Phone className="w-4 h-4" />
                (555) 123-4567
              </li>
              <li className="flex items-start gap-2 text-slate-400 text-sm">
                <MapPin className="w-4 h-4 mt-0.5" />
                <span>Serving contractors nationwide</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-slate-500 text-sm">
            © {new Date().getFullYear()} HDrywall Repair. All rights reserved.
          </p>
          <div className="flex gap-6">
            <Link to="/market-data" className="text-slate-500 hover:text-white text-sm transition-colors">
              Market Data
            </Link>
            <a href="#" className="text-slate-500 hover:text-white text-sm transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-slate-500 hover:text-white text-sm transition-colors">
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
