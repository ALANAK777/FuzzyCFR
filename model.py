import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from geopy.distance import geodesic

# Coordinates for major cities (you can add more)
city_coordinates = {
    'Gurgaon': (28.4595, 77.0266),'Delhi': (28.7041, 77.1025),'Mumbai': (19.0760, 72.8777), 'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639), 'Bangalore': (12.9716, 77.5946),'Hyderabad': (17.3850, 78.4867), 'Pune': (18.5204, 73.8567),
    'Ahmedabad': (23.0225, 72.5714),'Jaipur': (26.9124, 75.7873),'Lucknow': (26.8467, 80.9462),'Bhopal': (23.2599, 77.4126),
    'Patna': (25.5941, 85.1376),'Indore': (22.7196, 75.8577),'Kanpur': (26.4499, 80.3319),'Nagpur': (21.1458, 79.0882),
    'Visakhapatnam': (17.6868, 83.2185),'Vadodara': (22.3072, 73.1812), 'Surat': (21.1702, 72.8311),'Varanasi': (25.3176, 82.9739),
    'Amritsar': (31.6340, 74.8723),'Ludhiana': (30.9010, 75.8573), 'Agra': (27.1767, 78.0081),'Meerut': (28.9845, 77.7064),
    'Rajkot': (22.3039, 70.8022),'Coimbatore': (11.0168, 76.9558),'Madurai': (9.9252, 78.1198),'Nashik': (19.9975, 73.7898),
    'Jodhpur': (26.2389, 73.0243), 'Ranchi': (23.3441, 85.3096),'Guwahati': (26.1445, 91.7362),'Chandigarh': (30.7333, 76.7794),
    'Mysore': (12.2958, 76.6394),'Thrissur': (10.5276, 76.2144),'Thiruvananthapuram': (8.5241, 76.9366),'Vijayawada': (16.5062, 80.6480),
    'Gwalior': (26.2183, 78.1828),'Kochi': (9.9312, 76.2673),'Faridabad': (28.4089, 77.3178),'Noida': (28.5355, 77.3910),
    'Ghaziabad': (28.6692, 77.4538),'Dehradun': (30.3165, 78.0322),'Shimla': (31.1048, 77.1734),'Jammu': (32.7266, 74.8570),
    'Panaji': (15.4909, 73.8278),'Bhubaneswar': (20.2961, 85.8245),'Raipur': (21.2514, 81.6296),'Bilaspur': (22.0796, 82.1391),
    'Jabalpur': (23.1815, 79.9864),'Aurangabad': (19.8762, 75.3433),'Tirupati': (13.6288, 79.4192),'Rourkela': (22.2270, 84.8524),
    'Durgapur': (23.5204, 87.3119),'Silchar': (24.8333, 92.7789),'Shillong': (25.5788, 91.8933),'Kozhikode': (11.2588, 75.7804),
    'Alappuzha': (9.4981, 76.3388),'Navi Mumbai': (19.0330, 73.0297),'Chennai': (13.0827, 80.2707),'Coimbatore': (11.0168, 76.9558),
    'Madurai': (9.9252, 78.1198),'Tiruchirappalli': (10.7905, 78.7047),'Salem': (11.6643, 78.1460),'Tirunelveli': (8.7139, 77.7567),
    'Erode': (11.3410, 77.7172),'Vellore': (12.9165, 79.1325),'Thoothukudi': (8.7642, 78.1348),'Tiruppur': (11.1085, 77.3411),
    'Dindigul': (10.3673, 77.9803),'Thanjavur': (10.7870, 79.1378),'Sivagangai': (9.8477, 78.4815),'Virudhunagar': (9.5810, 77.9624),
    'Nagapattinam': (10.7672, 79.8420),'Ramanathapuram': (9.3762, 78.8308),'Namakkal': (11.2189, 78.1677),'Cuddalore': (11.7447, 79.7689),
    'Karur': (10.9571, 78.0792),'Theni': (10.0104, 77.4777),'Kanyakumari': (8.0883, 77.5385),'Krishnagiri': (12.5186, 78.2137),
    'Perambalur': (11.2320, 78.8806),'Ariyalur': (11.1428, 79.0782),'Nilgiris': (11.4916, 76.7337),'Ranipet': (12.9224, 79.3326),
    'Tiruvannamalai': (12.2253, 79.0747),'Villupuram': (11.9395, 79.4924),'Kallakurichi': (11.7376, 78.9597),'Chengalpattu': (12.6921, 79.9707),
    'Tenkasi': (8.9604, 77.3152),'Tirupattur': (12.4967, 78.5730),'Pudukkottai': (10.3797, 78.8205),'Thiruvarur': (10.7668, 79.6345),
    'Mayiladuthurai': (11.1036, 79.6491),'Dharmapuri': (12.1357, 78.1602)
}

