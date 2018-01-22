#/usr/bin/env pypy

from pyscipopt import Model

model = Model("try")

x = model.addVar("x")
y = model.addVar("y")

model.addCons(2 * x + y <= 10, "bound costs")
model.addCons(2* x + 5 * y <= 30, "bound costs")

model.setObjective(x + y, "maximize")   # autre possibilité "minimize"
model.optimize()

print("Optimal value: %f" % model.getObjVal())
print("x: = %f" % model.getVal(x))
print("y: = %f" % model.getVal(y))
