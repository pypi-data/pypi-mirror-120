import numpy as np
import logging
from tqdm import tqdm

class ActivationFunction:
    def __init__(self, fn, alpha = None):
        self.fn = fn
        self.alpha = alpha
        
    def step(self, x):
        return np.where(x >= 0, 1, 0)
    
    def signum(self, x):
        return -1 if x < 0 else 0 if x == 0 else 1
    
    def linear(self, x):
        return x
    
    def ReLU(self, x):
        return max(0.0, x)
    
    def sigmoid(self, x):
        return 1/(1 + np.exp(x))
    
    def tan_h(self, x):
        return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))
    
    def ELU(self, x, alpha = 1):
        return x if x >= 0 else alpha*(np.exp(x) - 1)
    
    def GELU(self, x):
        return 0.5*x*(1 + np.tanh((7/11)**.5 * (x + (0.044715 * x**3))))
    
    def swish(self, x):
        return  x/(1 + np.exp(-x))
    
    def call(self):
        funcs = [self.step, self.signum, self.linear, self.ReLU, self.sigmoid, self.tan_h, self.ELU, self.GELU, self.swish]
        func_str = ['step', 'signum', 'linear', 'relu', 'sigmoid', 'tanh', 'elu', 'gelu', 'swish']
        func_dict = dict(zip(func_str, funcs))
        return func_dict[self.fn]

class Perceptron:
  def __init__(self, eta, epochs):
    self.weights = np.random.randn(3) * 1e-4 # SMALL WEIGHT INIT
    logging.info(f"initial weights before training: \n{self.weights}")
    self.eta = eta # LEARNING RATE
    self.epochs = epochs 

  def activationFunction(self, inputs, weights, fnxn, alpha):
    z = np.dot(inputs, weights) # Z = W.X [Matrix Dot products]
    fn = ActivationFunction(fnxn).call()
    vf = np.vectorize(fn)
    outputs = vf(z) if fnxn != 'elu' else vf( z, alpha)
    return outputs

  def fit(self, X, y, fn, alpha):
    self.X = X
    self.y = y
    self.funxn = fn
    self.alpha = alpha

    X_bias = np.c_[self.X, -np.ones((len(self.X), 1))] # CONCATINATION
    logging.info(f"X with bias: \n{X_bias}")

    for epoch in tqdm(range(self.epochs), total=self.epochs, desc='Training the model'):
      logging.info("--"*10)
      logging.info(f"for epoch: {epoch}")
      logging.info("--"*10)

      y_hat = self.activationFunction(X_bias, self.weights, self.funxn, self.alpha) # foward propagation
      logging.info(f"predicted value after forward pass: \n{y_hat}")
      self.error = self.y - y_hat
      logging.info(f"error: \n{self.error}")
      self.weights = self.weights + self.eta * np.dot(X_bias.T, self.error) # backward propagation
      logging.info(f"updated weights after epoch:\n{epoch}/{self.epochs} : \n{self.weights}")
      logging.info("#####"*10)


  def predict(self, X):
    X_with_bias = np.c_[X, -np.ones((len(X), 1))]
    return self.activationFunction(X_with_bias, self.weights, self.funxn, self.alpha)

  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"total loss: {total_loss}")
    return total_loss