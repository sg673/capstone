# Airport Delay Analytics - Capstone Project

A comprehensive data analytics solution for analyzing US airport delays, featuring an ETL pipeline and interactive Streamlit dashboard.

## Table of Contents

- <a href="#project-overview">Project Overview</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#features">Features</a>
- <a href="#installation">Installation</a>
- <a href="#usage">Usage</a>
- <a href="#data-sources">Data Sources</a>
- <a href="#key-metrics">Key Metrics</a>
- <a href="#dashboard-features">Dashboard Features</a>
- <a href="#testing">Testing</a>
- <a href="#configuration">Configuration</a>
- <a href="#logging">Logging</a>

## Project Overview

This capstone project consists of two main components:
1. **ETL Pipeline** - Extracts, transforms, and loads airport delay data
2. **Streamlit Dashboard** - Interactive web application for data visualization

The system processes airline delay data and airport information to provide insights into flight delays across US airports, carriers, and states.

## Project Structure

```
capstone/
├── etl_process/           # ETL Pipeline
│   ├── config/           # Configuration files
│   ├── data/             # Data storage (raw, processed, output)
│   ├── src/              # Source code
│   │   ├── extract/      # Data extraction modules
│   │   ├── transform/    # Data transformation modules
│   │   ├── load/         # Data loading modules
│   │   └── utils/        # Utility functions
│   ├── tests/            # Unit tests
│   ├── scripts/          # Executable scripts
│   └── notebooks/        # Jupyter notebooks
└── streamlit_app/        # Web Dashboard
    ├── nav_pages/        # Page components
    ├── app.py           # Main application
    └── util.py          # Utility functions
```

## Features

### ETL Pipeline
- **Extract**: Processes airline delay data and airport location data
- **Transform**: Cleans, validates, and merges datasets
- **Load**: Stores processed data in PostgreSQL database or CSV files
- **Logging**: Comprehensive logging system for monitoring
- **Testing**: Unit tests with coverage reporting

### Streamlit Dashboard
- **Interactive Charts**: Bar charts showing delay percentages by carrier, airport, or state
- **Geographic Visualization**: US map showing delay patterns by state
- **Filtering**: Multi-year selection and grouping options
- **Real-time Data**: Connects to database or local files

## Installation

### Prerequisites
- Python 3.6+
- PostgreSQL (optional, for database storage)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd capstone
```

2. **Install ETL Pipeline dependencies**
```bash
cd etl_process
pip install -e .
```


1. **Configure environment variables**
```bash
# Copy and edit environment files
cp etl_process/.env.dev etl_process/.env
```

## Usage

### Running the ETL Pipeline

```bash
cd etl_process
run_etl process [prod | dev]
```

Options:
- `dev`: Development environment (file-based storage)
- `prod`: Production environment (database storage)

### Running the Streamlit Dashboard

```bash
cd streamlit_app
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

### Running Tests

```bash
cd etl_process
python run_tests unit
```

## Data Sources

- **Airline Delay Data**: US Department of Transportation airline delay statistics: https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp?20=E
- **Airport Data**: Airport codes, names, and geographic coordinates: https://openflights.org/data.php

## Key Metrics

The system analyzes various delay types:
- **Carrier Delays**: Issues within airline's control
- **Weather Delays**: Weather-related delays
- **NAS Delays**: National Airspace System delays
- **Security Delays**: Security-related delays
- **Late Aircraft Delays**: Previous flight delays
> A flight is considered delayed when it arrived 15 or more minutes than the schedule. Delayed minutes are calculated for delayed flights only.
When multiple causes are assigned to one delayed flight, each cause is prorated based on delayed minutes it is responsible for. The displayed numbers are rounded and may not add up to the total.

## Dashboard Features

### Graph View
- Interactive bar charts
- Filter by year, carrier, airport, or state
- Sortable results (ascending/descending)
- Top 20 results display

### Map View
- US choropleth map
- State-level delay visualization
- Year and delay type filtering
- Color-coded intensity mapping

## Testing

The project includes comprehensive unit tests:
- Extract module tests
- Transform module tests
- Load module tests
- Configuration tests
- Utility function tests

Coverage reports are generated in `etl_process/htmlcov/`

## Configuration

### Environment Variables
- `ENV`: Environment type (dev/prod)
- `POST_DATA`: Save intermediate files (True/False)
- Database connection parameters for production


## Logging

Comprehensive logging system tracks:
- ETL pipeline execution
- Data extraction progress
- Transformation steps
- Load operations
- Error handling

Logs are stored in `etl_process/src/logs/`

> note: a large portion of this readme is AI generated