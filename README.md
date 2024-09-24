# ReAttempt

ReAttempt is a python decorator to retry a function when exceptions are raised.

### Demonstration:


```python
merge("text-gray-100 text-gray-50")
    -> "text-gray-50"
merge(clsx("text-gray-100", "text-gray-50")) 
    -> "text-gray-50"
```

## Table of Contents

- [TWindMerge](#TWindMerge)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [Contact](#contact)

## Description

TWindMerge provides a powerful solution for managing Tailwind CSS classes in dynamic environments. 
By keeping only the latest conflicting class, TWindMerge ensures that your styles are applied as intended, reducing unexpected visual outcomes and improving the maintainability of your codebase.


## Installation

```bash
# Install the dependency
npm install --save twindmerge

```

## Usage

```bash
# Import and call the merge function
import {merge} from 'twindmerge'
<div className={merge("bg-red-200 bg-green-200")}></div>
```


## License

TWindMerge is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, suggestions, or issues related to TWindMerge, please open an issue on the GitHub repository.

