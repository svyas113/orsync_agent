import { Link } from 'react-router-dom'
import './Agents.css'

function Agents() {
  const agents = [
    {
      name: 'Spyran — Retail Support Agent',
      category: 'Retail',
      status: 'Demo',
      description:
        'A retail support demo that searches products, browses categories, shows product details, and manages a cart. Great for seeing structured agent workflows in action.',
      capabilities: [
        'Product search & browse',
        'Product details',
        'Cart management',
        'Natural-language shopping help',
      ],
    },
    {
      name: 'Zebrata — Jewellery Try-On Agent',
      category: 'Jewellery',
      status: 'Demo',
      description:
        'A jewellery and home décor demo with catalog and cart flows, plus virtual try-on from a customer selfie.',
      capabilities: [
        'Catalogue & cart',
        'Virtual try-on',
        'Jewellery discovery',
        'Natural-language assistance',
      ],
    },
    {
      name: 'RVD Jewels — Jewellery Agent',
      category: 'Jewellery',
      status: 'Demo',
      description:
        'A jewellery retail demo with catalog/cart flows and virtual try-on, using an RVD Jewels–style catalog.',
      capabilities: [
        'Catalogue & cart',
        'Virtual try-on',
        'Product discovery',
        'Natural-language assistance',
      ],
    },
  ]

  return (
    <div className="agents">
      <section className="agents-hero">
        <div className="container">
          <h1 className="agents-title">
            Our <span className="gradient-text">AI Agents</span>
          </h1>
          <p className="agents-subtitle">
            Specialized AI agents designed for specific domains and customized to your needs.
            Contact us to see our agents in action.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="agents-grid">
            {agents.map((agent, index) => (
              <div key={index} className="card agent-card">
                <div className="agent-header">
                  <span className="agent-category">{agent.category}</span>
                  <span className={`agent-status ${agent.status === 'Live' ? 'live' : 'soon'}`}>
                    {agent.status}
                  </span>
                </div>
                <h3>{agent.name}</h3>
                <p className="agent-description">{agent.description}</p>
                <ul className="agent-capabilities">
                  {agent.capabilities.map((cap, i) => (
                    <li key={i}>
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M3 7L6 10L11 4" stroke="var(--accent-blue)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      {cap}
                    </li>
                  ))}
                </ul>
                <Link to="/contact" className="btn btn-primary agent-btn">
                  Request a Demo
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M5 10L9 7L5 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section custom-section">
        <div className="container">
          <div className="custom-banner">
            <h2>Need a Custom Agent?</h2>
            <p>
              Don't see what you need? We build custom agents tailored to your exact
              business requirements. Tell us your use case and we'll make it happen.
            </p>
            <Link to="/contact" className="btn btn-primary">
              Describe Your Use Case
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Agents
