import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib
from matplotlib.colors import ListedColormap
import os
import logging

plt.style.use('fivethirtyeight')

def prepare_data(df):
  """Used to sepearate the depedent variables and independent features

  Args:
      df (pd.DataFrame): Pandas DataFrame

  Returns:
      tuple: Returns tuples of dependent and independent variables
  """
  logging.info("Preparing the data by segregating the indepedent and dependent variables")
  X = df.drop("y", axis=1)

  y = df["y"]

  return X, y

def save_model(model, filename):
  """This saves the trained model

  Args:
      model (python object): trained model
      filename (str): path to save the model
  """
  logging.info("saving the trained model")
  model_dir = 'models'
  os.makedirs(model_dir, exist_ok = True) #ONLY CREATE IF MODEL_DIR does not exist
  filePath = os.path.join(model_dir, filename) # model/filename
  logging.info(f'model saved at {filePath}')
  joblib.dump(model,filePath)

def save_plot(df, file_name, model):
  def _create_base_plot(df):
    logging.info(f"creating the base plot")
    df.plot(kind="scatter",x="x1", y="x2",c='y',s=100, cmap='winter')
    plt.axhline(y=0,color='black',linestyle="--",linewidth=1)
    plt.axvline(x=0,color='black',linestyle="--",linewidth=1)
    figure = plt.gcf() #get current figure
    figure.set_size_inches(10,8)

  def _plot_decision_regions(X,y, classifier, resolution=0.02):
    logging.info(f"plitting the decision regions")
    colors = ("red","blue","lightgreen","gray","cyan")
    cmap = ListedColormap(colors[:len(np.unique(y))])

    X = X.values #need as an array instead of a dataframe
    x1_min, x1_max = X[:, 0].min() -1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() -1, X[:, 1].max() + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                          np.arange(x2_min, x2_max, resolution))
    # print(xx1, xx2)
    # print(xx1.ravel(),xx2.ravel())
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    # print(Z)
    Z = Z.reshape(xx1.shape)
    # print(Z)
    plt.contourf(xx1,xx2,Z,alpha=0.2, cmap = cmap)
    plt.xlim(xx1.min(),xx1.max())
    plt.ylim(xx2.min(),xx2.max())

    plt.plot()

  X, y = prepare_data(df)

  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  plotPath = os.path.join(plot_dir, file_name) # model/filename
  plt.savefig(plotPath)
  logging.info(f"saved the plot at {plotPath}")