import numpy as np
import pandas as pd

num_entries = 1000
time_of_day = np.random.choice(["Morning", "Afternoon", "Evening", "Night"], size=num_entries)

vata = np.random.randint(0, 101, size=num_entries)
pitta = np.random.randint(0, 101, size=num_entries)
kapha = np.random.randint(0, 101, size=num_entries)

total = vata + pitta + kapha
vata = np.round((vata / total) * 100, 2)
pitta = np.round((pitta / total) * 100, 2)
kapha = np.round((kapha / total) * 100, 2)

def determine_dominance_and_disease(vata, pitta, kapha):
    if vata > pitta and vata > kapha:
        return "Vata", "Insomnia or Anxiety"
    elif pitta > vata and pitta > kapha:
        return "Pitta", "Acid Reflux or Skin Issues"
    else:
        return "Kapha", "Obesity or Hypertension"

dominance_and_disease = [determine_dominance_and_disease(v, p, k) for v, p, k in zip(vata, pitta, kapha)]
dosha_dominance, prominent_disease = zip(*dominance_and_disease)

time_of_day_factor = {
    "Morning": [0.9, 0.8, 1.1],
    "Afternoon": [1.0, 1.2, 0.9],
    "Evening": [1.1, 0.9, 0.8],
    "Night": [1.2, 0.8, 1.0],
}

vata_adjusted, pitta_adjusted, kapha_adjusted = [], [], []
for v, p, k, t in zip(vata, pitta, kapha, time_of_day):
    factors = time_of_day_factor[t]
    vata_adjusted.append(np.round(v * factors[0], 2))
    pitta_adjusted.append(np.round(p * factors[1], 2))
    kapha_adjusted.append(np.round(k * factors[2], 2))

extended_data = pd.DataFrame({
    "Vata": vata_adjusted,
    "Pitta": pitta_adjusted,
    "Kapha": kapha_adjusted,
    "Dosha Dominance": dosha_dominance,
    "Prominent Disease": prominent_disease
})

file_path_extended = "data/nadi_pariksha_extended_with_dosha_and_disease.csv"
extended_data.to_csv(file_path_extended, index=False)
file_path_extended
