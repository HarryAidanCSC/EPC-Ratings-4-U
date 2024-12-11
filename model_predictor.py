# %%
import joblib
import pandas as pd
from pathlib import Path

class PredictMWH:
    def __init__(self):
        self.loaded_model = joblib.load(Path('model/lr_model.pkl'))
    
    def user_data(self, user_data):
        self.user_data = user_data
        self.user_data = pd.DataFrame(self.user_data, index=[0])
        return self.user_data

    def predict(self):
        return self.loaded_model.predict(self.user_data)[0]


p = PredictMWH()
p.user_data({'month_of_year' : 12, 'day_of_week': 6, 'has_heat_pump': 0, 'has_home_battery' : 0,
       'has_solar_pv' : 0, 'has_electric_hot_water': 0, 'has_electric_radiator': 0,
       'is_mains_gas': 1, 'has_ev': 0, 'has_lct': 0, 'property_type_Detached': 1,
       'property_type_Dwelling': 0, 'property_type_Flat': 0, 'property_type_House': 0,
       'property_type_Non_residential': 0, 'property_type_Semi_Detached': 0,
       'property_type_Terraced': 0, 'energy_rating_D_E': 0, 'energy_rating_F_G': 1,
       'urbanity_Urban': 1})

outcome = p.predict()
print(outcome)