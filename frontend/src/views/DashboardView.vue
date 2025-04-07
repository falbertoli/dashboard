<template>
  <div class="dashboard">
    <header class="hero">
      <div class="hero-content">
        <div class="hero-grid">
          <div class="logo-container">
            <img src="@/assets/images/flight-logo.png" alt="FLIGHT Logo" class="logo" />
          </div>
          <div class="title-container">
            <h1>FLIGHT</h1>
            <h2>Future Logistics In Green Hydrogen Technology</h2>
            <p class="tagline">Powering Tomorrow's Aviation with Green Solutions Today</p>
            <p class="description">
              Our comprehensive dashboard empowers airports and airlines to plan their transition
              to hydrogen-powered aviation. Calculate demand, assess environmental impact, analyze
              economic feasibility, and plan infrastructure requirements all in one place. Make
              data-driven decisions for a sustainable aviation future.
            </p>
          </div>
        </div>
      </div>
    </header>

    <div class="content-grid">
      <div class="tabs-container">
        <div class="tabs">
          <button v-for="tab in tabs" :key="tab.id" :class="['tab-button', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id">
            <i :class="tab.icon"></i>
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <div v-show="activeTab === 'overview'" class="tab-pane">
            <section class="dashboard-section results-section">
              <h2><i class="fas fa-chart-pie"></i> Quick Results Overview</h2>
              <div class="results-grid">
                <router-link to="/hydrogen" class="result-card">
                  <div class="card-icon-container">
                    <i class="fas fa-atom"></i>
                  </div>
                  <div class="card-content">
                    <h3>Hydrogen Demand</h3>
                    <p>Calculate daily hydrogen requirements for aircraft and GSE operations.</p>
                  </div>
                </router-link>
                <router-link to="/sustainability" class="result-card">
                  <div class="card-icon-container">
                    <i class="fas fa-leaf"></i>
                  </div>
                  <div class="card-content">
                    <h3>Emissions Impact</h3>
                    <p>View potential CO₂ reductions and environmental benefits.</p>
                  </div>
                </router-link>
                <router-link to="/economy" class="result-card">
                  <div class="card-icon-container">
                    <i class="fas fa-dollar-sign"></i>
                  </div>
                  <div class="card-content">
                    <h3>Economic Analysis</h3>
                    <p>Assess financial implications and incentive requirements.</p>
                  </div>
                </router-link>
                <router-link to="/storage" class="result-card">
                  <div class="card-icon-container">
                    <i class="fas fa-warehouse"></i>
                  </div>
                  <div class="card-content">
                    <h3>Storage Requirements</h3>
                    <p>Determine infrastructure needs and safety considerations.</p>
                  </div>
                </router-link>
              </div>
            </section>
          </div>

          <div v-show="activeTab === 'guide'" class="tab-pane">
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
          </div>

          <div v-show="activeTab === 'info'" class="tab-pane">
            <div class="two-column-grid">
              <section class="dashboard-section">
                <h2><i class="fas fa-clipboard-check"></i> Key Assumptions</h2>
                <div class="assumptions-grid">
                  <div class="assumption-card">
                    <div class="card-header">
                      <i class="fas fa-plane"></i>
                      <h3>Aircraft Operations</h3>
                    </div>
                    <ul>
                      <li>Based on Delta's ATL operations</li>
                      <li>Focus on domestic flights</li>
                      <li>Standard turnaround times</li>
                    </ul>
                  </div>
                  <div class="assumption-card">
                    <div class="card-header">
                      <i class="fas fa-gas-pump"></i>
                      <h3>Hydrogen Demand</h3>
                    </div>
                    <ul>
                      <li>LH2 as primary fuel source</li>
                      <li>Includes storage losses</li>
                      <li>Safety margins applied</li>
                    </ul>
                  </div>
                  <div class="assumption-card">
                    <div class="card-header">
                      <i class="fas fa-chart-line"></i>
                      <h3>Growth Projections</h3>
                    </div>
                    <ul>
                      <li>2% annual growth rate</li>
                      <li>Linear adoption curve</li>
                      <li>Projections until 2050</li>
                    </ul>
                  </div>
                </div>
              </section>

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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'overview',
      tabs: [
        { id: 'overview', name: 'Overview', icon: 'fas fa-chart-pie' },
        { id: 'guide', name: 'User Guide', icon: 'fas fa-book-reader' },
        { id: 'info', name: 'Information', icon: 'fas fa-info-circle' }
      ]
    }
  }
}
</script>

