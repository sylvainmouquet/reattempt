import pytest
from reattempt import reattempt
import asyncio
import random
import logging

# List of flowers for our examples
flowers = ["Rose", "Tulip", "Sunflower", "Daisy", "Lily"]


# Synchronous function example
@reattempt
def plant_flower():
    flower = random.choice(flowers)
    logging.info(f"Attempting to plant a {flower}")
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
    logging.info(f"Watering the {flower}")
    await asyncio.sleep(0.1)  # Simulating watering time
    if random.random() < 0.6:  # 60% chance of failure
        raise Exception(f"The {flower} needs more water")
    return f"{flower} is well-watered"


# Asynchronous generator function example
@reattempt
async def harvest_flowers():
    for _ in range(3):
        flower = random.choice(flowers)
        logging.info(f"Harvesting {flower}")
        yield flower
        await asyncio.sleep(0.1)  # Time between harvests
    if random.random() < 0.4:  # 40% chance of failure at the end
        raise Exception("The garden needs more care")


@pytest.mark.asyncio
async def test_tend_garden(disable_logging_exception):
    # Plant a flower (sync function)
    try:
        result = plant_flower()
        logging.info(result)
    except Exception as e:
        logging.info(f"Planting error: {e}")

    # Grow flowers (sync generator)
    try:
        for flower in grow_flowers():
            print(f"Grown: {flower}")
    except Exception as e:
        print(f"Growing error: {e}")

    # Water a flower (async function)
    try:
        result = await water_flower()
        logging.info(result)
    except Exception as e:
        logging.info(f"Watering error: {e}")

    # Harvest flowers (async generator function)
    try:
        async for flower in harvest_flowers():
            logging.info(f"Harvested: {flower}")
    except Exception as e:
        logging.info(f"Harvesting error: {e}")