# Function to calculate distance between Gurgaon and user-specified location
def calculate_distance_to_gurgaon(user_place):
    gurgaon_coords = city_coordinates['Gurgaon']  # Gurgaon coordinates
    if user_place in city_coordinates:
        user_place_coords = city_coordinates[user_place]
        return geodesic(gurgaon_coords, user_place_coords).kilometers
    else:
        print(f"Coordinates for '{user_place}' not found. Please provide a valid location.")
        print("Valid locations are:", ', '.join(city_coordinates.keys()))
        exit()

# Load the CSV files
vendordata = pd.read_csv('C:\\Users\\vilsons\\Desktop\\Ini Projects\\FuzzyCFR\\vendor_data.csv')
technicalrating = pd.read_csv('C:\\Users\\vilsons\\Desktop\\Ini Projects\\FuzzyCFR\\tech_rating.csv')

# Clean column names by stripping leading/trailing spaces
vendordata.columns = vendordata.columns.str.strip()
technicalrating.columns = technicalrating.columns.str.strip()

# Merge the two datasets on the 'FACADE VENDOR' column
if 'FACADE VENDOR' in vendordata.columns and 'FACADE VENDOR' in technicalrating.columns:
    merged_data = pd.merge(vendordata, technicalrating, on='FACADE VENDOR')
else:
    raise KeyError("'FACADE VENDOR' column is missing in one of the datasets")

# Drop duplicate columns if they exist
merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()]

# Preserve original vendor names and factory locations before encoding
vendor_names = merged_data['FACADE VENDOR']
factory_locations = merged_data['Factory Location']

# Convert categorical columns (object type) into numerical format
le = LabelEncoder()
for column in merged_data.select_dtypes(include=['object']).columns:
    merged_data[column] = le.fit_transform(merged_data[column])

# Convert 'Recommended' column ('YES'/'NO') to numerical values (1 for 'YES', 0 for 'NO')
if 'Recommended' in merged_data.columns:
    merged_data['Recommended'] = merged_data['Recommended'].apply(lambda x: 1 if x == 'YES' else 0)

# Get user input for location
user_place = input("Enter the location (e.g., Lucknow, Delhi, Jaipur, Mumbai): ")

# Calculate the distance from Gurgaon to the user-provided location
distance_to_user_place = calculate_distance_to_gurgaon(user_place)
print(f"Distance between Gurgaon and {user_place}: {distance_to_user_place:.2f} km")

# Update the 'Distance of Factory from Gurgaon (Kms)' column based on user-provided location
merged_data['Distance of Factory from Gurgaon (Kms)'] = distance_to_user_place

# Define features and target
X = merged_data.drop(columns=['FACADE VENDOR', 'Recommended'])  # Drop ID and target columns
y = merged_data['Recommended']

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the XGBoost model and train it
xgb_model = XGBClassifier()
xgb_model.fit(X_train, y_train)

# Predict using the test data
y_pred = xgb_model.predict(X_test)

# Evaluate the model
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nAccuracy Score: ", accuracy_score(y_test, y_pred))

# Adjust the ranking formula to reduce the impact of distance (normalizing by 100)
merged_data['Ranking_Score'] = (merged_data['Production Capacity'] * 0.3) + \
                               (merged_data['Turn Over'] * 0.2) + \
                               (merged_data['Past Similar projects'] * 0.2) + \
                               (merged_data['Average Rating'] * 0.1) - \
                               (merged_data['Distance of Factory from Gurgaon (Kms)'] / 100 * 0.2)


# Rank vendors based on the ranking score
ranked_vendors = merged_data.sort_values(by='Ranking_Score', ascending=False)

# Restore original vendor names and factory locations
ranked_vendors['FACADE VENDOR'] = vendor_names.iloc[ranked_vendors.index]
ranked_vendors['Factory Location'] = factory_locations.iloc[ranked_vendors.index]

# Print details of all vendors including the ranking score
print("All Vendors with Ranking:")
print(ranked_vendors[['FACADE VENDOR', 'Factory Location', 'Production Capacity', 'Turn Over', 'Past Similar projects', 'Distance of Factory from Gurgaon (Kms)', 'Average Rating', 'Ranking_Score']])

# Get the top two vendors
top_two_vendors = ranked_vendors.head(2)

# Print the top two vendors without index
print("\nTop Two Vendors:")
print(top_two_vendors[['FACADE VENDOR', 'Factory Location', 'Production Capacity', 'Turn Over', 'Past Similar projects', 'Distance of Factory from Gurgaon (Kms)', 'Average Rating', 'Ranking_Score']].to_string(index=False))