<style scoped>
.dashboard {
  margin: 0 auto;
  padding-bottom: 60px;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 0;
  }
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #0e141b 0%, #1c2c3a 50%, #2c3e50 100%);
  padding: 60px 20px;
  text-align: center;
  margin-bottom: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
}

/* Hero pattern using CSS instead of external SVG */
.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
  opacity: 0.3;
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.hero-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 40px;
  align-items: center;
  text-align: left;
}

.logo-container {
  padding-right: 40px;
  border-right: 1px solid rgba(100, 255, 218, 0.2);
}

.title-container {
  text-align: left;
}

.logo {
  max-width: 120px;
  filter: drop-shadow(0 0 10px rgba(100, 255, 218, 0.5));
}

.hero h1 {
  font-size: 3.5rem;
  color: #64ffda;
  margin: -5px 0 0 0;
  font-weight: 800;
  letter-spacing: -1px;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
}

.hero h2 {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 5px 0;
  font-weight: 400;
}

.tagline {
  color: rgba(255, 255, 255, 0.65);
  font-size: 1.2rem;
  margin-top: 20px;
  font-style: italic;
  max-width: 80%;
  margin-left: auto;
  margin-right: auto;
}

.description {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  line-height: 1.6;
  margin-top: 20px;
  max-width: 800px;
}

/* Content Grid */
.content-grid {
  display: grid;
  gap: 40px;
  padding: 0 20px;
  max-width: 1300px;
  margin: 0 auto;
}

.two-column-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

/* Dashboard Sections */
.dashboard-section {
  background: rgba(22, 28, 36, 0.7);
  border-radius: 12px;
  padding: 35px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(100, 255, 218, 0.1);
  transition: all 0.3s ease;
}

.dashboard-section:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
  border-color: rgba(100, 255, 218, 0.25);
}

.dashboard-section h2 {
  color: #64ffda;
  font-size: 1.6rem;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(100, 255, 218, 0.2);
}

.dashboard-section h2 i {
  font-size: 1.4rem;
}

/* Steps List */
.step-list {
  display: grid;
  gap: 25px;
}

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  padding: 22px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.3s ease;
}

.step:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(100, 255, 218, 0.4);
  transform: translateY(-2px);
}

.step-number {
  background: linear-gradient(135deg, #64ffda 0%, #38b2ac 100%);
  color: #0e1621;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.3rem;
  flex-shrink: 0;
  box-shadow: 0 2px 10px rgba(100, 255, 218, 0.5);
}

.step-content {
  flex: 1;
}

.step-content h3 {
  color: #fff;
  margin: 0 0 12px 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.step-content p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 1.05rem;
}

.step-details {
  list-style-type: none;
  padding-left: 0;
  margin-top: 12px;
}

.step-details li {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 10px;
  padding-left: 22px;
  position: relative;
  line-height: 1.5;
}

.step-details li::before {
  content: "•";
  color: #64ffda;
  position: absolute;
  left: 0;
  font-size: 1.2rem;
}

/* Assumptions Grid */
.assumptions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.assumption-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 22px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.25s ease;
}

