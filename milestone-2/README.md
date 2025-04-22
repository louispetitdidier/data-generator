# Ride-Sharing Analytics System


## Overview

An analytics platform for ride-sharing services that:
- Generates synthetic ride & driver data
- Processes streaming data with Apache Spark
- Stores processed data in Azure Blob Storage
- Visualizes KPIs through an interactive Streamlit dashboard

## Features

- **Data Pipeline**:
  - Kafka-compatible streaming via Azure Event Hub
  - Spark Structured Streaming for processing
  - Optimized parquet storage in Azure Blob

- **Interactive Dashboard**:
  - Ride demand monitoring
  - Driver availability heatmaps
  - Revenue and cancellation analytics
  - Dynamic pricing insights

- **Data Generation**:
  - Synthetic ride requests with realistic distributions
  - Driver status simulation with geo-coordinates
  - Configurable demand patterns


## Files
| File | Purpose |
|------|---------|
| `data_generation_streama.py` | Generates synthetic ride requests and driver status data, streaming to Azure Event Hub |
| `streamlitt.py` | Streamlit dashboard that loads processed data from Azure Blob Storage and displays interactive visualizations |
| `requirements.txt` | Lists all Python dependencies needed to run the system |


