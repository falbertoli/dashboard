FLIGHT Future Logistics in Green Hydrogen Transport
• Comprehensive Hydrogen Storage Analysis Use Case
• Demand, Storage, Regulatory Compliance, Sustainability, and Economic Impact
Introduction
• Presentation Topic: Integrated H2 Infrastructure Analysis for the Atlanta Airport
• H2 airport adoption Problem statement:
• Uncertain H2 demand (flights/GSE ops)
• Storage constraints (land, safety distances).
• Regulatory maze (OSHA, DOT, NFPA, SAE).
• Economic viability (costs, incentives, Return On Investment).
• Purpose:
• Enable stakeholders to analyze hydrogen storage requirements comprehensively.
• Evaluate demand, storage needs, regulatory compliance, sustainability impacts, and economic feasibility of hydrogen infrastructure.
• Stakeholders:
• Airport developers
• Airline stakeholders
Comprehensive Use Case Overview
• Goal of Analysis:
• Accurately estimate hydrogen demand for aircraft and ground support equipment (GSE).
• Evaluate hydrogen storage infrastructure requirements.
• Ensure regulatory compliance with safety standards.
• Analyze sustainability impacts.
• Provide detailed economic feasibility assessments.
Key Steps
Scenario & Fleet Selection
Hydrogen Consumption Data Input
Hydrogen Demand and Storage Calculation
Infrastructure Requirements & Land Area
Regulatory Compliance Evaluation
Sustainability Assessment
Economic Impact Analysis
Step 1 – Scenario and Fleet Selection
• Scenarios Considered:
• Aircraft only
• Ground Support Equipment (GSE) only
• Combined Scenario (Aircraft + GSE)
• Inputs:
• Aircraft transition percentage: Proportion of aircraft adopting hydrogen technology
• Types of GSE vehicles (e.g., buses, forklifts, …): GSE transitioning to H2
• Projection year: Selected year for forecasting H2 transition impacts
Example Screenshot - UI Mockup
Step 2 – Hydrogen Consumption Data sources
• Fleet Data Required:
• Growth rate
• Aircraft type and frequency of operations
• GSE types, quantities and operating patterns
• Aircraft data (aircraft_data.csv)
• GSE data (gse_data.csv)
Step 3 – Hydrogen Demand Calculation – Aircraft
Step 3 – Hydrogen Demand Calculation – GSE
• Hydrogen Demand Output
• Aircraft H2 volume
• GSE H2 volume
• Total H2 demand
• GSE chosen information
• Charts
Example Screenshot
Step 4: Storage Capacity & Land Calculation
• total_storage_volume = aircraft_H2_volume + GSE_H2_Volume
• usable_volume_of_LH2 = water_volume _ (1-ullage)_(1-evaporation_rate)
• #\_of_tanks = H2_demand_volume_per_day/usable_volume_of_LH2
• tank_footprint = width _ length
• H2_stockage_area = tank_footprint _ #\_of_tanks
• Storage Capacity & Land Calculation Output
• # of tanks
• Storage area required
• Charts
Example Screenshot
• Step 5: Regulatory Compliance – Distance
• Checking Compliance
• Convert storage volume (ft^3) à gallons
• Compare capacity to regulations
• Verify Safety distance and tank requirements
Step 5: Regulatory Compliance - Requirement
• Output – Regulatory Compliance
• Map
• Color Schemes
• Applicable regulations
Example Screenshot
Step 6: Sustainability Analysis
• Emission Reductions:
• Calculate CO₂ emissions reductions from replacing Jet A, Diesel, and Gasoline with Hydrogen
• total_emissions = jetA_emissions + diesel_emissions + gasoline_emissions
• Emission Factors:
• Jet A: 9.57 kg CO₂/lb
• Diesel: 22.38 kg CO₂/lb
• Gasoline: 19.64 kg CO₂/lb
• Environmental Benefits:
• Improved air quality
• Lower operational carbon footprint
• Output - Sustainability Analysis
• Charts
• Time series
Step 7:
• Costs Calculated:
• Initial Capital Investment: Tanks, infrastructure setup
• Operational Expenses: Maintenance, hydrogen procurement
• Incentives/Subsidies: Inflation Reduction Act and other financial incentives
Key Takeaways
• Clear hydrogen infrastructure planning guidance
• Regulatory compliance requirements
• Sustainability benefits
• Economic feasibility and incentives
