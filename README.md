# Quick Start

## Prerequisites

- Python & pip
- Node.js & npm
- Git

## Running the Project

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/falbertoli/dashboard.git
    cd hydrogen
    ```

2.  **Run Backend (Flask):**

    - Open a terminal.
    - Navigate to backend:
      ```bash
      cd backend
      ```
    - (First time) Install dependencies:
      ```bash
      # Optional: Create/activate virtual environment first
      # python -m venv venv
      # source venv/bin/activate  (or .\venv\Scripts\activate on Windows)
      pip install -r requirements.txt
      ```
    - Run the server:
      ```bash
      python run.py
      ```

3.  **Run Frontend (Vue + Vite):**

    - Open a **new** terminal.
    - Navigate to frontend:
      ```bash
      cd frontend
      ```
    - (First time) Install dependencies:
      ```bash
      npm install
      ```
    - Run the development server:
      ```bash
      npm run dev
      ```

    (npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome --save)
    (npm install @fortawesome/fontawesome-free --save)

4.  **Access:**
    - Open your browser to the frontend URL provided in the terminal.

# FLIGHT Dashboard: Hydrogen Infrastructure Analysis Tool

_Future Logistics in Green Hydrogen Transport_

## 1. Dashboard Overview

_Interactive analysis tool for hydrogen infrastructure planning_

### Home Screen

- **Welcome & Purpose**

  - Hydrogen transition planning for airports
  - Infrastructure requirement analysis
  - Economic impact assessment
  - Regulatory compliance verification

- **Key Benefits**
  - Data-driven decision making
  - Comprehensive scenario analysis
  - Real-time calculations
  - Risk mitigation support

## 2. Input Configuration Screen

_Where planning begins_

### User Inputs

- **Fleet Transition Parameters**

  - Fleet transition percentage (configurable):

    - Impact on total flights: Based on ATL departure data
    - Current baseline: 531,558 annual Delta departures
    - Example: 20% transition = ~106,311 H2 flights

  - Timeline configuration:
    - Start year (2024-2030)
    - End year (up to 2050)
    - Transition milestones
  - Growth rate modeling:
    - Historical growth patterns from ac_data.csv
    - User-adjustable (1-5% annual)
    - Impact on infrastructure sizing

- **Operational Parameters**

  - Extra turnaround time:

    - Current data shows 10-30 minutes additional
    - Impact on daily operations
    - Revenue hour calculations

  - Route prioritization:
    - Based on actual flight distances from ac_data.csv
    - Focus on routes < 1,000 miles initially
    - Gradual expansion to longer routes

### What This Answers

- **"How do we start the transition?"**

  - Strategic Insights from Data:
    - Most viable routes for initial transition (based on flight data showing 67-406 mile routes from ATL)
    - Optimal fleet segment to convert (based on aircraft utilization patterns)
    - Infrastructure capacity needed (derived from actual fuel consumption data)
    - Revenue impact estimates (calculated from real operational data)

- **"What parameters matter most?"**
  Delta Airlines Decision Support:

  - Revenue Impact Analysis:

    - Actual flight schedule disruption costs
    - Real utilization changes from extended turnaround
    - Route-specific profitability impacts

  - Fleet Planning Insights:
    - High-frequency routes suitable for H2
    - Aircraft type transition priorities
    - Maintenance schedule implications

  Airport Authority Decision Support:

  - Infrastructure Planning:
    - Land use optimization (based on current facility data)
    - Storage capacity requirements (from actual fuel demand)
    - Safety compliance requirements
    - Phasing approach based on airline needs

- **"How can we phase the implementation?"**
  Data-Driven Implementation Strategy:

  - Initial Phase Focus:

    - Routes showing highest H2 conversion viability
    - Minimal infrastructure impact
    - Manageable revenue effects

  - Scaling Triggers:

    - Infrastructure utilization thresholds
    - Revenue impact tolerance levels
    - Operational efficiency metrics

  - Risk Management:
    - Early warning indicators from operational data
    - Adjustment points based on performance metrics
    - Compliance milestone tracking

### Impact Analysis

Each parameter is linked to specific stakeholder decisions:

- Airlines:
  - Route network optimization
  - Fleet modernization timing
  - Revenue protection strategies
- Airport:
  - Infrastructure investment timing
  - Land use planning
  - Safety compliance roadmap

## 3. Demand Analysis Screen

_Understanding hydrogen requirements_

### Calculations Performed

- Aircraft H2 demand based on:
  - Flight volumes
  - Aircraft types
  - Route patterns
- GSE H2 requirements
- Total demand forecasting

### What This Answers

For Airlines:

- Fuel logistics planning based on actual flight schedules
- Peak demand periods from historical patterns
- Route-specific hydrogen requirements
- Fleet transition impact on fuel needs

For Airport:

- Total hydrogen storage requirements
- Daily/monthly throughput planning
- Infrastructure sizing requirements
- Supply chain planning needs

### Key Outputs

- Monthly demand forecasts
- Peak usage patterns
- Growth trajectories

## 4. Infrastructure Requirements Screen

_Planning storage and facilities_

### Analysis Provided

- Storage tank requirements
- Land area needs
- Safety buffer calculations
- Facility layout recommendations

### What This Answers

For Airport Planning:

- Land use optimization strategies
- Storage facility placement options
- Future expansion planning
- Safety compliance requirements

For Airlines:

- Aircraft parking and fueling logistics
- Ground operations adaptation needs
- Maintenance facility requirements
- Operational constraint identification

## 5. Economic Impact Screen

_Financial analysis and optimization_

### What This Answers

For Financial Planning:

- Capital investment requirements
- Operating cost changes
- Revenue impact mitigation
- Tax incentive opportunities

For Operations:

- Resource allocation efficiency
- Cost optimization opportunities
- Performance metrics impacts
- ROI optimization strategies

### Key Metrics Shown

- Revenue projections
- Infrastructure costs
- Tax credit requirements
- Payback periods

## 6. Regulatory Compliance Screen

_Safety and standards verification_

### Features

- Automated compliance checking
- Safety distance validation
- Regulatory requirement tracking
- Risk assessment display

### What This Answers

For Safety/Compliance Teams:

- Specific regulation adherence status
- Required safety measure implementations
- Permit application requirements
- Risk mitigation strategies

For Management:

- Compliance timeline planning
- Resource allocation needs
- Risk assessment insights
- Implementation priorities

## 7. Sustainability Impact Screen

_Environmental benefit tracking_

### Metrics Displayed

- CO2 emissions reduction
- Environmental benefits
- Progress towards goals
- Impact visualization

### What This Answers

For Environmental Teams:

- Carbon reduction quantification
- Environmental compliance tracking
- Green initiative progress
- Sustainability goal achievements

For Stakeholder Relations:

- Environmental impact reporting
- Public relations metrics
- Sustainability milestone tracking
- Green funding qualification data

## 8. Results & Recommendations

_Final analysis and next steps_

### Output Summary

- Comprehensive analysis results
- Implementation recommendations
- Risk mitigation strategies
- Timeline proposals

### Output Value

For Executive Decision Making:

- Strategic implementation roadmap
- Resource allocation guidance
- Risk mitigation priorities
- Performance optimization paths

For Project Teams:

- Detailed action items
- Timeline synchronization
- Resource coordination needs
- Success metrics definition

### Action Items

- Key decisions needed
- Implementation phases
- Resource requirements
- Timeline milestones

## Contact Information

For detailed demonstrations and analysis:

- Email: [contact@flightdashboard.com]
- Phone: [555-0123]
