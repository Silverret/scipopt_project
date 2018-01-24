#/usr/bin/env pypy

from pyscipopt import Model

model = Model("Manhattan")

x1 = model.addVar("x1", "B")
x2 = model.addVar("x2", "B")
x3 = model.addVar("x3", "B")
x4 = model.addVar("x4", "B")
x5 = model.addVar("x5", "B")
x6 = model.addVar("x6", "B")

model.addCons(x1 + x4 >= 1)
model.addCons(x1 + x2 >= 1)
model.addCons(x6 + x4 >= 1)
model.addCons(x6 + x2 >= 1)
model.addCons(x3 + x6 <= 1)
model.addCons(x3 + x1 <= 1)
model.addCons(x5 + x6 <= 1)
model.addCons(x5 + x1 <= 1)
model.addCons(x5 + x2 <= 1)
model.addCons(x5 + x4 <= 1)
model.addCons(x1 + x2 <= 1)
model.addCons(x1 + x4 <= 1)
model.addCons(x5 + x1 >= 1)
model.addCons(x5 + x6 >= 1)
model.addCons(x2 + x1 >= 1)
model.addCons(x2 + x6 >= 1)

model.optimize()

print("Optimal value: %f" % model.getObjVal())
print("x1: = %f" % model.getVal(x1))
print("x2: = %f" % model.getVal(x2))
print("x3: = %f" % model.getVal(x3))
print("x4: = %f" % model.getVal(x4))
print("x5: = %f" % model.getVal(x5))
print("x6: = %f" % model.getVal(x6))
