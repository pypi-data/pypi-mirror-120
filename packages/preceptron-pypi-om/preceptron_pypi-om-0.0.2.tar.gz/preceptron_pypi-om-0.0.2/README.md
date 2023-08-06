# preceptron_pypi
preceptron_pypi

## How to use this

```python
from synapses.perceptron import Perceptron

## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```