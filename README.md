# Hydrogen Infrastructure Dashboard

## Overview

The **Hydrogen Infrastructure Dashboard** is a full-stack application designed to analyze and visualize hydrogen infrastructure needs at airports. The project evaluates storage requirements, operational feasibility, cost impact, and compliance with safety regulations. The dashboard provides decision-makers with a tool to assess various hydrogen demand scenarios and their impact on infrastructure and costs.

## Features

- **Hydrogen Demand Calculation**: Estimates hydrogen fuel needs based on fleet percentage and operational requirements.
- **Storage Capacity Analysis**: Determines space and regulatory constraints for hydrogen storage at airports.
- **Cost Impact Assessment**: Evaluates financial implications, including turnaround time effects and infrastructure costs.
- **Geospatial Visualization**: Uses **Leaflet** to display hydrogen storage locations and land use requirements.
- **Economic Analysis**: Assesses financial feasibility, revenue impact, and tax incentives related to hydrogen adoption.
- **Sustainability Analysis**: Evaluates environmental benefits, regulatory alignment, and long-term sustainability goals.
- **Interactive Dashboard**: Developed using **Vue 3** and **Vite** for a dynamic user experience.

## Tech Stack

- **Frontend**: Vue 3, Vite, Leaflet
- **Backend**: Flask (Python)
- **Data Processing**: Python (Pandas, NumPy)
- **Mapping & Visualization**: Leaflet.js, Chart.js

## Installation

### Prerequisites

Ensure you have the following installed:

- Node.js & npm
- Python 3.8+
- pip (Python package manager)

### Clone Repository

```sh
git clone https://github.com/falbertoli/dashboard.git
cd dashboard
```

### Backend Setup

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```sh
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```

## Usage

- Open `http://localhost:5173/` in your browser to access the dashboard.
- Use the dashboard to input demand parameters, visualize storage locations, and analyze cost impacts.
- Adjust parameters dynamically to evaluate different scenarios.

## Hydrogen Demand Analysis

- **Fleet Utilization**: Calculates hydrogen demand based on the percentage of aircraft transitioning to hydrogen fuel.
- **List of Ground Fleet Equipment**: Includes hydrogen-powered ground support vehicles such as baggage tugs, fuel trucks, pushback tractors, and maintenance vehicles.
- **Operational Scenarios**: Evaluates hydrogen demand for a full year to accommodate seasonal variations and peak operational loads.
- **Storage Requirements**: Determines the amount of hydrogen required and the infrastructure needed for refueling operations.
- **Safety and Compliance**: Ensures hydrogen demand meets regulatory safety requirements for airport operations.

## Economic Impact

- **Cost Analysis**: Assesses the cost of hydrogen adoption, including infrastructure, storage, handling, and operational changes.
- **Revenue Impact**: Evaluates the effect of hydrogen transition on airline revenue due to turnaround time variations.
- **Tax Incentives**: Incorporates available government incentives and tax credits to offset hydrogen infrastructure costs.

## Sustainability Impact

- **Environmental Benefits**: Hydrogen adoption reduces carbon emissions, contributing to cleaner air travel.
- **Regulatory Compliance**: Aligns with the **Paris Agreement** and other international sustainability mandates.
- **Long-term Feasibility**: Supports a transition towards net-zero aviation by promoting green energy solutions.
