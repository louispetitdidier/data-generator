# -*- coding: utf-8 -*-
"""streamlitt

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z99SO7VhKpN0IdaAJ5FL2J7m44PDkFc5
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import numpy as np

# --- Configuration ---
st.set_page_config(page_title="Ride Analytics", layout="wide", page_icon="")
st.title("Ride-Sharing Analytics Dashboard")

# --- Data Loading (with caching) ---
@st.cache_data(ttl=300)  # Refresh every 5 minutes
def load_data():
    # Azure Blob Storage config (move to secrets in production)
    blob_service_client = BlobServiceClient(
        account_url="https://iesstsabdbaa.blob.core.windows.net/",
        credential="yfqMW8gf8u+M5pOW33Q5gtRTFBJQXStVK4K2rlCVVzxlrRG21Sh7MVj06uExoL86Npb7HWWgxYUe+ASthUr6/g=="  # Use st.secrets in production
    )

    def load_parquet_from_blob(path_prefix):
        container_client = blob_service_client.get_container_client("group7")
        blob_list = container_client.list_blobs(name_starts_with=path_prefix)
        dataframes = []
        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob.name)
            stream = BytesIO(blob_client.download_blob().readall())
            try:
                df = pd.read_parquet(stream)
                dataframes.append(df)
            except Exception:
                continue
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

    ride_df = load_parquet_from_blob("optimized_ride_data")
    driver_df = load_parquet_from_blob("optimized_driver_data")

    # Data preprocessing
    for df in [ride_df, driver_df]:
        df.dropna(inplace=True)

    if "datetime" in ride_df.columns:
        ride_df["datetime"] = pd.to_datetime(ride_df["datetime"])
        ride_df["hour"] = ride_df["datetime"].dt.hour
        ride_df["day_of_week"] = ride_df["datetime"].dt.day_name()

    if "timestamp" in driver_df.columns:
        driver_df["timestamp"] = pd.to_datetime(driver_df["timestamp"])

    return ride_df, driver_df

ride_df, driver_df = load_data()

# --- Basic Analytics ---
st.header("Basic Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rides", len(ride_df))
col2.metric("Completed Rides", len(ride_df[ride_df["status"] == "completed"]))
col3.metric("Active Drivers", len(driver_df[driver_df["status"].isin(["available", "on_trip"])]))
col4.metric("Avg Ride Price", f"${ride_df['estimate_price'].mean():.2f}")

# Basic Visualizations
tab1, tab2, tab3 = st.tabs(["Status Distribution", "Hourly Demand", "Ride Duration"])

with tab1:
    fig = px.pie(ride_df, names="status", title="Ride Status Distribution",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    hourly = ride_df.groupby("hour").size().reset_index(name="count")
    fig = px.bar(hourly, x="hour", y="count", title="Hourly Ride Demand Pattern")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    if "estimated_distance_km" in ride_df.columns:
        fig = px.box(ride_df, x="ride_type", y="estimated_distance_km",
                    title="Ride Distance by Type (km)")
        st.plotly_chart(fig, use_container_width=True)

# --- Intermediate Analytics ---
st.header("Business Insights")

# Add only the cancellation rate metric here
cancelled_rides = len(ride_df[ride_df["status"] == "cancelled"])
total_rides = len(ride_df)
cancellation_rate = (cancelled_rides / total_rides) * 100 if total_rides > 0 else 0
st.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")

# Demand-Supply Analysis
st.subheader("Demand-Supply Matching")
col1, col2 = st.columns(2)

with col1:
    # Driver Utilization
    status_counts = driver_df["status"].value_counts()
    fig = go.Figure(go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker_colors=['#2ca02c', '#ff7f0e', '#d62728']
    ))
    fig.update_layout(title_text="Driver Utilization")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Cancellation Analysis
    cancelled = ride_df[ride_df["status"] == "cancelled"]
    if not cancelled.empty:
        fig = px.scatter(cancelled, x="estimate_price", y="estimated_distance_km",
                        color="ride_type", title="Cancelled Rides Analysis",
                        trendline="lowess")
        st.plotly_chart(fig, use_container_width=True)

# Revenue Analysis
st.subheader("Revenue Analytics")
rev_fig = px.violin(ride_df, y="estimate_price", x="ride_type", box=True,
                   title="Price Distribution by Ride Type")
st.plotly_chart(rev_fig, use_container_width=True)

# --- Advanced Analytics ---
st.header("Advanced Analytics")

# Anomaly Detection
st.subheader("Anomaly Detection")
if "estimated_distance_km" in ride_df.columns:
    # Simple statistical anomaly detection
    mean_dist = ride_df["estimated_distance_km"].mean()
    std_dist = ride_df["estimated_distance_km"].std()
    anomalies = ride_df[
        (ride_df["estimated_distance_km"] > mean_dist + 3*std_dist) |
        (ride_df["estimated_distance_km"] < mean_dist - 3*std_dist)
    ]

    if not anomalies.empty:
        fig = px.scatter(ride_df, x="datetime", y="estimated_distance_km",
                        title="Ride Distance Anomalies",
                        color=ride_df["estimated_distance_km"].apply(
                            lambda x: "Anomaly" if abs(x - mean_dist) > 3*std_dist else "Normal"))
        fig.add_hline(y=mean_dist + 3*std_dist, line_dash="dot")
        fig.add_hline(y=mean_dist - 3*std_dist, line_dash="dot")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No distance anomalies detected")

# Surge Pricing Potential
st.subheader("Surge Pricing Opportunities")
if "demand_level" in ride_df.columns:
    surge_data = ride_df.groupby(["hour", "demand_level"]).size().unstack().fillna(0)
    fig = px.line(surge_data, title="Demand Levels by Hour",
                 labels={"value": "Ride Count", "hour": "Hour of Day"})
    st.plotly_chart(fig, use_container_width=True)
