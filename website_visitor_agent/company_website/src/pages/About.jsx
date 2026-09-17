import { Link } from 'react-router-dom'
import './About.css'

function About() {
  const values = [
    {
      title: 'Purpose-Built',
      description: 'Every agent we create is designed for a specific use case — no generic solutions, no one-size-fits-all.',
    },
    {
      title: 'Transparent',
      description: 'We believe in clear communication about what AI can and cannot do. No hype, just results.',
    },
    {
      title: 'Affordable by Design',
      description: 'State-of-the-art agent technology at the lowest possible cost — small models that perform like frontier ones.',
    },
    {
      title: 'User-First',
      description: 'We design agents that feel natural to interact with, prioritizing the end-user experience above all.',
    },
  ]

  return (
    <div className="about">
      <section className="about-hero">
        <div className="container">
          <h1 className="about-title">
            We Build Agents That <span className="gradient-text">Actually Work</span>
          </h1>
          <p className="about-subtitle">
            Or-sync was founded in 2026 on a simple belief: every business deserves
            production-grade AI agents — state-of-the-art technology at the most
            affordable price.
          </p>
        </div>
      </section>

      <section className="section story-section">
        <div className="container">
          <div className="story-grid">
            <div className="story-content">
              <h2>Our Story</h2>
              <p>
                Or-sync was founded in 2026 by engineers who were part of the core team
                that developed{' '}
                <a
                  href="https://github.com/radiantlogicinc/fastworkflow"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  fastWorkflow
                </a>
                , an open-source framework for building large-scale, deterministic,
                interactive agent workflows. On industry-standard Tau Bench benchmarks,
                fastWorkflow enables small models to match frontier model performance
                on structured agentic tasks.
              </p>
              <p>
                We're a young company with a handful of early clients, but our team
                brings deep experience in building agents that are reliable in production —
                not just impressive in demos. We know what breaks when real users show up,
                and we built our stack to handle it.
              </p>
            </div>
            <div className="story-visual">
              <div className="story-card">
                <div className="story-stat">2026</div>
                <p>Founded with a mission to deliver SOTA agent technology at the lowest cost</p>
              </div>
              <div className="story-card">
                <div className="story-stat">fastWorkflow</div>
                <p>Our core team helped build the open-source agent framework</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section values-section">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Mission & Vision</h2>
            <p className="section-subtitle">
              State-of-the-art agent technology at the lowest possible cost.
              We make production-grade AI accessible to businesses of every size.
            </p>
          </div>
        </div>
      </section>

      <section className="section values-section">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Our Values</h2>
            <p className="section-subtitle">
              The principles that guide everything we build.
            </p>
          </div>
          <div className="values-grid">
            {values.map((value, index) => (
              <div key={index} className="card value-card">
                <span className="value-number">0{index + 1}</span>
                <h3>{value.title}</h3>
                <p>{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section team-section">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Our Team</h2>
            <p className="section-subtitle">
              Or-sync is led by directors and engineers from the core team that developed
              fastWorkflow. With deep experience in agent architecture, intent detection,
              and production deployment, we build SOTA agents without the enterprise overhead —
              and without putting names or faces on a website. Our work speaks for itself.
            </p>
          </div>
        </div>
      </section>

      <section className="section cta-section">
        <div className="container text-center">
          <h2 className="section-title">Want to Work With Us?</h2>
          <p className="section-subtitle">
            Whether you need an agent or want to join the team, we'd love to hear from you.
          </p>
          <Link to="/contact" className="btn btn-primary">
            Get in Touch
          </Link>
        </div>
      </section>
    </div>
  )
}

export default About
