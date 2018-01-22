class constraint_programming:

    def __init__(self, var):
        """
        :param var: dict (K, V), K is a variable, V its domain (list of value)
        """
        self.var = var
        self.constr = {x: [] for x in var}
        self.assign = {x:None for x in var}
        self.log = []
        for x in var:
            for y in var:
                if x != y and var[x] is var[y]:
                    raise "Variables have same domain object."

    def add_constraints(self, x, y, rel):
        """
        rel is a set of tuple
        """
        self.constr[x].append(y, rel)
        self.constr[y].append(x, set(map(reversed, rel)))

    def solve(self):
        x = self.choice_var() # variable branchement
        if x is None:
            return self.assign # Success
        for u in self.var[x]:
            history = self.save_context()
            self.assign[x] = u
            self.forward_check(x, u)
            sol = self.solve()
            if sol:
                return sol
            self.assign[x] = None
            self.restore_context(history)

    def choice_var(self):
        best = None
        for x in self.var:
            if self.assign[x] is None and (
                    best is None or len(self.var[x]) < len(best)):
                return x
        return None

    def forward_check(self, x, u):
        for (y, rel) in self.constr[x]:
            to_remove = set()
            for v in self.var[y]:
                if (u, v) not in rel:
                    to_remove.add(v)
            if to_remove:
                self.remove_vals(y, to_remove)

    def remove_vals(self, y, to_remove):
        self.var[y] -= to_remove
        self.log.append((y, to_remove))

    def save_context(self):
        return len(self.log)

    def restore_context(self, history):
        while len(self.log) > history:
            (y, to_remove) = self.log.pop()
            self.var[y] += to_remove
