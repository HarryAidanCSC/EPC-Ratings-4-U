# %%
import ast
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.metrics import r2_score
import joblib



df = pd.read_csv(Path('data/OpenSynthReleaseDataBatch1.csv'))

valid_property_types = ['Detached', 'Semi Detached', 'Terraced', 'Flat']
df = df[df['property_type'].isin(valid_property_types)]


# Specify the columns to include
desired_columns = [
    'month_of_year','has_heat_pump', 'has_solar_pv', #
    'has_ev', 'property_type', 'kwh', 'energy_rating', 'urbanity'
]

df = df[desired_columns]

# Parse the `kwh` column as lists
df["kwh"] = df["kwh"].apply(lambda x: ast.literal_eval(x))

# Convert strings in the parsed arrays to integers and aggregate their sum
df["kwh"] = df["kwh"].apply(lambda x: sum(float(i) for i in x))


# Identify categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns
columns_to_keep = df.drop(columns=categorical_columns).reset_index(drop=True)

for column in categorical_columns:
    encoder = OneHotEncoder(drop='first', sparse_output=False)  # Use sparse_output=False for dense arrays

    encoded_arrays = encoder.fit_transform(df[[column]])  # Use [[column]] to keep the column as a DataFrame

    encoded_df = pd.DataFrame(
        encoded_arrays,
        columns=encoder.get_feature_names_out([column])  # Use a list with the column name
    )

    columns_to_keep = pd.concat([columns_to_keep, encoded_df.reset_index(drop=True)], axis=1)

df = columns_to_keep
# %%
# Define the dependent variable (target) and independent variables (features)
X = df.drop(columns=['kwh'])
y = df['kwh']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Model Coefficients: {model.coef_}")
print(f"Model Intercept: {model.intercept_}")
r2 = r2_score(y_test, y_pred)
print(f"R-squared: {r2}")

# Save model
joblib.dump(model, 'model/lr_model.pkl')