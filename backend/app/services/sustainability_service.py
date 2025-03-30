# File: sustainability_service.py

import matplotlib.pyplot as plt
import numpy as np

def emissions(jetA_weight, H2_weight, Fuel_weight):
    """
    Calculate and plot CO2 emissions (in metric tons) for two fleet scenarios:
      1. A hydrogen-jetA combination fleet (combining emissions from the jetA and the hydrogen fuel component).
      2. A pure jetA-only fleet.
      
    Inputs:
      - jetA_weight: Weight of Jet A fuel (in lbs) that is used in a hydrogen-jetA combination fleet.
      - H2_weight:   Weight of hydrogen fuel (in lbs) that is used in a hydrogen-jetA combination fleet.
      - Fuel_weight: Weight of Jet A fuel (in lbs) that is used in a jetA-only fleet.

    Returns:
      A tuple (jetA_co2, H2_co2, just_jetA_co2) representing:
        - jetA_co2: CO2 emissions (metric tons) for the jetA portion in the hydrogen-combination fleet.
        - H2_co2:   CO2 emissions (metric tons) for the H2-derived portion in the hydrogen-combination fleet.
        - just_jetA_co2: CO2 emissions (metric tons) for the pure jetA-only fleet.
    """
    # Constants
    lbstokgconversionfactor = 2.02  # lbs -> kg conversion factor
    jetAco2EI = 3.16                # kg CO2 per kg Jet A
    h2co2EI   = 1.5                 # kg CO2 per kg Hydrogen

    # Convert input weights from lbs to kg
    jetA_weight = jetA_weight / lbstokgconversionfactor
    H2_weight = H2_weight / lbstokgconversionfactor
    Fuel_weight = Fuel_weight / lbstokgconversionfactor

    # Compute CO2 emissions in metric tons
    jetA_co2 = (jetA_weight * jetAco2EI) / 1000
    H2_co2 = (H2_weight * h2co2EI) / 1000
    just_jetA_co2 = (Fuel_weight * jetAco2EI) / 1000

    # # Plotting the emissions breakdown
    # fig, ax = plt.subplots(figsize=(10, 6))

    # # Plot bars for the Hydrogen-combination fleet: Jet A is shown first, then H2 stacked above it.
    # ax.bar(0.5, jetA_co2, label='JetA CO2', color='lightcoral')
    # ax.bar(0.5, H2_co2, label='H2 CO2', color='cornflowerblue', bottom=jetA_co2)

    # # Plot bar for the JetA-only fleet
    # ax.bar(2, just_jetA_co2, label='Just JetA CO2', color='goldenrod')

    # # Formatting
    # ax.set_title('Mass of Emissions with and without Hydrogen Influence', color='white')
    # ax.set_xlabel('Scenario Index', color='white')
    # ax.set_ylabel('Emissions (Metric Tons)', color='white')
    # ax.legend()
    # plt.xticks([0.5, 2], ["Hydrogen + JetA Fleet", "Only JetA Fleet"], color='white')
    # plt.yticks(color='white')

    # # Set background and spine colors for improved aesthetics
    # ax.set_facecolor("#003057")
    # fig.patch.set_facecolor('#003057')
    # for spine in ax.spines.values():
    #     spine.set_color('white')

    # plt.show()

    return jetA_co2, H2_co2, just_jetA_co2

# Example usage
if __name__ == "__main__":
    # Example input weights (lbs) from your hydrogen demand tool outputs:
    jetA_weight_example = 10000  # lbs used in a hydrogen-jetA combination fleet
    H2_weight_example = 3000     # lbs used in a hydrogen-jetA combination fleet
    Fuel_weight_example = 15000  # lbs used in a pure jetA-only fleet

    jetA_co2, H2_co2, just_jetA_co2 = emissions(jetA_weight_example, H2_weight_example, Fuel_weight_example)
    print("Emissions for Hydrogen+JetA Fleet (JetA part):", jetA_co2, "metric tons")
    print("Emissions for Hydrogen+JetA Fleet (H2 part):", H2_co2, "metric tons")
    print("Emissions for JetA-Only Fleet:", just_jetA_co2, "metric tons")