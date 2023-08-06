# Perceptron
**Single Layer Perceptron(one Neuron)**  
A Perceptron is a simple model of a biological neuron that classifies the label of the input data based on various activation functions:
1. Binary Step Function
2. Signum Function
3. Linear Activation Function
4. Sigmoid / Logistic Activation Function
5. Tanh Function (Hyperbolic Tangent)
6. ReLU Function
7. Exponential Linear Units (ELUs) Function
8. Swish
9. Gaussian Error Linear Unit (GELU)

```python
fn_list = ['step', 'signum', 'linear', 'relu', 'sigmoid', 'tanh', 'elu', 'gelu', 'swish']
```

## How to use this
```python
from Perceptron.perceptron import Perceptron
from Perceptron.utils import prepare_data, save_plot, save_model

# get the data, convert it into a DataFrame and then use below commands
X, y = prepare_data(df)

model = Perceptron(eta = eta, epochs = epochs)
model.fit(X, y, fn, alpha=None) # alpha ranges between 0 to 1 if and only if ELU activation function is applied else alpha value remains None for other activation functions

Total_Error = model.total_loss()

save_model(model, filename = filename)

save_plot(df, plotFilename, model)
```

## Reference
[Python Package Publishing Docs](https://packaging.python.org/tutorials/packaging-projects/)

[GitHub Actions CICD Docs](https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries)