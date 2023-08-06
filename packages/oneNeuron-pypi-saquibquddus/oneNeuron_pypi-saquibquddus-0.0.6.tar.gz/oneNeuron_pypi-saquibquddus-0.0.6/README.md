# oneNeuron_pypi
oneNeuron_pypi

## Reference -
[Python package docs](https://packaging.python.org/tutorials/packaging-projects/)

[Github doc for gihub actions](https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries)

## How to use
```python
from oneNeuron.perceptron import Perceptron

## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```

