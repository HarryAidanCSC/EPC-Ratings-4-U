# EPC-Ratings-4-U

## Running the app

Run the app by entering the below into a terminal:

``` shell
streamlit run app/home.py
```

## Example Product Vision 1

Understanding whether you have an accurate EPC rating is hard, but can be important if you're looking at getting a new certificate. 

We can use data from smart meters to make that process easier. We propose using data from the EPC register matched against smart meter data to understand when you're likely to be an outlier.

### Required Work

There's some backend work required to setup the analysis.
1. Match EPC register data to smart meter data to understand what an outlier looks like. If we have data about EPC changes over time that will be easier as you can infer what type of smart meter readings have led to a recently changed EPC rating. If historical data isn't available then we'll likely just need to understand which are the least standard smart meter readings for that rating, and use that to make our judgement. This is also a matching proble. Kalusa data has the smart meter readings. We should look at the properties here and find their EPC register data so our dataset always has both.
2. Clean and prepare this dataset for model training.
3. Train the model, so we infer the likelihood of being an outlier given the EPC data and the smart meter readings for new properties.

There's some frontend work required as well.
1. A user needs to be able to input their smart meter readings and get an EPC rating.
2. For the prototype, just let them select from a property in the Kalusa dataset, but mention that we'll have an extension that'll link in with their energy provider. This already happens see SERL as an example.
3. Given these readings, then we suggest their likelihood of being an outlier
4. If we have time also make some recommendations as well.


