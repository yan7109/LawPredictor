from svmutil import *
import json

class svmModel:
  def __init__(self, y = None, x = None):
    self.y = y
    self.x = x
    self.model = None
  
  def train(self, options = None):
    if options is None:
      self.model = svm_train(self.y, self.x)
    else:
      self.model = svm_train(self.y, self.x, options)
  
  def predict(self, y, x, options = None):
    if options is None:
      return svm_predict(y, x, self.model)
    else:
      return svm_predict(y, x, self.model, options)

  def read(self, file):
    f = open(file, 'r')
    raw = json.loads(f.read())
    self.y = [0] * len(raw)
    slef.x = [0] * len(raw)
    for i in range(len(raw)):
      self.y[i] = raw[i][1]
      self.x[i] = raw[i][0]

  def saveModel(self, file):
    svm_save_model(file, self.model)

  def loadModel(self, file):
    self.model = svm_load_model(file)

  def trainProb(self, y, x):
    self.train(y, x, '-b 1')

  def predictProb(self, y, x):
    self.predict(y, x, '-b 1')

  def crossValidation(self):
    return svm_train(self.y, self.x, '-v')

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  def getModel(self):
    return self.model
