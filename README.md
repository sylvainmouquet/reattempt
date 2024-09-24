# ReAttempt

ReAttempt is a python decorator to retry a function when exceptions are raised.

### Demonstration:

```python
import reattempt

@reattempt(max_retries=5, min_time=0.1, max_time=2)
def wrong_function():
  raise Exception("failure")

if __name__ == "__main__":
    wrong_function()

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

```bash
import reattempt

@reattempt
def hello_world():
  print("Hello World")
  raise Exception("failure")

if __name__ == "__main__":
    hello_world()
```


## License

ReAttempt is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, suggestions, or issues related to ReAttempt, please open an issue on the GitHub repository.

