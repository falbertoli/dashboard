<template>
  <div class="dashboard">
    <header class="hero">
      <div class="hero-content">
        <img src="@/assets/images/flight-logo.png" alt="FLIGHT Logo" class="logo" />
        <h1>FLIGHT</h1>
        <h2>Future Logistics In Green Hydrogen Technology</h2>
        <p class="tagline">Powering Tomorrow's Aviation with Green Solutions Today</p>
      </div>
    </header>

    <div class="content-grid">
      <!-- How to Use Section -->
      <section class="dashboard-section">
        <h2><i class="fas fa-book-reader"></i> How to Use This Dashboard</h2>
        <div class="step-list">
          <div class="step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>Configure Hydrogen Demand</h3>
              <p>Begin with the Hydrogen Demand calculator:</p>
              <ul class="step-details">
                <li>Set the target fleet percentage (0-100%) for hydrogen aircraft transition</li>
                <li>Select the projection year (2023-2050) for your analysis</li>
                <li>Choose which Ground Support Equipment (GSE) to convert to hydrogen</li>
                <li>Review the calculated daily hydrogen demand for both aircraft and GSE</li>
              </ul>
            </div>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>Review Sustainability Impact</h3>
              <p>Analyze environmental benefits in the Sustainability section:</p>
              <ul class="step-details">
                <li>Compare CO₂ emissions between conventional and hydrogen operations</li>
                <li>View emissions reduction metrics in metric tons</li>
                <li>Understand the environmental impact through equivalency metrics</li>
                <li>Examine detailed emissions breakdowns by source</li>
              </ul>
            </div>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>Assess Economic Feasibility</h3>
              <p>Evaluate financial implications in the Economics section:</p>
              <ul class="step-details">
                <li>Set turnaround time parameters for hydrogen aircraft</li>
                <li>Compare different improvement rate scenarios</li>
                <li>Review required tax credits and revenue impacts</li>
                <li>Analyze cumulative costs and benefits over time</li>
              </ul>
            </div>
          </div>
          <div class="step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>Plan Infrastructure</h3>
              <p>Determine storage and safety requirements:</p>
              <ul class="step-details">
                <li>Calculate required storage tank capacity</li>
                <li>Review safety buffer zones and compliance</li>
                <li>Assess potential storage locations</li>
                <li>Understand construction and insulation requirements</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Key Assumptions Section -->
      <section class="dashboard-section">
        <h2><i class="fas fa-clipboard-check"></i> Key Assumptions</h2>
        <div class="assumptions-grid">
          <div class="assumption-card">
            <i class="fas fa-plane"></i>
            <h3>Aircraft Operations</h3>
            <ul>
              <li>Based on Delta's ATL operations</li>
              <li>Focus on domestic flights</li>
              <li>Standard turnaround times</li>
            </ul>
          </div>
          <div class="assumption-card">
            <i class="fas fa-gas-pump"></i>
            <h3>Hydrogen Demand</h3>
            <ul>
              <li>LH2 as primary fuel source</li>
              <li>Includes storage losses</li>
              <li>Safety margins applied</li>
            </ul>
          </div>
          <div class="assumption-card">
            <i class="fas fa-chart-line"></i>
            <h3>Growth Projections</h3>
            <ul>
              <li>2% annual growth rate</li>
              <li>Linear adoption curve</li>
              <li>Projections until 2050</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Acronyms Section -->
      <section class="dashboard-section">
        <h2><i class="fas fa-language"></i> Common Acronyms</h2>
        <div class="acronyms-table">
          <div class="acronym-row">
            <div class="acronym">GSE</div>
            <div class="definition">Ground Support Equipment</div>
          </div>
          <div class="acronym-row">
            <div class="acronym">LH2</div>
            <div class="definition">Liquid Hydrogen</div>
          </div>
          <div class="acronym-row">
            <div class="acronym">ATL</div>
            <div class="definition">Hartsfield-Jackson Atlanta International Airport</div>
          </div>
          <div class="acronym-row">
            <div class="acronym">CO₂</div>
            <div class="definition">Carbon Dioxide</div>
          </div>
          <div class="acronym-row">
            <div class="acronym">FLIGHT</div>
            <div class="definition">Future Logistics In Green Hydrogen Technology</div>
          </div>
        </div>
      </section>

      <!-- Quick Results Section -->
      <section class="dashboard-section results-section">
        <h2><i class="fas fa-chart-pie"></i> Quick Results Overview</h2>
        <div class="results-grid">
          <router-link to="/hydrogen" class="result-card">
            <i class="fas fa-atom"></i>
            <h3>Hydrogen Demand</h3>
            <p>Calculate daily hydrogen requirements for aircraft and GSE operations.</p>
          </router-link>
          <router-link to="/sustainability" class="result-card">
            <i class="fas fa-leaf"></i>
            <h3>Emissions Impact</h3>
            <p>View potential CO₂ reductions and environmental benefits.</p>
          </router-link>
          <router-link to="/economy" class="result-card">
            <i class="fas fa-dollar-sign"></i>
            <h3>Economic Analysis</h3>
            <p>Assess financial implications and incentive requirements.</p>
          </router-link>
          <router-link to="/storage" class="result-card">
            <i class="fas fa-warehouse"></i>
            <h3>Storage Requirements</h3>
            <p>Determine infrastructure needs and safety considerations.</p>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  margin: 0 auto;
  padding-bottom: 40px;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #1a1e24 0%, #2c3e50 100%);
  padding: 60px 20px;
  text-align: center;
  margin-bottom: 40px;
  border-radius: 8px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.logo {
  max-width: 200px;
  margin-bottom: 20px;
}

