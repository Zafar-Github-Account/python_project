import streamlit as st

st.title("Unit Converter App")
st.markdown("### Convert Length, Weight, and Time Instantly")
st.write("Welcome! Select a category, enter a value, and get the converted result in real-time.")

# Select category
category = st.selectbox("Choose a category", ["Length", "Weight", "Time"])

# Unit options for each category
units = {
    "Length": ["Kilometer to Miles", "Miles to Kilometer"],
    "Weight": ["Kilogram to Pounds", "Pounds to Kilogram"],
    "Time": [
        "Second to Minutes", "Minutes to Seconds",
        "Minutes to Hours", "Hours to Minutes",
        "Hours to Days", "Days to Hours"
    ]
}

# Show unit options based on selected category
unit = st.selectbox("Choose conversion type", units[category])

# Enter value
value = st.number_input("Enter the value to convert", min_value=0)

# Conversion logic
def convert_units(category, value, unit):
    if category == "Length":
        if unit == "Kilometer to Miles":
            return value * 0.621371
        elif unit == "Miles to Kilometer":
            return value / 0.621371
    elif category == "Weight":
        if unit == "Kilogram to Pounds":
            return value * 2.20462
        elif unit == "Pounds to Kilogram":
            return value / 2.20462
    elif category == "Time":
        if unit == "Second to Minutes":
            return value / 60
        elif unit == "Minutes to Seconds":
            return value * 60
        elif unit == "Minutes to Hours":
            return value / 60
        elif unit == "Hours to Minutes":
            return value * 60
        elif unit == "Hours to Days":
            return value / 24
        elif unit == "Days to Hours":
            return value * 24
    return None

# Perform conversion
if st.button("Convert"):
    result = convert_units(category, value, unit)
    if result is not None:
        st.success(f"Converted result: {result:.2f}")
    else:
        st.error("Conversion type not supported.")
