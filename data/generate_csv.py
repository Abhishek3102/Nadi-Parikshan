import numpy as np
import pandas as pd

num_entries = 120

vata_diseases = [
    "Insomnia or Anxiety", "Arthritis", "Sciatica", "Constipation", "Tremors", "Parkinson's disease", "Rheumatoid arthritis", 
    "Irritable bowel syndrome (IBS)", "Dry skin", "Psoriasis", "Eczema", "Poor circulation", "Varicose veins", "Memory loss",
    "Fatigue", "Cold extremities", "Dry hair", "Restlessness", "Poor concentration", "Headaches", "Joint pain", "Nerve pain", 
    "Weak immunity", "Low body weight", "Menstrual irregularities", "Asthma", "Chronic dryness", "Miscarriage", "Hearing problems", 
    "Weight loss", "Osteoporosis", "Restless leg syndrome", "Urinary incontinence", "Cold hands and feet", "Low bone density", 
    "Sleep disturbances", "Weak digestion", "Bloating", "Excessive thirst", "Joint stiffness"
]

pitta_diseases = [
    "Acid Reflux or Skin Issues", "Heartburn", "Skin conditions (acne, rosacea)", "Ulcers", "Crohn's disease", "IBD", 
    "Hyperacidity", "Jaundice", "Liver disease", "Gallstones", "Hypertension", "Fever", "Inflammation", "Hot flashes", 
    "Excessive sweating", "Skin rashes", "Eye problems", "Migraine", "Stroke", "High blood pressure", "Bleeding disorders", 
    "Cystic acne", "Peptic ulcers", "Insomnia", "Diarrhea", "Hyperthyroidism", "Gall bladder issues", "Heat rash", "Urinary tract infections (UTIs)", 
    "Digestive inflammation", "Liver problems", "Blood sugar imbalance", "Mood swings", "Intense cravings", "Dehydration", "Nausea", 
    "Cystitis", "Excessive hunger", "Nosebleeds", "Heat intolerance", "Acne flare-ups"
]

kapha_diseases = [
    "Obesity or Hypertension", "Asthma", "Allergies", "Sinusitis", "Chronic cold and flu", "Sleep apnea", "Bronchitis", 
    "COPD", "Cystic fibrosis", "Swollen lymph nodes", "Water retention", "Edema", "Heavy legs", "Sinus infections", 
    "Mucus congestion", "Congestive heart failure", "Nasal congestion", "Depression", "Hypothyroidism", "Slow digestion", 
    "Lethargy", "Weakness", "Weak immune system", "Sluggish circulation", "Cold extremities", "Joint stiffness", "Greasy skin", 
    "Sleepiness after meals", "Overweight", "Diabetes-related complications", "Allergic rhinitis", "High cholesterol", "Gallstones", 
    "Clogged arteries", "Sore throat", "Dull headaches", "Respiratory infections", "Slow recovery from illness", "Fatigue", "Mucous buildup"
]

all_diseases = vata_diseases + pitta_diseases + kapha_diseases

np.random.shuffle(all_diseases)

nadi_dominance = []
diseases = []

for i in range(num_entries):
    if i < 40:
        nadi_dominance.append("Vata")
        diseases.append(vata_diseases[i])
    elif i < 80:
        nadi_dominance.append("Pitta")
        diseases.append(pitta_diseases[i - 40])
    else:
        nadi_dominance.append("Kapha")
        diseases.append(kapha_diseases[i - 80])

vata = np.random.randint(0, 101, size=num_entries)
pitta = np.random.randint(0, 101, size=num_entries)
kapha = np.random.randint(0, 101, size=num_entries)

total = vata + pitta + kapha
vata = np.round((vata / total) * 100, 2)
pitta = np.round((pitta / total) * 100, 2)
kapha = np.round((kapha / total) * 100, 2)

time_of_day = np.random.choice(["Morning", "Afternoon", "Evening", "Night"], size=num_entries)

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
    "Dosha Dominance": nadi_dominance,
    "Prominent Disease": diseases
})

file_path_extended = "nadi_pariksha_extended_with_dosha_and_unique_disease.csv"
extended_data.to_csv(file_path_extended, index=False)

file_path_extended
