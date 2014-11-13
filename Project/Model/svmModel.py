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
    newX = [0] * len(x)
    for i in range(len(x)):
      newX[i] = {}
      for j in x[i]:
        if j in self.featuresToIndex:
          newX[i][self.featuresToIndex[j]] = x[i][j]
    if options is None:
      return svm_predict(y, newX, self.model)
    else:
      return svm_predict(y, newX, self.model, options)

  def read(self, file):
    f = open(file, 'r')
    raw = json.loads(f.read())
    self.y = [0] * len(raw)
    x = [0] * len(raw)
    for i in range(len(raw)):
      self.y[i] = raw[i][1]
      x[i] = raw[i][0]
    self.featuresToIndex = {}
    self.indexToFeatures = {}
    count = 0
    self.x = [0] * len(raw)
    for i in range(len(x)):
      self.x[i] = {}
      for j in x[i]:
        if j not in self.featuresToIndex:
          self.featuresToIndex[j] = count
          self.indexToFeatures[count] = j
          count += 1
        self.x[i][self.featuresToIndex[j]] = x[i][j]

  def saveModel(self, file):
    svm_save_model(file, self.model)

  def loadModel(self, file):
    self.model = svm_load_model(file)

  def trainProb(self, y, x):
    self.train(y, x, '-b 1')

  def predictProb(self, y, x):
    self.predict(y, x, '-b 1')

  def crossValidation(self, k):
    return svm_train(self.y, self.x, '-v ' + str(k))

  def getX(self):
    return self.x
  
  def setX(self, x):
    self.x = x

  def setY(self, y):
    self.y = y

  def getY(self):
    return self.y

  def getModel(self):
    return self.model
