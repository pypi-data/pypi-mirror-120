from oneNeuron.Perceptron import Perceptron

import numpy as np
import pandas as pd 
import os
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from matplotlib.colors import ListedColormap
import joblib
import logging 


def prepare_data(df):

  logging.info("Preparing the data by segregating depemdent and dependent model")  

  x = df.drop("y", axis = 1)
  y = df["y"]
  return(x,y)



## Definining Save_model function 
def save_model (model,filename):
  """this save the trained model to

  Args:
      model (python object): trained model
      filename (str): path to save the trained model
  """
  logging.info("Saving the trained model")
    
  model_dir  = 'model'
  os.makedirs(model_dir,exist_ok=True) ## ONLY CREATE IF THE MODEL_DIR DOES NOT EXISTS
  filePath = os.path.join(model_dir,filename)## Model filename
  joblib.dump(model,filePath)
  logging.info(f"saved the trained model{filePath}")




 
## Defining save_plot
def save_plot(df, file_name, model):

  def _create_base_plot(df):
    logging.info("CreateBasePlot")
    df.plot(kind="scatter", x="x1", y="x2", c="y", s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)

  def _plot_decision_regions(X, y, classfier, resolution=0.02):
    logging.info("Plotting decision regions")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    X = X.values # as a array
    x1 = X[:, 0] 
    x2 = X[:, 1]
    x1_min, x1_max = x1.min() -1 , x1.max() + 1
    x2_min, x2_max = x2.min() -1 , x2.max() + 1  

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                           np.arange(x2_min, x2_max, resolution))
   
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
  logging.info(f"Saving plot at {plotPath}") 



