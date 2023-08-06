import  numpy as np
import logging
from tqdm import tqdm


class Perceptron:
  def __init__(self,eta,epochs):
    self.weights = np.random.randn(3)*1e-4
    logging.info(f"intial weight before training:\n {self.weights}")
    self.eta = eta # eta learning rate
    self.epochs = epochs

  def activationfunction(self,input,weights):
    z = np.dot(input,weights)
    return np.where(z>0,1,0)
  
  def fit(self,x,y):
    self.x = x
    self.y = y
    Weights_all = []


    x_with_bias = np.c_[self.x,-np.ones((len(self.x),1))]
    logging.info(f"X with bias:\n {x_with_bias}")

    for epoch in tqdm(range(self.epochs),total=self.epochs,desc='training the model'):
      logging.info(f"for epoch:\t {epoch}")
      logging.info("--"*10)
      Weights_all.append(self.weights)
      y_hat = self.activationfunction(x_with_bias,self.weights)# foraward propagation
      logging.info(f"Predicted value after forward pass:\n{y_hat}")

      self.error = self.y-y_hat
      # logging.info(f"error:\n{self.error}")
      logging.info(f"Total loss is {np.sum(self.error)}")
      if np.sum(self.error) ==0:
        
        break


      self.weights = self.weights + self.eta*np.dot(x_with_bias.T,self.error)# backward propagation
      logging.info(f"updated weights after epoch:\n {epoch}/{self.epochs} :\n {self.weights} ")
      logging.info("===="*30)
    # logging.info(Weights_all)

  
  def predict(self,x):
    x_with_bias = np.c_[x,-np.ones((len(x),1))]
    return self.activationfunction(x_with_bias,self.weights)
  def total_loss(self):
    toatal_loss = np.sum(self.error)
    logging.info(f"total loss: {toatal_loss}")
    return toatal_loss