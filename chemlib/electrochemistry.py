from chemlib.chemistry import Element

F = 96485 #Faraday's constant in coulombs

def electrolysis(element: str, n: int, **kwargs) -> dict:
    keys = kwargs.keys()

    if 'seconds' not in keys and 'amps' not in keys and 'grams' not in keys:
        raise TypeError('Expecting two args from either grams= , amps= , or seconds=')

    if len(kwargs) != 2:
        raise TypeError(f"Got {len(kwargs)} arguments when expecting 2 from either grams= , amps= , or seconds=")

    elem = Element(element)

    if ('seconds' in keys) and ('amps' in keys):
        secs = kwargs['seconds']
        amps = kwargs['amps']
        grams = secs*amps/F/n*float(elem.AtomicMass)
    
    elif ('seconds' in keys) and ('grams' in keys):
        secs = kwargs['seconds']
        grams = kwargs['grams']
        amps = grams/float(elem.AtomicMass)*n*F/secs
    
    else:
        amps = kwargs['amps']
        grams = kwargs['grams']
        secs = grams/float(elem.AtomicMass)*n*F/amps

    return {
        "element": element,
        "n": n,
        "seconds": secs,
        "amps": amps,
        "grams": grams,
    }

if __name__ == "__main__":
    print(electrolysis('Ti', 4, amps=1, grams=0.839))