c = 2.998*10**8    #Speed of light
h = 6.626*10**-34  #Planck's constant
R = 1.0974*10**7  #Rydberg constant

class Wave:
    def __init__(self, **kwargs):
        keys = kwargs.keys()

        if ('wavelength' not in keys and 'frequency' not in keys and 'energy' not in keys) or (len(keys) != 1):
            raise ValueError('Expecting one argument: either grams= , moles= , or molecules=')

        mode = list(keys)[0]
        if mode == 'frequency':
            self.frequency = kwargs[mode]
            self.wavelength = c/self.frequency

        elif mode == 'wavelength':
            self.wavelength = kwargs[mode]
            self.frequency = c/self.wavelength
        
        else:
            self.wavelength = h*c/self.frequency
            self.frequency = c/self.wavelength

        self.energy = h*self.frequency

        self.properties = {
            "wavelength": float('{:0.3e}'.format(self.wavelength)),
            "frequency": float('{:0.3e}'.format(self.frequency)),
            "energy": float('{:0.3e}'.format(self.energy))
        }

def energy_of_hydrogen_orbital(n):
    return((-h*R*c)*(1 / (n*n)))

if __name__ == "__main__":
    print(energy_of_hydrogen_orbital(3))
    w = Wave(frequency=5.6e16)
    print(w.properties)