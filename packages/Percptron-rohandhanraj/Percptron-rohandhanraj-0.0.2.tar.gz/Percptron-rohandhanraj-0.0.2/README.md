# Perceptron
**Single Layer Perceptron(one Neuron)**  
A Perceptron is a simple model of a biological neuron that classifies the label of the input data based on various activation functions:
1. Binary Step Function: 
\begin{equation}
  f(x)=\begin{cases}
    0, & \text{if $x<0$}.\\
    1, & \text{otherwise}.
  \end{cases}
\end{equation}
![Binary Step Function](Activation_Function_Plots\step.png)

2. Signum Function:
\begin{equation}
  f(x)=\begin{cases}
    -1, & \text{if $x<0$}.\\
    0, & \text{if $x=0$>}\\
    1, & \text{if $x>0$}.
  \end{cases}
\end{equation}
![Signum Function](Activation_Function_Plots\signum.png)

3. Linear Activation Function:
$$f(x) = x$$
![Linear Activation Function](Activation_Function_Plots\linear.png)

4. Sigmoid / Logistic Activation Function:
$$f(x) = \frac{1}{1+e^{-x}}$$
![Sigmoid / Logistic Activation Function](Activation_Function_Plots\sigmoid.png)

5. Tanh Function (Hyperbolic Tangent):
$$f(x) = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}$$
![Tanh Function (Hyperbolic Tangent)](Activation_Function_Plots\tanh.png)

6. ReLU Function:
$$f(x) = max(0, x)$$
![ReLU Function](Activation_Function_Plots\ReLU.png)

7. Exponential Linear Units (ELUs) Function:
\begin{equation}
  f(x)=\begin{cases}
    x, & \text{if $x\geqslant0$}.\\
    \alpha(e^{x} - 1), & \text{otherwise}.
  \end{cases}
\end{equation}
![Exponential Linear Units (ELUs) Function](Activation_Function_Plots\ELU.png)

8. Swish:
$$f(x) = \frac{x}{1 + e^{-x}}$$
![Swish](Activation_Function_Plots\swish.png)

9. Gaussian Error Linear Unit (GELU):
$$f(x) = 0.5x(1 + tanh[\sqrt{2/\pi}(x + 0.044715x^3)])$$
![Gaussian Error Linear Unit (GELU)](Activation_Function_Plots\GELU.png)


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