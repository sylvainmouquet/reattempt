# ReAttempt

ReAttempt is a python decorator to retry a function when exceptions are raised.

### Demonstration:

```python
from reattempt import reattempt

@reattempt(max_retries=5, min_time=0.1, max_time=2)
def simulate_network_failure():
    raise Exception("Connection timeout")

if __name__ == "__main__":
    simulate_network_failure()

------------------------------------------------------- live log call -------------------------------------------------------
WARNING  root:__init__.py:167 [RETRY] Attempt 1/5 failed, retrying in 0.17 seconds...
WARNING  root:__init__.py:167 [RETRY] Attempt 2/5 failed, retrying in 0.19 seconds...
WARNING  root:__init__.py:167 [RETRY] Attempt 3/5 failed, retrying in 0.19 seconds...
WARNING  root:__init__.py:167 [RETRY] Attempt 4/5 failed, retrying in 0.19 seconds...
WARNING  root:__init__.py:163 [RETRY] Attempt 5/5 failed, stopping
ERROR    root:__init__.py:177 [RETRY] Max retries reached
```

## Table of Contents

- [ReAttempt](#ReAttempt)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [Contact](#contact)

## Description

ReAttempt is a Python library that provides a decorator to automatically retry a function when exceptions are raised. It uses an exponential backoff strategy to wait between retries, ensuring that the function has multiple chances to succeed before ultimately failing.

## Installation

```bash
# Install the dependency
pip install reattempt
uv add reattempt
poetry add reattempt
```

## Usage

```python
from reattempt import reattempt
import asyncio
import random

# List of flowers for our examples
flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

# Synchronous function example
@reattempt
def plant_flower():
    flower = random.choice(flowers)
    print(f"Attempting to plant a {flower}")
    if random.random() < 0.8:  # 80% chance of failure
        raise Exception(f"The {flower} didn't take root")
    return f"{flower} planted successfully"

# Synchronous generator example
@reattempt
def grow_flowers():
    for _ in range(3):
        flower = random.choice(flowers)
        print(f"Growing {flower}")
        yield flower
    if random.random() < 0.5:  # 50% chance of failure at the end
        raise Exception("The garden needs more fertilizer")

# Asynchronous function example
@reattempt
async def water_flower():
    flower = random.choice(flowers)
    print(f"Watering the {flower}")
    await asyncio.sleep(0.1)  # Simulating watering time
    if random.random() < 0.6:  # 60% chance of failure
        raise Exception(f"The {flower} needs more water")
    return f"{flower} is well-watered"

# Asynchronous generator function example
@reattempt
async def harvest_flowers():
    for _ in range(3):
        flower = random.choice(flowers)
        print(f"Harvesting {flower}")
        yield flower
        await asyncio.sleep(0.1)  # Time between harvests
    if random.random() < 0.4:  # 40% chance of failure at the end
        raise Exception("The garden needs more care")

async def tend_garden():
    # Plant a flower (sync function)
    try:
        result = plant_flower()
        print(result)
    except Exception as e:
        print(f"Planting error: {e}")

    # Grow flowers (sync generator)
    try:
        for flower in grow_flowers():
            print(f"Grown: {flower}")
    except Exception as e:
        print(f"Growing error: {e}")

    # Water a flower (async function)
    try:
        result = await water_flower()
        print(result)
    except Exception as e:
        print(f"Watering error: {e}")

    # Harvest flowers (async generator function)
    try:
        async for flower in harvest_flowers():
            print(f"Harvested: {flower}")
    except Exception as e:
        print(f"Harvesting error: {e}")

if __name__ == "__main__":
    asyncio.run(tend_garden())
```


## License

ReAttempt is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, suggestions, or issues related to ReAttempt, please open an issue on the GitHub repository.

