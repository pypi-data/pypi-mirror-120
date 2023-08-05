## Note

Currently, this package is only configured to work in Axle's Jupyter deployment due to the choice of API paths.

## Usage

Create client object first
```py
from wipp_client.wipp import Wipp
w = Wipp()
```

Then choose the action you would like to make, i.e.
```py
w.get_image_collections()
```