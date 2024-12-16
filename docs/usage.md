# Usage

## Synchronous Function Example

```python exec="on" source="above"
from reattempt import reattempt
import random
from pprint import pprint

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
def plant_flower():
    flower = random.choice(flowers)
    print(f"Attempting to plant a {flower}")
    if random.random() < 0.8:  # 80% chance of failure
        raise Exception(f"The {flower} didn't take root")
    return f"{flower} planted successfully"

# Example output
try:
    result = plant_flower()
    pprint(result)
except Exception as e:
    pprint(f"Planting error: {e}")
```

## Synchronous Generator Example

```python exec="on" source="above"
from reattempt import reattempt
import random
from pprint import pprint

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
def grow_flowers():
    for _ in range(3):
        flower = random.choice(flowers)
        print(f"Growing {flower}")
        yield flower
    if random.random() < 0.5:  # 50% chance of failure at the end
        raise Exception("The garden needs more fertilizer")

# Example output
try:
    for flower in grow_flowers():
        pprint(f"Grown: {flower}")
except Exception as e:
    pprint(f"Growing error: {e}")
```

## Asynchronous Function Example

```python exec="on" source="above"
from reattempt import reattempt
import asyncio
import random
from pprint import pprint

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
async def water_flower():
    flower = random.choice(flowers)
    print(f"Watering the {flower}")
    await asyncio.sleep(0.1)  # Simulating watering time
    if random.random() < 0.6:  # 60% chance of failure
        raise Exception(f"The {flower} needs more water")
    return f"{flower} is well-watered"

# Example output
async def example_water_flower():
    try:
        result = await water_flower()
        pprint(result)
    except Exception as e:
        pprint(f"Watering error: {e}")

asyncio.run(example_water_flower())
```

## Asynchronous Generator Function Example

```python exec="on" source="above"
from reattempt import reattempt
import asyncio
import random
from pprint import pprint

flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]

@reattempt
async def harvest_flowers():
    for _ in range(3):
        flower = random.choice(flowers)
        print(f"Harvesting {flower}")
        yield flower
        await asyncio.sleep(0.1)  # Time between harvests
    if random.random() < 0.4:  # 40% chance of failure at the end
        raise Exception("The garden needs more care")

# Example output
async def example_harvest_flowers():
    try:
        async for flower in harvest_flowers():
            pprint(f"Harvested: {flower}")
    except Exception as e:
        pprint(f"Harvesting error: {e}")

asyncio.run(example_harvest_flowers())
```

## Complete Example

```python exec="on" source="above"
import asyncio
from pprint import pprint

async def tend_garden():
    # Plant a flower (sync function)
    try:
        result = plant_flower()
        pprint(result)
    except Exception as e:
        pprint(f"Planting error: {e}")

    # Grow flowers (sync generator)
    try:
        for flower in grow_flowers():
            pprint(f"Grown: {flower}")
    except Exception as e:
        pprint(f"Growing error: {e}")

    # Water a flower (async function)
    try:
        result = await water_flower()
        pprint(result)
    except Exception as e:
        pprint(f"Watering error: {e}")

    # Harvest flowers (async generator function)
    try:
        async for flower in harvest_flowers():
            pprint(f"Harvested: {flower}")
    except Exception as e:
        pprint(f"Harvesting error: {e}")

if __name__ == "__main__":
    asyncio.run(tend_garden())

# Example output
asyncio.run(tend_garden())
```