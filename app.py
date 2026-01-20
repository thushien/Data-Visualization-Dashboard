import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Engineering Data Analytics Dashboard", layout="wide")

st.title("📊 Engineering Research Data Dashboard")
st.markdown("""
Developed by **Thushan Amarasinghege** *PhD Candidate, Laurentian University*
""")

# --- 1. Data Generation (Simulating Engineering Sensors) ---
@st.cache_data
def load_engineering_data():
    time = np.linspace(0, 100, 500)
    data = pd.DataFrame({
        'Time (s)': time,
        'Temperature (°C)': 20 + 5 * np.sin(time/5) + np.random.normal(0, 0.5, 500),
        'Vibration (Hz)': np.random.normal(50, 2, 500),
        'Strain (με)': 100 + 20 * np.log1p(time) + np.random.normal(0, 1, 500)
    })
    return data

df = load_engineering_data()

# --- 2. Sidebar Filters ---
st.sidebar.header("Filter Parameters")
sensor_selection = st.sidebar.multiselect(
    "Select Sensors to Visualize:",
    options=['Temperature (°C)', 'Vibration (Hz)', 'Strain (με)'],
    default=['Temperature (°C)', 'Strain (με)']
)

# --- 3. Main Dashboard Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Temperature", f"{df['Temperature (°C)'].mean():.2f} °C")
with col2:
    st.metric("Max Vibration", f"{df['Vibration (Hz)'].max():.2f} Hz")
with col3:
    st.metric("Peak Strain", f"{df['Strain (με)'].max():.2f} με")

st.divider()

# --- 4. Interactive Plotting ---
st.subheader("Time-Series Analysis")
if sensor_selection:
    fig = px.line(df, x='Time (s)', y=sensor_selection, 
                  title="Sensor Output Over Time",
                  template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one sensor from the sidebar.")

# --- 5. Statistical Distribution ---
st.subheader("Data Distribution & Correlation")
c1, c2 = st.columns(2)

with c1:
    st.write("Histogram of Sensor Readings")
    hist_sensor = st.selectbox("Choose sensor for distribution:", options=sensor_selection if sensor_selection else ['Temperature (°C)'])
    fig_hist = px.histogram(df, x=hist_sensor, nbins=30, marginal="box")
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.write("Correlation Heatmap")
    corr = df.corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
    st.plotly_chart(fig_corr, use_container_width=True)
