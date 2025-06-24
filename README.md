# Climate-Resilient Agriculture System

This project develops an advanced climate monitoring and prediction system focused on **Climate-Resilient Agriculture**. It aims to provide farmers and agricultural policymakers with data-driven insights to mitigate the impacts of climate change and enhance food security.

## Features (Planned/Under Development)

-   **Climate Data Visualization:** Interactive dashboards for historical and projected climate data.
-   **Crop Suitability Analysis:** Recommendations for optimal crop varieties based on regional climate conditions.
-   **Precision Irrigation Guidance:** Data-driven insights for efficient water management.
-   **Agricultural Hazard Alerts:** Early warnings for droughts, floods, heatwaves, and pest outbreaks.
-   **Yield Prediction:** Forecasting crop yields under various climate scenarios.

## Architecture

The system is designed with a modular architecture, including:

-   **Data Ingestion Layer:** Collects data from various climate APIs (NOAA CDO, Copernicus CDS, NASA Earth).
-   **Data Processing and Storage Layer:** Cleans, transforms, and stores climate data.
-   **Machine Learning and Analytics Layer:** Develops and deploys predictive models.
-   **Application Layer:** Provides user interfaces (Streamlit dashboard).
-   **API Management and Security Layer:** Manages API keys and ensures secure access.

## Setup and Installation

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)
-   Access to NOAA CDO API, Copernicus CDS API, and NASA Earth API keys.
    -   **NOAA CDO API:** Obtain a token from [NOAA NCDC](https://www.ncdc.noaa.gov/cdo-web/webservices/v2).
    -   **Copernicus CDS API:** Register at [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/user/register) and follow instructions to set up your `.cdsapirc` file (see [CDSAPI setup](https://cds.climate.copernicus.eu/how-to-api)).
    -   **NASA Earth API:** Obtain an API key from [NASA Open APIs](https://api.nasa.gov/).



### 1. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

###2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory of the project (`climate_resilient_agriculture/`) and add API keys:

```
NOAA_API_KEY="your_noaa_api_key"
COPERNICUS_UID="your_copernicus_uid"
COPERNICUS_API_KEY="your_copernicus_api_key"
NASA_API_KEY="your_nasa_api_key"
```

### 4. Running the Streamlit Application

```bash
streamlit run main.py
```

This will open the application in web browser.

## Project Structure

```
climate_resilient_agriculture/
├── main.py
├── requirements.txt
├── .env
├── src/
│   ├── data/
│   │   └── data_ingestion.py
│   ├── models/
│   └── utils/
└── README.md
```

