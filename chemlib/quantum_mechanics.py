from chemlib.constants import c, h, R

class Wave:
    def __init__(self, **kwargs):
        keys = kwargs.keys()

        if ('wavelength' not in keys and 'frequency' not in keys and 'energy' not in keys) or (len(keys) != 1):
            raise ValueError('Expecting one argument: either wavelength= , frequency= , or energy=')

        mode = list(keys)[0]
        if mode == 'frequency':
            self.frequency = kwargs[mode]
            self.wavelength = c/self.frequency

        elif mode == 'wavelength':
            self.wavelength = kwargs[mode]
            self.frequency = c/self.wavelength
        
        else:
            self.frequency = kwargs[mode]/h
            self.wavelength = c/self.frequency
            
        self.energy = h*self.frequency

        self.properties = {
            "wavelength": float('{:0.3e}'.format(self.wavelength)),
            "frequency": float('{:0.3e}'.format(self.frequency)),
            "energy": float('{:0.3e}'.format(self.energy))
        }

def energy_of_hydrogen_orbital(n):
    return((-h*R*c)*(1 / (n*n)))

def rydberg(element, n1, n2):
    Z = element.AtomicNumber
    if not (n2 > n1):
        raise ValueError("In the Rydberg Equation, n2 is always greater than n1.")
    length = ((R*Z*Z)*((1/(n1**2)) - (1/(n2**2))))**-1
    return Wave(wavelength = length).properties

if __name__ == "__main__":
    print(energy_of_hydrogen_orbital(3))
    w = Wave(frequency=5.6e16)
    print(w.properties)