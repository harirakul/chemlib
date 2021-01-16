import inspect
from fractions import Fraction

class DimensionalAnalyzer():
    def __init__(self, rounding = 3, **kwargs) -> None:
        self.kwargs = kwargs
        self.dependencies = {}
        self.rounding = rounding
        for item in self.kwargs:
            arg = tuple(inspect.signature(self.kwargs[item]).parameters)[0]
            self.dependencies.update({item: arg})
    
    def __getitem__(self, item: str):
        return self.kwargs[item]
    
    def validate(self, item: str):
        if item not in self.kwargs: raise ValueError("Unknown item.")
    
    def plug(self, **params) -> dict:
        rdict = {}
        for var in params:
            self.validate(var)
            rdict.update({var: rround(params[var], self.rounding)})

        while len(rdict) != len(self.kwargs):
            for item in self.kwargs:
                if item not in rdict:
                    try:
                        rdict.update({item: rround(self.kwargs[item](rdict[self.dependencies[item]]), self.rounding)})
                    except:
                        continue

        return rdict

def rround(num: float, places: int) -> float:
    if 'e' in str(num): return float(f'{num:.{places}e}')
    else: return round(num, places)

def reduce_list(L):
    a = L
    denominators = [f.denominator for f in [Fraction(x).limit_denominator() for x in L]]
    a = [a[i]*max(denominators) for i in range(len(a))]
    a = [a[i]/min(a) for i in range(len(a))]
    a = [round(i) for i in a]
    return a
    
if __name__ == "__main__":
    print(rround(2.32432432423e25, 5))
    # molar_mass = 50
    # AVOGADROS_NUMBER = 6.02e+23

    # d = DimensionalAnalyzer(
    #     grams = lambda mols: mols*molar_mass,
    #     mols = lambda molecules: molecules/AVOGADROS_NUMBER,
    #     molecules = lambda grams: grams/molar_mass*AVOGADROS_NUMBER
    # )

    # print(d.plug(mols = 25))