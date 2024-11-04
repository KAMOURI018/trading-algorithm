# Trading Algorithm on Interactive Brokers

This repository hosts a trading algorithm designed to perform pairs trading between TLT ATM covered calls and TLTW. The algorithm includes risk management, visualization of trading signals, and is built for deployment using Docker, Kubernetes, and CI/CD with GitHub Actions.

## Project Overview

### Features

1. **Data Ingestion**: Retrieves TLT and TLTW prices and TLT options with Greeks, storing data in a low-latency Redis database.
2. **Pairs Trading Strategy**: Implements a pairs trading strategy using the Fractional Kelly Criterion for order sizing.
3. **Risk Management**: Monitors position limits and applies stop-loss thresholds.
4. **Visualization**: Uses FastAPI to display trading signals and spread plots between TLT and TLTW.
5. **Monitoring and Logging**: Provides real-time monitoring using Grafana and centralized logging with the ELK stack (Elasticsearch, Logstash, Kibana).
6. **Deployment**: Dockerized services, orchestrated with Kubernetes, and automated using GitHub Actions for CI/CD.

### System Architecture

The architecture consists of the following services:
- **Data Ingestion**: Collects real-time price data and options Greeks from Interactive Brokers.
- **Strategy Execution**: Executes the pairs trading strategy based on the TLT/TLTW spread.
- **Risk Management**: Monitors positions and manages risk through position limits and stop-loss mechanisms.
- **Visualization**: Displays trading signals and spread plots using FastAPI.
- **Monitoring**: Uses Grafana and the ELK stack to monitor system health and log events.

## Directory Structure

```plaintext
trading-algorithm/
├── data-ingestion/
│   ├── Dockerfile
│   └── data_ingestion.py
├── strategy/
│   ├── Dockerfile
│   └── strategy.py
├── risk-management/
│   ├── Dockerfile
│   └── risk_management.py
├── visualization/
│   ├── Dockerfile
│   └── visualization.py
├── monitoring/
│   ├── Dockerfile
│   └── monitoring_dashboard.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── k8s-deployment.yaml
