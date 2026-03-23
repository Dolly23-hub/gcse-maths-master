import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X, BookOpen, FileText, Brain, Calculator, FlaskConical, GraduationCap, CalendarDays } from "lucide-react";

const navLinks = [
  { to: "/topics", label: "Topics", icon: BookOpen },
  { to: "/past-papers", label: "Past Papers", icon: FileText },
  { to: "/quiz", label: "Quizzes", icon: Brain },
  { to: "/formulas", label: "Formulas", icon: Calculator },
  { to: "/ai-tutor", label: "AI Tutor", icon: FlaskConical },
  { to: "/revision-planner", label: "Planner", icon: CalendarDays },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  return (
    <nav
      data-testid="main-navbar"
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b-2 border-black"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            to="/"
            data-testid="navbar-logo"
            className="flex items-center gap-2 font-heading font-bold text-xl hover:opacity-80 transition-opacity"
          >
            <div className="w-9 h-9 bg-black text-white rounded-lg flex items-center justify-center border-2 border-black shadow-hard-sm">
              <GraduationCap size={20} />
            </div>
            <span className="hidden sm:inline">GCSE Maths Master</span>
            <span className="sm:hidden">GCM</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = location.pathname.startsWith(link.to);
              const Icon = link.icon;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  data-testid={`nav-${link.label.toLowerCase().replace(/\s/g, "-")}`}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                    isActive
                      ? "bg-black text-white shadow-hard-sm"
                      : "text-neutral-600 hover:bg-neutral-100 hover:text-black"
                  }`}
                >
                  <Icon size={16} />
                  {link.label}
                </Link>
              );
            })}
          </div>

          {/* Mobile Menu Button */}
          <button
            data-testid="mobile-menu-toggle"
            className="md:hidden p-2 rounded-lg border-2 border-black hover:bg-neutral-100 transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div
          data-testid="mobile-menu"
          className="md:hidden bg-white border-b-2 border-black"
        >
          <div className="px-4 py-3 space-y-1">
            {navLinks.map((link) => {
              const isActive = location.pathname.startsWith(link.to);
              const Icon = link.icon;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  data-testid={`mobile-nav-${link.label.toLowerCase().replace(/\s/g, "-")}`}
                  onClick={() => setMobileOpen(false)}
                  className={`flex items-center gap-2 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                    isActive
                      ? "bg-black text-white"
                      : "text-neutral-600 hover:bg-neutral-100"
                  }`}
                >
                  <Icon size={18} />
                  {link.label}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}
