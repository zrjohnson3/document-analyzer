import { Link } from "react-router-dom";
import "./Navigation.css";

/**
 * Navigation Component
 *
 * Main application header/navigation bar with:
 * - Brand logo and title
 * - Navigation links
 *
 * Provides consistent app navigation and branding across all pages.
 * Uses React Router for client-side navigation.
 */
export const Navigation = () => {
  return (
    <nav className="navigation">
      {/* Brand section with logo and app title */}
      <div className="nav-brand">
        <Link to="/">
          <svg
            className="brand-logo"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="#4f46e5"
          >
            <path d="M7 3C4.79086 3 3 4.79086 3 7V17C3 19.2091 4.79086 21 7 21H17C19.2091 21 21 19.2091 21 17V7C21 4.79086 19.2091 3 17 3H7ZM6 8C6 7.44772 6.44772 7 7 7H17C17.5523 7 18 7.44772 18 8C18 8.55228 17.5523 9 17 9H7C6.44772 9 6 8.55228 6 8ZM6 12C6 11.4477 6.44772 11 7 11H11C11.5523 11 12 11.4477 12 12C12 12.5523 11.5523 13 11 13H7C6.44772 13 6 12.5523 6 12ZM6 16C6 15.4477 6.44772 15 7 15H17C17.5523 15 18 15.4477 18 16C18 16.5523 17.5523 17 17 17H7C6.44772 17 6 16.5523 6 16Z" />
          </svg>
          Document Analyzer
        </Link>
      </div>

      {/* Main navigation links */}
      <ul className="nav-links">
        <li>
          <Link to="/">Upload Documents</Link>
        </li>
        {/* Additional navigation links can be added here */}
      </ul>
    </nav>
  );
};
