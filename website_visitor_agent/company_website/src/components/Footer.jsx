import { Link } from 'react-router-dom'
import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <div className="footer-brand">
            <Link to="/" className="footer-logo">
              <span className="brand-icon">O</span>
              <span className="brand-text">r-sync</span>
            </Link>
            <p className="footer-description">
              Building intelligent AI agents tailored to your specific business needs.
              From e-commerce to customer support, we create agents that work.
            </p>
          </div>

          <div className="footer-links">
            <h4>Company</h4>
            <Link to="/about">About Us</Link>
            <Link to="/services">Services</Link>
            <Link to="/agents">Our Agents</Link>
            <Link to="/contact">Contact</Link>
          </div>

          <div className="footer-links">
            <h4>Solutions</h4>
            <Link to="/agents">Custom Agents</Link>
            <Link to="/agents">Demo Agents</Link>
            <Link to="/services">Consulting</Link>
            <Link to="/services">Integration</Link>
          </div>

          <div className="footer-links">
            <h4>Connect</h4>
            <a href="mailto:orsyncagents@gmail.com">orsyncagents@gmail.com</a>
            <a href="https://www.instagram.com/orsyncagents/" target="_blank" rel="noopener noreferrer">Instagram</a>
            <a href="https://www.linkedin.com/company/orsync-agents/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            <a href="https://github.com/radiantlogicinc/fastworkflow" target="_blank" rel="noopener noreferrer">GitHub</a>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} Or-sync. All rights reserved.</p>
          <div className="footer-bottom-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
