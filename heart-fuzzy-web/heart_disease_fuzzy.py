# heart_disease_fuzzy.py - Manual Mamdani Fuzzy System (no skfuzzy ControlSystem)
import numpy as np
import skfuzzy as fuzz

# Universes (same as article)
chest_pain_univ = np.arange(0, 8, 1)
hba1c_univ = np.arange(3, 15, 0.1)
hdl_univ = np.arange(10, 81, 1)
ldl_univ = np.arange(40, 201, 1)
heart_rate_univ = np.arange(40, 161, 1)
age_univ = np.arange(20, 121, 1)
blood_pressure_univ = np.arange(80, 241, 1)
risk_univ = np.arange(0, 11, 0.1)

# Membership functions dicts
mf_chest_pain = {
    'no_pain': fuzz.trimf(chest_pain_univ, [0, 1, 2]),
    'non_anginal': fuzz.trimf(chest_pain_univ, [2, 3, 4]),
    'atypical': fuzz.trimf(chest_pain_univ, [4, 5, 6]),
    'typical': fuzz.trimf(chest_pain_univ, [6, 7, 8])
}

mf_hba1c = {
    'very_healthy': fuzz.trimf(hba1c_univ, [3, 5, 7]),
    'healthy': fuzz.trimf(hba1c_univ, [6.5, 7.75, 9]),
    'high': fuzz.trimf(hba1c_univ, [8.5, 11.25, 14])
}

mf_hdl = {
    'low': fuzz.trimf(hdl_univ, [10, 30, 50]),
    'healthy': fuzz.trimf(hdl_univ, [40, 60, 80])
}

mf_ldl = {
    'very_healthy': fuzz.trimf(ldl_univ, [40, 60, 80]),
    'healthy': fuzz.trimf(ldl_univ, [70, 90, 110]),
    'high': fuzz.trimf(ldl_univ, [100, 120, 140]),
    'very_high': fuzz.trimf(ldl_univ, [130, 150, 170]),
    'extra_high': fuzz.trimf(ldl_univ, [160, 180, 200])
}

mf_heart_rate = {
    'very_healthy': fuzz.trimf(heart_rate_univ, [40, 55, 70]),
    'healthy': fuzz.trimf(heart_rate_univ, [60, 80, 100]),
    'high': fuzz.trimf(heart_rate_univ, [90, 125, 160])
}

mf_age = {
    'young': fuzz.trimf(age_univ, [20, 32.5, 45]),
    'mid': fuzz.trimf(age_univ, [40, 52.5, 65]),
    'old': fuzz.trimf(age_univ, [60, 72.5, 85]),
    'very_old': fuzz.trimf(age_univ, [80, 100, 120])
}

mf_blood_pressure = {
    'normal': fuzz.trimf(blood_pressure_univ, [80, 110, 140]),
    'high': fuzz.trimf(blood_pressure_univ, [120, 160, 200]),
    'very_high': fuzz.trimf(blood_pressure_univ, [180, 210, 240])
}

mf_risk = {
    'healthy': fuzz.trimf(risk_univ, [0, 2, 4]),
    'low': fuzz.trimf(risk_univ, [2, 4, 6]),
    'medium': fuzz.trimf(risk_univ, [4, 6, 8]),
    'high': fuzz.trimf(risk_univ, [6, 8, 10])
}

# All linguistic labels
labels = {
    'chest_pain': list(mf_chest_pain.keys()),
    'hba1c': list(mf_hba1c.keys()),
    'hdl': list(mf_hdl.keys()),
    'ldl': list(mf_ldl.keys()),
    'heart_rate': list(mf_heart_rate.keys()),
    'age': list(mf_age.keys()),
    'blood_pressure': list(mf_blood_pressure.keys())
}

# Manual predict function
def predict_risk(cp, hba, hd, ld, hr, ag, bp):
    inputs = {'chest_pain': cp, 'hba1c': hba, 'hdl': hd, 'ldl': ld,
              'heart_rate': hr, 'age': ag, 'blood_pressure': bp}
    
    # Aggregated output membership
    aggregated = np.zeros_like(risk_univ)
    
    # Loop over all possible combinations (4320)
    import itertools
    for combo in itertools.product(*labels.values()):
        # Firing strength (MIN of memberships)
        firing = min(
            fuzz.interp_membership(chest_pain_univ, mf_chest_pain[combo[0]], inputs['chest_pain']),
            fuzz.interp_membership(hba1c_univ, mf_hba1c[combo[1]], inputs['hba1c']),
            fuzz.interp_membership(hdl_univ, mf_hdl[combo[2]], inputs['hdl']),
            fuzz.interp_membership(ldl_univ, mf_ldl[combo[3]], inputs['ldl']),
            fuzz.interp_membership(heart_rate_univ, mf_heart_rate[combo[4]], inputs['heart_rate']),
            fuzz.interp_membership(age_univ, mf_age[combo[5]], inputs['age']),
            fuzz.interp_membership(blood_pressure_univ, mf_blood_pressure[combo[6]], inputs['blood_pressure'])
        )
        
        if firing > 0:
            # Determine output label based on bad factors (same logic as before)
            bad_count = 0
            if combo[0] in ['atypical', 'typical']: bad_count += 2
            if combo[1] == 'high': bad_count += 2
            if combo[2] == 'low': bad_count += 2
            if combo[3] in ['very_high', 'extra_high']: bad_count += 3
            elif combo[3] == 'high': bad_count += 2
            if combo[4] == 'high': bad_count += 1
            if combo[5] in ['old', 'very_old']: bad_count += 2
            if combo[6] == 'very_high': bad_count += 3
            elif combo[6] == 'high': bad_count += 2
            
            if bad_count <= 3: out_label = 'healthy'
            elif bad_count <= 7: out_label = 'low'
            elif bad_count <= 11: out_label = 'medium'
            else: out_label = 'high'
            
            # Clip output mf
            clipped = np.fmin(firing, mf_risk[out_label])
            aggregated = np.fmax(aggregated, clipped)
    
    # Defuzzification (centroid - simple and close to article's average)
    if np.sum(aggregated) == 0:
        return 5.0  # fallback
    risk_value = fuzz.defuzz(risk_univ, aggregated, 'centroid')
    return risk_value