# Setup

## Requirements
Before installing openstix, ensure that you meet the following requirements:

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment recommended (virtualenv, venv, hatch, etc.)

## Installation
### Step 1: Create a Virtual Environment (Optional but Recommended)
It is recommended to create a virtual environment to avoid conflicts with other libraries and ensure a clean setup.

```
python -m venv env
source env/bin/activate  # For Linux/MacOS
env\Scripts\activate  # For Windows
```

### Step 2: Install openstix
Install the openstix library using pip:

```
pip install openstix
```

## Development Environment Setup
If you intend to contribute to the development of openstix, follow the steps below to set up your development environment:

### Step 1: Clone the Repository
Clone the GitHub repository:

```
git clone https://github.com/AbuseTotal/openstix-python.git
cd openstix-python
```

### Step 2: Install Development Dependencies
Ensure you have all the necessary dependencies to develop and test the library.

1. Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate  # For Linux/MacOS
env\Scripts\activate  # For Windows
```

2. Install the development dependencies:
```
pip install -r requirements-dev.txt
```

## Common Issues and Solutions
### Issue: pip is not installed
If you encounter the error `pip: command not found`, pip may not be installed or configured correctly on your system. Refer to the [official pip documentation](https://pip.pypa.io/en/stable/installation/) for installation instructions.

### Issue: Dependency Conflicts
If you encounter dependency conflict issues, consider using a virtual environment to isolate `openstix` dependencies from those of other projects.