.assumption-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
  border-color: rgba(100, 255, 218, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.card-header i {
  color: #64ffda;
  font-size: 1.5rem;
  background: rgba(100, 255, 218, 0.1);
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.assumption-card h3 {
  color: #fff;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 500;
}

.assumption-card ul {
  color: rgba(255, 255, 255, 0.65);
  padding-left: 20px;
  margin: 0;
  line-height: 1.6;
}

.assumption-card li {
  margin-bottom: 8px;
}

/* Acronyms Table */
.acronyms-table {
  display: grid;
  gap: 12px;
}

.acronym-row {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 20px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  transition: all 0.2s ease;
  align-items: center;
}

.acronym-row:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(3px);
}

.acronym {
  color: #64ffda;
  font-weight: 600;
  font-size: 1.1rem;
}

.definition {
  color: rgba(255, 255, 255, 0.8);
}

/* Results Grid */
.results-section {
  background: linear-gradient(to bottom, rgba(20, 30, 48, 0.8), rgba(22, 28, 36, 0.7));
  border-width: 1px;
  border-style: solid;
  border-color: rgba(100, 255, 218, 0.2);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.result-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 25px;
  border-radius: 12px;
  transition: all 0.3s ease;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-card:hover {
  transform: translateY(-5px);
  background: rgba(100, 255, 218, 0.08);
  border-color: #64ffda;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.card-icon-container {
  background: rgba(100, 255, 218, 0.1);
  border-radius: 12px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.result-card:hover .card-icon-container {
  background: rgba(100, 255, 218, 0.2);
  transform: scale(1.1);
}

.card-icon-container i {
  font-size: 1.8rem;
  color: #64ffda;
}

.card-content {
  text-align: left;
}

.result-card h3 {
  color: #fff;
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.result-card p {
  color: rgba(255, 255, 255, 0.65);
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Tabs Container */
.tabs-container {
  background: rgba(22, 28, 36, 0.7);
  border-radius: 12px;
  border: 1px solid rgba(100, 255, 218, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  background: rgba(14, 20, 27, 0.5);
  padding: 15px 15px 0;
  gap: 5px;
  border-bottom: 1px solid rgba(100, 255, 218, 0.1);
}

.tab-button {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  padding: 12px 24px;
  font-size: 1.1rem;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-button i {
  font-size: 1rem;
}

.tab-button:hover {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(100, 255, 218, 0.1);
}

.tab-button.active {
  color: #64ffda;
  background: rgba(22, 28, 36, 0.95);
  border: 1px solid rgba(100, 255, 218, 0.2);
  border-bottom-color: transparent;
  transform: translateY(1px);
}

.tab-content {
  padding: 30px;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Design */
@media (max-width: 1100px) {
  .two-column-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .hero {
    padding: 40px 20px;
  }

  .hero-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    text-align: center;
  }

  .logo-container {
    padding-right: 0;
    border-right: none;
    border-bottom: 1px solid rgba(100, 255, 218, 0.2);
    padding-bottom: 20px;
  }

  .title-container {
    text-align: center;
  }

  .description {
    margin-left: auto;
    margin-right: auto;
  }

  .logo-container {
    flex-direction: column;
    text-align: center;
  }

  .title-container {
    text-align: center;
  }

  .hero h1 {
    font-size: 2.8rem;
  }

  .hero h2 {
    font-size: 1.2rem;
  }

  .dashboard-section {
    padding: 25px;
  }

  .results-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .hero h1 {
    font-size: 2.2rem;
  }

  .step {
    flex-direction: column;
  }

  .step-number {
    margin-bottom: 10px;
  }

  .dashboard-section {
    padding: 20px;
  }

  .result-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }

  .card-content {
    text-align: center;
  }

  .tabs {
    flex-direction: column;
    padding: 10px;
    gap: 8px;
  }

  .tab-button {
    width: 100%;
    border-radius: 6px;
    justify-content: center;
  }

  .tab-button.active {
    transform: none;
    border-bottom-color: rgba(100, 255, 218, 0.2);
  }

  .tab-content {
    padding: 20px;
  }
}
</style>