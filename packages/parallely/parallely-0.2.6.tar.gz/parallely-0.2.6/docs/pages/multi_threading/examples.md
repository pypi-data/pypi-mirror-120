```python
from parallely import threaded
import requests

@threaded(max_workers=500)
def fetch_data(url):
    return requests.get(url).json()

# Use the function as usual for fine grained control, testing etc. 
fetch_data("http://www.SOME-WEBSITE.com/data/cool-stuff")

# Use a thread-pool to map over a list of inputs in concurrent manner
fetch_data.map([
    "http://www.SOME-WEBSITE.com/data/cool-stuff",
    "http://www.SOME-WEBSITE.com/data/cool-stuff",
    "http://www.SOME-WEBSITE.com/data/cool-stuff"
])
```

```python
from parallely import threaded
import requests

@threaded
def fetch(min_val=100, max_val=1000, count=5):
    return requests.get(f"http://www.randomnumberapi.com/api/v1.0/random?min={min_val}&max={max_val}&count={count}").json()

fetch.map(count=list(range(10)))
```