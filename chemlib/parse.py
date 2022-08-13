import re

FORMULA_PARENS = re.compile(r"\((.*?)\)(\d*)") 
FORMULA_REGULAR = re.compile(r"(\(?)([A-Z][a-z]?)(\d*)(\)?)")

def parse_formula(formula : str) -> dict: 
    def multiply(form: dict, mul: int) -> None:
        for key in form: form[key] *= mul

    formDict = {}
    # PARENS
    for match in FORMULA_PARENS.finditer(formula):
        parens = parse_formula(match.group(1))
        mul = match.group(2)
        if not mul: mul = 1
        multiply(parens, int(mul))
        formDict.update(parens)
    # REST
    for match in FORMULA_REGULAR.finditer(formula):
        left, elem, mul, right = match.groups()
        if left or right: continue
        if not mul: mul = 1
        if elem in formDict:
            formDict[elem] += int(mul)
        else:
            formDict[elem] = int(mul)

    return formDict

if __name__ == '__main__':
    b = "CH3COO"
    form = parse_formula(b)
    print(form)