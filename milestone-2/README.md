# Ride-Sharing Analytics System

This project showcases a real-time analytics pipeline for a ride-sharing platform using Apache Spark, Azure Event Hub, Azure Blob Storage, and Streamlit. It includes synthetic data generation, real-time ingestion, processing, and an interactive dashboard.

---

##  Files

- `data_generation_streama.py`: Simulates and streams ride & driver data to Azure Event Hub.
- `streamlitt.py`: Streamlit dashboard that pulls data from Azure Blob Storage and visualizes KPIs.
- `requirements.txt`: Python dependencies.

---

## 🛠️ Technologies Used

- **Streamlit** – Front-end dashboard
- **Plotly** – Interactive charts
- **Apache Spark (Structured Streaming)** – Real-time processing
- **Azure Event Hub** – Kafka-compatible streaming
- **Azure Blob Storage** – Storage layer for structured data
- **Mimesis** – Fake data generation
- **Pandas, PyArrow** – Data manipulation and storage

