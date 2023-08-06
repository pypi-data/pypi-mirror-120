

```python
from parallely import threaded
import requests

@threaded
def fetch(min_val=100, max_val=1000, count=5):
    return requests.get(f"http://www.randomnumberapi.com/api/v1.0/random?min={min_val}&max={max_val}&count={count}").json()

fetch.map(count=list(range(10)))
```