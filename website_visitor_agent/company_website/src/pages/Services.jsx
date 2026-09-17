import { Link } from 'react-router-dom'
import './Services.css'

function Services() {
  const services = [
    {
      icon: '🎯',
      title: 'Custom Agent Development',
      description: 'We design and build AI agents from scratch based on your specific business requirements. From e-commerce to internal ops, we craft agents that understand your domain.',
      features: ['Domain-specific training', 'Multi-step workflow handling', 'Natural language understanding', 'Custom personality & tone'],
    },
    {
      icon: '🔌',
      title: 'Platform Integration',
      description: 'Connect your AI agent seamlessly to the tools and platforms you already use. We handle the technical integration so your agent works within your existing ecosystem.',
      features: ['Shopify & e-commerce platforms', 'CRM systems (Salesforce, HubSpot)', 'Communication tools (Slack, Teams)', 'Custom API integrations'],
    },
    {
      icon: '🧠',
      title: 'Agent Strategy & Consulting',
      description: 'Not sure where to start? We help you identify the highest-impact areas for AI agent deployment and design a roadmap for implementation.',
      features: ['Use case identification', 'ROI analysis', 'Architecture planning', 'Implementation roadmap'],
    },
    {
      icon: '📈',
      title: 'Optimization & Scaling',
      description: 'Already have agents in production? We help optimize their performance, improve accuracy, and scale to handle growing demand.',
      features: ['Performance analytics', 'Response quality tuning', 'Load scaling', 'A/B testing frameworks'],
    },
    {
      icon: '🛡️',
      title: 'Maintenance & Support',
      description: 'Keep your agents running smoothly with our ongoing maintenance packages. We monitor, update, and improve your agents continuously.',
      features: ['24/7 monitoring', 'Regular model updates', 'Bug fixes & patches', 'Monthly performance reports'],
    },
    {
      icon: '🎓',
      title: 'Training & Workshops',
      description: 'Empower your team with hands-on training on AI agent best practices, prompt engineering, and managing deployed agents.',
      features: ['Team workshops', 'Prompt engineering training', 'Agent management guides', 'Best practices documentation'],
    },
  ]

  const process = [
    {
      step: '01',
      title: 'Discovery',
      description: 'We learn about your business, workflows, and goals to identify the perfect use case for an AI agent.',
    },
    {
      step: '02',
      title: 'Design',
      description: 'We architect the agent\'s capabilities, integrations, and conversation flows tailored to your needs.',
    },
    {
      step: '03',
      title: 'Build',
      description: 'Our engineering team develops your agent with rigorous testing at every stage.',
    },
    {
      step: '04',
      title: 'Deploy & Iterate',
      description: 'We launch your agent and continuously improve it based on real-world performance data.',
    },
  ]

  return (
    <div className="services">
      <section className="services-hero">
        <div className="container">
          <h1 className="services-title">
            Our <span className="gradient-text">Services</span>
          </h1>
          <p className="services-subtitle">
            End-to-end AI agent solutions — from strategy and design
            through development, deployment, and ongoing optimization.
            Powered by fastWorkflow for production-grade reliability at a fraction of the cost.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="services-grid">
            {services.map((service, index) => (
              <div key={index} className="card service-card">
                <span className="service-icon">{service.icon}</span>
                <h3>{service.title}</h3>
                <p className="service-description">{service.description}</p>
                <ul className="service-features">
                  {service.features.map((feature, i) => (
                    <li key={i}>
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M3 7L6 10L11 4" stroke="var(--accent-blue)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section process-section">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">How We Work</h2>
            <p className="section-subtitle">
              A proven process that turns your idea into a production-ready agent.
            </p>
          </div>
          <div className="process-grid">
            {process.map((item, index) => (
              <div key={index} className="process-card">
                <span className="process-step">{item.step}</span>
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section cta-section">
        <div className="container text-center">
          <h2 className="section-title">Let's Build Something Together</h2>
          <p className="section-subtitle">
            Tell us about your project and we'll show you what's possible.
          </p>
          <div className="cta-actions">
            <Link to="/contact" className="btn btn-primary">Start a Project</Link>
            <Link to="/contact" className="btn btn-secondary">Request a Demo</Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Services
