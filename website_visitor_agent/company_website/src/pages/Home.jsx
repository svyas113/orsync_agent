import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  const features = [
    {
      icon: '🤖',
      title: 'Production-Grade Agents',
      description: 'Built on fastWorkflow — validated parameters, structured tool execution, and clarification instead of silent wrong actions.',
    },
    {
      icon: '⚡',
      title: 'SOTA at Lower Cost',
      description: 'Small models that match frontier performance on agentic benchmarks — state-of-the-art technology without frontier-model pricing.',
    },
    {
      icon: '🔗',
      title: 'Seamless Integration',
      description: 'Our agents plug into your existing tools — CRMs, communication platforms, and custom APIs — without restructuring your app.',
    },
    {
      icon: '📊',
      title: 'Reliable by Design',
      description: 'Intent detection, parameter validation, and context hierarchies keep agents accurate on real, messy user input.',
    },
  ]

  const stats = [
    { value: '2026', label: 'Founded' },
    { value: 'Open Source', label: 'fastWorkflow Core' },
    { value: '24/7', label: 'Agent Availability' },
    { value: 'Tau Bench', label: 'Benchmark-Backed Tech' },
  ]

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-bg">
          <div className="hero-glow hero-glow-1"></div>
          <div className="hero-glow hero-glow-2"></div>
        </div>
        <div className="container hero-content">
          <div className="hero-badge">AI-Powered Automation</div>
          <h1 className="hero-title">
            Intelligent Agents Built<br />
            <span className="gradient-text">For Your Business</span>
          </h1>
          <p className="hero-subtitle">
            Or-sync delivers state-of-the-art AI agents at the most affordable price.
            Built on proven open-source technology by engineers who helped create
            fastWorkflow — production-ready agents without the enterprise price tag.
          </p>
          <div className="hero-actions">
            <Link to="/contact" className="btn btn-primary">
              Get in Touch
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M6 12L10 8L6 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
            <Link to="/services" className="btn btn-secondary">
              Explore Services
            </Link>
          </div>
        </div>
      </section>

      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            {stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <span className="stat-value">{stat.value}</span>
                <span className="stat-label">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section features-section">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Why Choose Or-sync?</h2>
            <p className="section-subtitle">
              We don't just build chatbots — we create reliable, production-grade agents
              powered by the same framework benchmarked against frontier models.
            </p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="card feature-card">
                <span className="feature-icon">{feature.icon}</span>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section demo-banner">
        <div className="container">
          <div className="banner-card">
            <div className="banner-content">
              <h2>Try Our Demo Agents</h2>
              <p>
                Explore public retail demos like Spyran, Zebrata, and RVD Jewels — or request
                a private walkthrough tailored to your business. Chat with our site assistant
                anytime to get started.
              </p>
              <Link to="/contact" className="btn btn-primary">
                Request a Demo
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M6 12L10 8L6 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </Link>
            </div>
            <div className="banner-visual">
              <div className="mock-chat">
                <div className="mock-message bot">Hi! I'm the Or-sync assistant. Want to try a demo agent or request a private demo?</div>
                <div className="mock-message user">Show me a random demo agent</div>
                <div className="mock-message bot">Here's Zebrata — jewellery browse, cart, and virtual try-on. Open it anytime from chat.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section cta-section">
        <div className="container text-center">
          <h2 className="section-title">Ready to Build Your Agent?</h2>
          <p className="section-subtitle">
            Tell us about your use case and we'll design an agent that fits perfectly.
          </p>
          <Link to="/contact" className="btn btn-primary">
            Get in Touch
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
