# geojson_transformer

A python library for transforming GPX data to GeoJSON format.
It also gives you the ability to extract data from the gpx file such as:
Total elevation, total distance, starting point, paired data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install geojson_transformer.

```bash
pip install geojson_transformer
```

## Usage

```python
from geojson_transformer import GeoJsonTransformer

# Create an object from a gpx file.
gpxfile = GeoJsonTransformer(path='path/to/my_gpx_file.gpx') 

# Returns the total distance between each point in the gpx file.
gpxfile.total_distance

# Returns the total cumulative elevation between each point in the gpx file.
gpxfile.total_elevation

# Returns the first lat/lon pair found in the file.
gpxfile.starting_point
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)