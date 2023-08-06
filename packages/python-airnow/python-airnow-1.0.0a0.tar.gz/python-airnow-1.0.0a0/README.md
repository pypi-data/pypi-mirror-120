![PyPI](https://img.shields.io/pypi/v/python-airnow)
[![CI](https://github.com/ronnie-llamado/python-airnow/actions/workflows/ci.yaml/badge.svg)](https://github.com/ronnie-llamado/python-airnow/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/ronnie-llamado/python-airnow/branch/main/graph/badge.svg?token=KJZNDU1Z6Q)](https://codecov.io/gh/ronnie-llamado/python-airnow)
[![Documentation Status](https://readthedocs.org/projects/python-airnow/badge/?version=latest)](https://python-airnow.readthedocs.io/en/latest/?badge=latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/python-airnow)
# python-airnow
A wrapper around [AirNow API](https://docs.airnowapi.org/).

## Install

```
pip install -U python-airnow
```

## Example

```python
import airnow
import datetime

AIRNOW_API_KEY = '{INSERT_API_KEY}'
air = airnow.AirNow(AIRNOW_API_KEY)

obsrvtns = air.observation.by_zip_code(20002)
print(obsrvtns)
# [
#     AirNowObservation(
#         date_time=datetime.datetime(2021, 9, 7, 12, 0, tzinfo=tzoffset('EST', -18000)),
#         reporting_area='Metropolitan Washington',
#         parameter_name='O3',
#         aqi=46
#     ),
#     AirNowObservation(
#         date_time=datetime.datetime(2021, 9, 7, 12, 0, tzinfo=tzoffset('EST', -18000)),
#         reporting_area='Metropolitan Washington',
#         parameter_name='PM2.5',
#         aqi=4
#     )
# ]

frcst = air.forecast.by_lat_long(38.919, -77.013, date=datetime.datetime(2021,9,7))
print(frcst)
# [
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 7),
#       reporting_area='Metropolitan Washington',
#       parameter_name='O3',
#       aqi=61
#     ),
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 7),
#       reporting_area='Metropolitan Washington',
#       parameter_name='PM2.5',
#       aqi=38),
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 8),
#       reporting_area='Metropolitan Washington',
#       parameter_name='O3',
#       aqi=50
#     ),
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 8),
#       reporting_area='Metropolitan Washington',
#       parameter_name='PM2.5',
#       aqi=46
#     ),
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 9),
#       reporting_area='Metropolitan Washington',
#       parameter_name='O3',
#       aqi=46
#     ),
#     AirNowForecast(
#       date_forecast=datetime.date(2021, 9, 9),
#       reporting_area='Metropolitan Washington',
#       parameter_name='PM2.5',
#       aqi=33
#     )
# ]

```

## Links
- Documentation: https://python-airnow.readthedocs.io/
- PyPI Releases: https://pypi.org/project/python-airnow/
- Source Code: https://github.com/ronnie-llamado/python-airnow/
- Issue Tracker: https://github.com/ronnie-llamado/python-airnow/issues/
- AirNow API Documentation: https://docs.airnowapi.org
