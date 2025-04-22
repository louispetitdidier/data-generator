# Ride-Sharing Analytics System


## Overview

A real-time analytics platform for ride-sharing services that:
- Generates synthetic ride & driver data
- Processes streaming data with Apache Spark
- Stores processed data in Azure Blob Storage
- Visualizes KPIs through an interactive Streamlit dashboard

## Features

- **Real-time Data Pipeline**:
  - Kafka-compatible streaming via Azure Event Hub
  - Spark Structured Streaming for processing
  - Optimized parquet storage in Azure Blob

- **Interactive Dashboard**:
  - Real-time ride demand monitoring
  - Driver availability heatmaps
  - Revenue and cancellation analytics
  - Dynamic pricing insights

- **Data Generation**:
  - Synthetic ride requests with realistic distributions
  - Driver status simulation with geo-coordinates
  - Configurable demand patterns

## Technologies

| Component               | Technology                          |
|-------------------------|-------------------------------------|
| **Data Streaming**      | Azure Event Hub                     |
| **Stream Processing**   | Apache Spark (Structured Streaming) |
| **Storage**             | Azure Blob Storage (Parquet)        |
| **Dashboard**           | Streamlit + Plotly                  |
| **Data Generation**     | Mimesis + Faker                     |
| **Visualization**       | Plotly, Folium                      |

## Getting Started

### Prerequisites
- Azure account with Blob Storage and Event Hub
- Python 3.9+
- Java 11 (for Spark)
- Docker (optional)

### Installation
```bash
git clone https://github.com/yourusername/ride-sharing-analytics.git
cd ride-sharing-analytics
pip install -r requirements.txt
