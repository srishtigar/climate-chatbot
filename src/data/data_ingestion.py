
import requests
import os
import pandas as pd
from datetime import datetime, timedelta

class NOAA_CDO_API:
    def __init__(self):
        self.api_key = os.getenv("NOAA_API_KEY")
        self.base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2"
        if not self.api_key:
            raise ValueError("NOAA_API_KEY not found in environment variables.")

    def _make_request(self, endpoint, params=None):
        headers = {"token": self.api_key}
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_datasets(self):
        return self._make_request("datasets")

    def get_datatypes(self, datasetid=None):
        params = {"datasetid": datasetid} if datasetid else None
        return self._make_request("datatypes", params)

    def get_locations(self, datasetid=None, locationcategoryid=None):
        params = {"datasetid": datasetid, "locationcategoryid": locationcategoryid} if datasetid else None
        return self._make_request("locations", params)

    def get_data(self, datasetid, datatypeid, locationid, startdate, enddate, units="metric", limit=1000):
        params = {
            "datasetid": datasetid,
            "datatypeid": datatypeid,
            "locationid": locationid,
            "startdate": startdate,
            "enddate": enddate,
            "units": units,
            "limit": limit
        }
        data = self._make_request("data", params)
        return data.get("results", [])

    def get_daily_summaries(self, locationid, start_date, end_date, datatypeid='TMAX,TMIN,PRCP'):
        # Example: Fetch TMAX, TMIN, PRCP for a given location and date range
        data = self.get_data(
            datasetid="GHCND", # Global Historical Climatology Network Daily
            datatypeid=datatypeid,
            locationid=locationid,
            startdate=start_date,
            enddate=end_date,
            units="metric",
            limit=1000 # Adjust limit as needed, or implement pagination
        )
        df = pd.DataFrame(data)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.pivot_table(index='date', columns='datatype', values='value')
            return df
        return pd.DataFrame()


class Copernicus_CDS_API:
    def __init__(self):
        # CDS API requires a .cdsapirc file with url and key
        # This class will primarily guide the user on how to set it up
        # and provide example usage, as direct programmatic access via requests is not straightforward
        # due to the need for the cdsapi library and .cdsapirc file.
        pass

    def get_era5_data_example(self):
        example_code = """
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            '2m_temperature', 'total_precipitation', 'surface_solar_radiation_downwards',
            'leaf_area_index_high_vegetation', 'leaf_area_index_low_vegetation',
            'soil_temperature_level_1', 'soil_temperature_level_2',
            'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
        ],
        'year': '2023',
        'month': '01',
        'day': '01',
        'time': '12:00',
        'format': 'netcdf',
    },
    'download.nc')
"""
        return example_code


class NASA_Earth_API:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov/planetary/earth/assets"
        if not self.api_key:
            raise ValueError("NASA_API_KEY not found in environment variables.")

    def get_landsat_asset(self, lon, lat, date, dim=0.025):
        params = {
            "lon": lon,
            "lat": lat,
            "date": date,
            "dim": dim, # degrees, width and height of the image
            "api_key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_landsat_imagery_url(self, lon, lat, date, dim=0.025, cloud_score=True):
        params = {
            "lon": lon,
            "lat": lat,
            "date": date,
            "dim": dim,
            "cloud_score": cloud_score,
            "api_key": self.api_key
        }
        response = requests.get("https://api.nasa.gov/planetary/earth/imagery", params=params)
        response.raise_for_status()
        return response.url


if __name__ == "__main__":
    # Example Usage (requires API keys set as environment variables)
    # For Copernicus, you need to install cdsapi and configure .cdsapirc

    # NOAA Example
    try:
        print("\n--- NOAA CDO API Example ---")
        noaa = NOAA_CDO_API()
        # Find a location ID for a specific city/area, e.g., "FIPS:US06" for California
        # You might need to use get_locations() first to find relevant IDs
        # For demonstration, let's assume a known location ID for a weather station
        # You can search for stations here: https://www.ncei.noaa.gov/cdo-web/search
        # Example: GHCND:USW00014733 (NEW YORK CENTRAL PARK, NY US)
        location_id = "GHCND:USW00014733"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        print(f"Fetching daily summaries for {location_id} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        daily_data = noaa.get_daily_summaries(location_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        print("Daily Summaries (first 5 rows):")
        print(daily_data.head())
    except Exception as e:
        print(f"NOAA API Error: {e}")

    # NASA Earth API Example
    try:
        print("\n--- NASA Earth API Example ---")
        nasa = NASA_Earth_API()
        lon, lat = -100.0, 40.0 # Example coordinates (Kansas, USA)
        date = "2023-01-01"
        print(f"Getting Landsat asset for lon={lon}, lat={lat}, date={date}")
        asset_info = nasa.get_landsat_asset(lon, lat, date)
        print("Landsat Asset Info:")
        print(asset_info)

        print(f"Getting Landsat imagery URL for lon={lon}, lat={lat}, date={date}")
        imagery_url = nasa.get_landsat_imagery_url(lon, lat, date)
        print("Landsat Imagery URL:")
        print(imagery_url)
    except Exception as e:
        print(f"NASA API Error: {e}")

    # Copernicus CDS API Example (requires manual setup of .cdsapirc and cdsapi library)
    print("\n--- Copernicus CDS API Example ---")
    copernicus = Copernicus_CDS_API()
    print("To use Copernicus CDS API, you need to install 'cdsapi' library and configure your ~/.cdsapirc file.")
    print("Example code for retrieving ERA5 data:")
    print(copernicus.get_era5_data_example())


