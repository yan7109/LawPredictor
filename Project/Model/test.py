from svmModel import *

a = svmModel()
a.read('features')
print a.crossValidation(10)
