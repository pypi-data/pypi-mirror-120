# Change log for Bamboo API Client
All notable changes to this project will be documented in this file.

## 1.5.0 - 2021-09-17
- Renamed `SitesApi.list_zones` to `SitesApi.list_thermal_zones`
- Renamed `SitesApi.get_zone` to `SitesApi.get_thermal_zone`
- Renamed `SitesApi.read_measurements` to `SitesApi.read_device_measurements`
- Renamed `SitesApi.update_measurements` to `SitesApi.update_device_measurements`
- Renamed `SitesApi.read_forecasts` to `SitesApi.read_device_baseline_forecasts`
- Renamed `SitesApi.update_forecasts` to `SitesApi.update_device_baseline_forecasts`
- Renamed `SitesApi.read_activations` to `SitesApi.read_device_activations`
- Renamed `SitesApi.read_baseline_model` to `SitesApi.read_device_baseline_model`
- Renamed `SitesApi.update_baseline_model` to `SitesApi.update_device_baseline_model`
- Renamed `SitesApi.read_flexibility_model` to `SitesApi.read_thermal_flexibility_model`
- Renamed `SitesApi.update_flexibility_model` to `SitesApi.update_thermal_flexibility_model`
- Updated `SitesApi.update_device_flexibility_forecast` to accept a DataFrame
- Added read&update flexibility forecast endpoints in `SitesApi` for devices and thermal zones ([BMVP-447](https://bambooenergy.atlassian.net/browse/BMVP-447))

## 1.4.1 - 2021-09-08
- Added `Tariffs` CRUD endpoints ([BMVP-403](https://bambooenergy.atlassian.net/browse/BMVP-403), [BMVP-413](https://bambooenergy.atlassian.net/browse/BMVP-413))
- Added endpoints to store & retrieve flexibility model parameters ([BMVP-323](https://bambooenergy.atlassian.net/browse/BMVP-323))
- Split `DataPoint` model into `SitesDataPoint` and `WeatherDataPoint` models ([BMVP-424](https://bambooenergy.atlassian.net/browse/BMVP-424))
- Added missing fields to `WeatherDataPoint` schema: `dewpoint`, `humidity`, `pressure` and `wind_speed` ([BMVP-391](https://bambooenergy.atlassian.net/browse/BMVP-391))

## 1.3.0 - 2021-08-11
- Added `elevation` to Site & Weather Station schemas ([BMVP-397](https://bambooenergy.atlassian.net/browse/BMVP-397))
- Added type hinting to all public methods ([BMVP-396](https://bambooenergy.atlassian.net/browse/BMVP-396))

## 1.2.1 - 2021-08-05
- Added Mock API client for testing with factories ([BMVP-359](https://bambooenergy.atlassian.net/browse/BMVP-359))

## 1.2.0 - 2021-07-27
- News fields in Sites schema: `country_code`, `timezone`, `latitude` & `longitude` ([BMVP-249](https://bambooenergy.atlassian.net/browse/BMVP-249), [BMVP-271](https://bambooenergy.atlassian.net/browse/BMVP-271))
- Modified `list_sites` to return a simpler schema ([BMVP-302](https://bambooenergy.atlassian.net/browse/BMVP-302))
- Renamed all `asset_name` arguments to `device_name` ([BMVP-380](https://bambooenergy.atlassian.net/browse/BMVP-380))
- Added input data validation rules for all data models ([BMVP-379](https://bambooenergy.atlassian.net/browse/BMVP-379))
- Added all variables in [mapping format](https://bambooenergy.atlassian.net/wiki/spaces/BMD/pages/175472655/Mapping+Format) to DataPoint schema ([BMVP-346](https://bambooenergy.atlassian.net/browse/BMVP-346))
- Updated battery schema, removing the redundant `max_power` and `min_power` variables ([BMVP-362](https://bambooenergy.atlassian.net/browse/BMVP-362))
- **BUGFIX**: Decreased min length for device names to 2 characters ([BMVP-365](https://bambooenergy.atlassian.net/browse/BMVP-365))

## 1.1.5 - 2021-06-22
- Modify setup and requirements to make package compatible with Python 3.5 and up
- Update requirements in README and add dynamic version badges

## 1.1.3 - 2021-06-11
- Restrict exception catching to "NotFoundException" (HTTP 404) in get methods

## 1.1.2 - 2021-06-11
- Updated client based con v1.1.2 of openapi definition for Bamboo API

## 1.1.1 - 2021-06-04
- Updated README with usage instructions

## 1.1.0 - 2021-06-03
- Updated client based con latest openapi definition for Bamboo API
- Renamed `find` method to `get`: `find_site` becomes `get_site`, etc...
- In GET methods, catch `NotFound` API errors (HTTP 404) and return None instead of raising an error
- Added `get_site_id_by_name` method to obtain site ID given a site name
- Added `get_station_id_by_name` method to obtain weather station ID given a station name
- Renamed `read_load_model` to `read_baseline_model` and `update_load_model` to `update_baseline_model`
- Added missing `horizon` parameter in `update_forecasts` method

## 1.0.0 - 2021-05-27
- Initial release
