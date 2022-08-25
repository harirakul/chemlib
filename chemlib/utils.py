import inspect
from fractions import Fraction
import pandas as pd
from sympy import Eq, Symbol, solve

class DimensionalAnalyzer():
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.dependencies = {}
        for item in self.kwargs:
            arg = tuple(inspect.signature(self.kwargs[item]).parameters)[0]
            self.dependencies.update({item: arg})
        
        self.reverse_deps = {v: k for k, v in self.dependencies.items()}
    
    def __getitem__(self, item: str):
        return self.kwargs[item]
    
    def validate(self, item: str):
        if item not in self.kwargs: raise ValueError("Unknown item.")
    
    def plug(self, **params) -> dict:
        rdict = {}
        for var in params:
            self.validate(var)
            rdict.update({var: params[var]})

        while len(rdict) != len(self.kwargs):
            for item in self.kwargs:
                if item not in rdict:
                    try:
                        #known = self.reverse_deps[item]
                        rdict.update({item: self.kwargs[item](rdict[self.dependencies[item]])})
                    except:
                        continue

        return rdict

class Quantity():
    def __init__(self, name: str, change = 1, initial = 0, final = None) -> None:
        self.name = name
        self.initial = initial
        self.change = change
        self.final = final
    
    def todict(self) -> dict:
        d = self.__dict__
        d['change'] = str(d['change']) + "x"
        return d
    
    def solvable(self) -> bool:
        return self.final is not None and self.initial is not None

    def solve(self):
        if self.solvable():
            return (self.final - self.initial)/self.change
    
    def plug(self, x: int):
        self.final = self.initial + self.change*x

class ICETable():
    def __init__(self, quantities: list, relationship = None, show_work = False) -> None:
        if not any(q.solvable() for q in quantities) and relationship is None:
            raise ValueError("Not enough information to solve for x given the quantities. A relationship between the final values needs to be provided.")
        
        self.quantities = quantities
        self.relationship = relationship
        self.show_work = show_work
    
    def show(self, *args):
        if self.show_work: print(*args)
    
    def solve(self) -> float:
        if any(q.solvable() for q in self.quantities):
            for q in self.quantities:
                if q.solvable():
                    self.x = q.solve()
                    break
        
        else: #have to use a relationship
            x = Symbol('x')
            arg = [a.initial + a.change*x for a in self.quantities]
            eqn = self.relationship(*arg)
            solns = solve(eqn)

            for s in solns:
                if s > 0 and 'I' not in str(s):
                    self.x = s
                    break

        for q in self.quantities:
            if not q.solvable():
                q.plug(self.x)
                  
        self.update_table()
        self.show(str(eqn)[3:-1].replace(',', ' ='))
        self.show('x =', self.x)
        return self.x
    
    def update_table(self):
        data = []
        for q in self.quantities:
            data.append(q.todict())

        df = pd.DataFrame(data).T
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace=True)
        self.show(df)

def reduce_list(L):
    a = L
    denominators = [f.denominator for f in [Fraction(x).limit_denominator() for x in L]]
    a = [a[i]*max(denominators) for i in range(len(a))]
    a = [a[i]/min(a) for i in range(len(a))]
    a = [round(i) for i in a]
    return a
    
if __name__ == "__main__":
    import numpy as np
    from chemlib.constants import Kw

    ice = ICETable([
        Quantity("A", change = 1),
        Quantity("B", change = 3),
        Quantity("X", change = -1, initial = 2)
    ],
    relationship= lambda a, b, x: Eq(x / (a * b**3), 0.146),
    show_work = True)

    ice.solve()

    # print(rround(2.32432432423e25, 5))

    # print(DimensionalAnalyzer(
    #     pH = lambda pOH: 14 - pOH,
    #     pOH = lambda H: 14 + np.log10(H),
    #     H = lambda OH: Kw/OH,
    #     OH = lambda pH: 10 ** (-(14 - pH))
    # ).plug(pH = 11.3))