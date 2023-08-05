# Skyworker Processor: {processor_name}

Template repository for the Skyworker AI Processor

## Requirements

- `Python >= 3.6`
- `pip`
- `venv (recommended)`

## Usage

- Clone this repository
- Update todos in [setup.py](setup.py) file
- Update todos in [skyworker_processor/\_\_init\_\_.py](skyworker_processor/__init__.py) file
- Define your logic in [skyworker_processor/core/processor.py](skyworker_processor/core/processor.py) module's `process` function

The return value of `skyworker_processor.process()` function should be the `pandas.DataFrame` object with following columns:

- `measurement` - Measurement Name
- `value` - Calculated Value

and the index of each row should be the unique timestamp.

### Example

```python
import pandas as pd
from datetime import datetime

time_series = [
    {
        "timestamp": 1628150400,
        "measurement": "Electricity Price",
        "value": 0.23,
    },
    {
        "timestamp": 1628236800,
        "measurement": "Electricity Price",
        "value": 0.25,
    }
]

data_frame = pd.DataFrame(time_series)
# Set "timestamp" column as index.
data_frame.index = data_frame["timestamp"]
# Compose "time" column from the "timestamp"
data_frame["time"] = data_frame["timestamp"].map(datetime.fromtimestamp)
del data_frame["timestamp"]
```

## Build & Publish

Build and Publish is a part of the CI/CD pipeline, but you can publish your package manually:

```shell
# Check the package.
$ python setup.py check

# Build the package.
$ python setup.py sdist

# Publish the package.
$ twine upload dist/*
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for details.

## Authors

- [Temuri Takalandze](https://abgeo.dev) - *Author and Maintainer*

## License

Copyright © 2021 [Omedia](https://omedia.dev).  
Released under the [Other/Proprietary License](LICENSE).
