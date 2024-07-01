import streamlit as st
import pickle
import pandas as pd

# Load model
with open('xgboost_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Title name of streamlit
st.title('Car Price Prediction')

# Example of using the platform
st.markdown(
    '<p style="color:gray;">Ex. Car Name: Toyota Camry | Kilometers Driven: 60,343 | Fuel Type: Petrol | Transmission: Automatic | Ownership: 1 | Manufacture(Year): 2016 | Engine: 2494 | Seats: 5</p>',
    unsafe_allow_html=True
)

# Create a form for receiving information
car_name = st.text_input('Car Name', value='Toyota Camry')
kms_driven = st.number_input('Kilometers Driven', min_value=0, value=60343)
fuel_type = st.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG', 'Electric'], index=0)
transmission = st.selectbox('Transmission', ['Manual', 'Automatic'], index=1)
ownership = st.number_input('Ownership', min_value=0, value=1)
manufacture = st.number_input('Manufacture(Year)', min_value=0, value=2016)
engine = st.number_input('Engine', min_value=0.0, value=2494.0)
seats = st.number_input('Seats', min_value=1, value=5)

car_age = 2022 - manufacture
engine_per_seat = engine / seats

# Make predictions when the user presses a button
if st.button('Predict'):
    # Create DataFrame for input
    input_data = pd.DataFrame({
        'car_name': [car_name],
        'kms_driven': [kms_driven],
        'fuel_type': [fuel_type],
        'transmission': [transmission],
        'ownership': [ownership],
        'engine_per_seat': [engine_per_seat],
        'Seats': [seats],
        'car_age': [car_age]
    })

    # Make a prediction
    prediction_inr = model.predict(input_data)[0]

    # Convert INR to other currencies (@ 1/7/2024)
    conversion_rates = {
        'USD': 0.012,  # conversion rate INR to USD
        'THB': 0.44    # conversion rate INR to THB
    }
    prediction_usd = prediction_inr * conversion_rates['USD']
    prediction_thb = prediction_inr * conversion_rates['THB']

    # Round the predictions to integer and format with commas
    prediction_inr = "{:,.0f}".format(round(prediction_inr))
    prediction_usd = "{:,.0f}".format(round(prediction_usd))
    prediction_thb = "{:,.0f}".format(round(prediction_thb))

    # Display predictions in multiple currencies
    st.markdown(f"""
        <p style="font-size:24px;">Predicted Car Price: INR {prediction_inr}</p>
        <p style="font-size:24px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; USD {prediction_usd}</p>
        <p style="font-size:24px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; THB {prediction_thb}</p>
    """, unsafe_allow_html=True)

    # Add candidate information 
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown('<p style="color:gray; text-align:center;">Candidate: Natdanai Sriapai, Phone: 0640911178</p>',
    unsafe_allow_html=True
)