# ReAttempt

ReAttempt is a python decorator to retry a function when exceptions are raised.

### Demonstration:


```python

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

ReAttempt 

## Installation

```bash
# Install the dependency
pip install reattempt
uv add reattempt
poetry add reattempt
```

## Usage

```bash
from reattempt import reattempt

@reattempt
def hello_world():
    print("Hello World")

if __name__ == "__main__":
    hello_world()
```


## License

ReAttempt is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, suggestions, or issues related to ReAttempt, please open an issue on the GitHub repository.

