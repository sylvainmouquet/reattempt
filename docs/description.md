# Description

ReAttempt is a Python library that provides a decorator to automatically retry a function when exceptions are raised. It uses an exponential backoff strategy to wait between retries, ensuring that the function has multiple chances to succeed before ultimately failing.

## Features

- **Synchronous and Asynchronous Support**: ReAttempt supports both synchronous and asynchronous functions, making it versatile for various use cases.
- **Exponential Backoff**: The library uses an exponential backoff strategy to wait between retries, which helps in managing the load on the system and avoiding immediate repeated failures.
- **Customizable Retry Logic**: You can customize the number of retries, minimum and maximum wait times, and other parameters to suit your needs.

## Example Usage

### Synchronous Function Example

```python
from reattempt import reattempt
import random

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
def plant_flower():
    flower = random.choice(flowers)
    print(f"Attempting to plant a {flower}")
    if random.random() < 0.8:  # 80% chance of failure
        raise Exception(f"The {flower} didn't take root")
    return f"{flower} planted successfully"
```

### Asynchronous Function Example

```python
from reattempt import reattempt
import asyncio
import random

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
async def water_flower():
    flower = random.choice(flowers)
    print(f"Watering the {flower}")
    await asyncio.sleep(0.1)  # Simulating watering time
    if random.random() < 0.6:  # 60% chance of failure
        raise Exception(f"The {flower} needs more water")
    return f"{flower} is well-watered"
```

For more detailed examples and usage, please refer to the [Usage](usage.md) section.