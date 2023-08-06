import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import joblib # for saving my model as a binar file
from matplotlib.colors import ListedColormap
import os
import logging




def prepare_data(df):
  """It is used seprate features and labels for

  Args:
      df (pd Dataframe): its the pandas Dataframe

  Returns:
      tuple: it returns the tuple of the dependent variable and indepedent variable

  """
  logging.info("preparing the data by sergerts the indepedent variable ")
  x = df.drop('y',axis=1)
  y = df["y"]
  return x,y

def save_Model(model,filename):
  """This save the trainedn model to

  Args:
      model (pyton object): trained model
      filename (str): path  to save the trained model
      filename
  """
  logging.info("saving the trianed model")
  modle = "model"
  os.makedirs(modle,exist_ok=True) # if the model dir then it not create dir
  path = os.path.join('model',filename)
  
  joblib.dump(model,path)
  logging.info(f"the saving the file at {path}")
def save_plot(df, file_name, model):
  """It is save the plot  file

  Args:
      df (pandas DataFrame): It take the pd file 
      file_name (str): it saved the plot file
      model : it is the traiened model
  """
  def _create_base_plot(df):
    logging.info('creating the base plot')
    df.plot(kind="scatter", x="x1", y="x2", c="y", s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)

  def _plot_decision_regions(X, y, classfier, resolution=0.02):
    logging.info('ploting the decision  boundary')
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    X = X.values # as a array
    x1 = X[:, 0] 
    x2 = X[:, 1]
    x1_min, x1_max = x1.min() -1 , x1.max() + 1
    x2_min, x2_max = x2.min() -1 , x2.max() + 1  
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                       np.arange(x2_min, x2_max, resolution))
    # print(xx1)
    # print(xx1.ravel())
    Z = classfier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    plt.plot()



  X, y = prepare_data(df)

  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  plotPath = os.path.join(plot_dir, file_name) # model/filename
  plt.savefig(plotPath)
  logging.info(f"saving  in the {plotPath}")