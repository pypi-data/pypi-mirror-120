# backend-module

Main backend module, which is used for developing web-app logic and deploying AI model.

## Installation
Run the following to install:
```python
pip install anscenter
```

## Usage
```python
from anscester.predict import MachineLearningModel

# Generate model
model = MachineLearningModel()

# Using Example
data_input = [1.0, 2.0, 3.0, 4.0]
result = model.predict(data_input)
print(result)
```

## Developing HelloG
To install helloG, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install anscenter[dev]
```