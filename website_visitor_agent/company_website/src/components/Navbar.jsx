import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/about', label: 'About' },
    { path: '/services', label: 'Services' },
    { path: '/agents', label: 'Agents' },
    { path: '/contact', label: 'Contact' },
  ]

  return (
    <nav className="navbar">
      <div className="container navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">O</span>
          <span className="brand-text">r-sync</span>
        </Link>

        <button
          className={`hamburger ${isOpen ? 'active' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div className={`nav-menu ${isOpen ? 'open' : ''}`}>
          {navLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              end={link.path === '/'}
              className={({ isActive }) =>
                `nav-link ${isActive ? 'active' : ''}`
              }
              onClick={() => setIsOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
          <Link to="/contact" className="btn btn-primary nav-cta" onClick={() => setIsOpen(false)}>
            Get Started
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
