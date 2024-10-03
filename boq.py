import re
import pandas as pd
import json

# Define the feature extraction function for each row based on product description
def extract_features_from_row(row: pd.Series) -> dict:
    features = {}

    # Extract features based on the product description in 'Unnamed: 0' column
    product_description = row['Unnamed: 0']

    # Series (e.g., SKN, Alucobond, Framing Member)
    series_match = re.search(r'\bSKN[-\s]\d+\b|\b154\s*SKN\b|\bST[-\s]\d+\b|\bAlucobond\b|\bFraming Member\b', product_description, re.IGNORECASE)
    features['Series'] = series_match.group(0).strip() if series_match else None

    # Min Thickness (e.g., wind pressure or thickness mentions)
    thickness_match = re.search(r'(\b\d+\s*mm\b|\bminimum thickness of \d+\s*mm\b|\bminimum \d+\s*mm\b|\d+\s*mm thk\.|\bwind pressure\b)', product_description, re.IGNORECASE)
    features['Min Thickness'] = re.sub(r'(\bminimum thickness of\b|\bminimum\b|\sthk\.)', '', thickness_match.group(0)).strip() if thickness_match else None

    # Approved Makes (e.g., Saint Gobain, Alucobond, Hilti, Fischer)
    makes_match = re.search(r'(Saint\s*Gobain|Alucobond|Hilti|Fischer|Secondary\s*Steel\s*-?\s*M\.S\. structure)', product_description, re.IGNORECASE)
    features['Approved makes'] = makes_match.group(0).strip() if makes_match else None

    # Reflective Coating (e.g., surface mentions)
    reflective_coating_match = re.search(r'(surface\s*#\d+|Framing\s*member\s*-?\s*Finish)', product_description, re.IGNORECASE)
    features['Reflective coating'] = f"reflective coating shall be on {reflective_coating_match.group(0)}" if reflective_coating_match else None

    # Glass (e.g., insulated glass, laminated glass)
    glass_match = re.search(r'(insulated\s*glass\s*unit|insulated\s*glass|Glass\s*type\s*-?\s*Single\s*glass\s*/\s*Laminated|Laminated\s*Glass)', product_description, re.IGNORECASE)
    features['Glass'] = glass_match.group(0).strip() if glass_match else None

    # Special Seal (e.g., hermetically sealed, hardware)
    special_seal_match = re.search(r'(hermetically\s*sealed(?:\s*with\s*the\s*two\s*lites\s*of\s*glass)?|hardware)', product_description, re.IGNORECASE)
    features['Special seal'] = special_seal_match.group(0).strip() if special_seal_match else None

    # Air Gap (e.g., air space, glass type)
    air_gap_match = re.search(r'(\b\d+\s*mm\s*air\s*gap\b|\b\d+\s*mm\s*air\s*space\b|Glass\s*type\s*-?\s*Single\s*glass\s*/\s*Laminated)', product_description, re.IGNORECASE)
    features['Air Gap'] = re.sub(r'\s*air\s*space', ' air gap', air_gap_match.group(0).strip()) if air_gap_match else None

    # Spacer (e.g., black aluminum spacers, SGP/PVB)
    spacer_match = re.search(r'(black\s*aluminum\s*spacers|black\s*aluminium\s*spacers|SGP\s*/\s*PVB)', product_description, re.IGNORECASE)
    features['Spacer'] = spacer_match.group(0).strip() if spacer_match else None

    # Special Bend/Shape (e.g., Bent at corners, toughened clear glass)
    special_bend_shape_match = re.search(r'(Bent\s*at\s*corners|toughened\s*clear\s*glass)', product_description, re.IGNORECASE)
    features['Special bend/shape'] = special_bend_shape_match.group(0).strip() if special_bend_shape_match else None

    # Primary Sealant (e.g., Poly-Isobutylene, Spider fittings)
    primary_sealant_match = re.search(r'(Poly[-\s]*Isobutylene|Spider\s*fittings)', product_description, re.IGNORECASE)
    features['Primary Sealant'] = primary_sealant_match.group(0).strip() if primary_sealant_match else None

    # Secondary Silicon Sealant (e.g., Dow Corning, DC 991H, Silicone)
    secondary_sealant_match = re.search(r'(Dow\s*Corning\s*3362|DC\s*991H|Silicone|Sillicone)', product_description, re.IGNORECASE)
    features['Secondary silicon sealant'] = secondary_sealant_match.group(0).strip() if secondary_sealant_match else None

    # Codal Reference (e.g., BS EN, IS standards)
    codal_reference_match = re.search(r'(BS\s*EN\s*\d+|IS\s*875\s*part\s*III|AS\s*1288)', product_description, re.IGNORECASE)
    features['Codal reference'] = codal_reference_match.group(0).strip() if codal_reference_match else None

    # Special Treatment (e.g., heat strengthened, thermoplastic core, type of canopy)
    special_treatment_match = re.search(r'(heat\s*strengthened|thermoplastic\s*core\s*of\s*anti\s*oxidant\s*LDPE|Type\s*of\s*canopy\s*-?\s*Glass\s*canopy)', product_description, re.IGNORECASE)
    features['Special treatment'] = special_treatment_match.group(0).strip() if special_treatment_match else None

    return features

# Get input from the user for the product description
user_input = input("Enter the product description: ")

# Extract features from the user input
features = extract_features_from_row(pd.Series({'Unnamed: 0': user_input}))

# Display the extracted features
print("Extracted Features:")
print(json.dumps(features, indent=4))