.hero h1 {
  font-size: 3.5rem;
  color: #64ffda;
  margin: 0;
  font-weight: 700;
}

.hero h2 {
  font-size: 1.5rem;
  color: #fff;
  margin: 10px 0;
  font-weight: 400;
}

.tagline {
  color: #aaa;
  font-size: 1.1rem;
  margin-top: 10px;
}

/* Content Grid */
.content-grid {
  display: grid;
  gap: 30px;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Dashboard Sections */
.dashboard-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 30px;
}

.dashboard-section h2 {
  color: #64ffda;
  font-size: 1.5rem;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Steps List */
.step-list {
  display: grid;
  gap: 20px;
}

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.step:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #64ffda;
  transition: all 0.3s ease;
}

.step-number {
  background: #64ffda;
  color: #1a1e24;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-content h3 {
  color: #fff;
  margin: 0 0 10px 0;
}

.step-content p {
  color: #aaa;
  margin: 0;
}

.step-details {
  list-style-type: none;
  padding-left: 0;
  margin-top: 10px;
}

.step-details li {
  color: #aaa;
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.step-details li::before {
  content: "•";
  color: #64ffda;
  position: absolute;
  left: 0;
}

/* Assumptions Grid */
.assumptions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.assumption-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 20px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.assumption-card i {
  color: #64ffda;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.assumption-card h3 {
  color: #fff;
  margin: 0 0 15px 0;
}

.assumption-card ul {
  color: #aaa;
  padding-left: 20px;
  margin: 0;
}

.assumption-card li {
  margin-bottom: 8px;
}

/* Acronyms Table */
.acronyms-table {
  display: grid;
  gap: 10px;
}

.acronym-row {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 20px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
}

.acronym {
  color: #64ffda;
  font-weight: bold;
}

.definition {
  color: #ddd;
}

/* Results Grid */
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.result-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 25px;
  border-radius: 6px;
  text-align: center;
  transition: all 0.3s ease;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.result-card:hover {
  transform: translateY(-3px);
  background: rgba(100, 255, 218, 0.1);
  border-color: #64ffda;
}

.result-card i {
  font-size: 2rem;
  color: #64ffda;
  margin-bottom: 15px;
}

.result-card h3 {
  color: #fff;
  margin: 0 0 10px 0;
}

.result-card p {
  color: #aaa;
  margin: 0;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;
  }

  .hero h1 {
    font-size: 2.5rem;
  }

  .hero h2 {
    font-size: 1.2rem;
  }

  .dashboard-section {
    padding: 20px;
  }

  .step {
    flex-direction: column;
  }

  .assumptions-grid {
    grid-template-columns: 1fr;
  }

  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>
