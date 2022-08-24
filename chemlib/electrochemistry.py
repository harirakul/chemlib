from chemlib.chemistry import Element
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from chemlib.constants import F 

this_dir, this_filename = os.path.split(__file__)
DIAGRAM_PATH = os.path.join(this_dir, "resources", "gcell_root.png")

REDUCTION_POTENTIALS = REDPOTS = {
    "Ba": (-2.90, 2),
    "Ca": (-2.87, 2),
    "Na": (-2.71, 2),
    "Mg": (-2.37, 2),
    "Al": (-1.66, 3),
    "Mn": (-1.18, 2),
    "Zn": (-0.76, 2),
    "Fe": (-0.44, 2),
    "Cd": (-0.403, 2),
    "Co": (-0.277, 2),
    "Ni": (-0.25, 2),
    "Sn": (-0.136, 2),
    "Pb": (-0.13, 2),
    "H": (0, 2),
    "H2": (0, 2),
    "Cu": (0.34, 2),
    "Ag": (0.80, 1),
    "F2": (2.87, 2),
    "Cl2": (1.36, 2),
    "Br2": (1.09, 2),
    "I2": (0.54, 2),
}

class Galvanic_Cell():
    def __init__(self, electrode1: str, electrode2: str) -> None:
        e1, e2 = electrode1, electrode2

        if e1 not in REDPOTS:
            raise NotImplementedError(f"The reduction potential of {e1} is not yet implemented or {e1} is not a valid electrode.")
        if e2 not in REDPOTS:
            raise NotImplementedError(f"The reduction potential of {e2} is not yet implemented or {e2} is not a valid electrode.")
        
        if REDPOTS[e1][0] > REDPOTS[e2][0]: 
            self.anode = (e2, REDPOTS[e2])
            self.cathode = (e1, REDPOTS[e1])
        else:
            self.anode = (e1, REDPOTS[e1])
            self.cathode = (e2, REDPOTS[e2])
        
        self.electrodes = (self.anode, self.cathode)
        self.cell_potential = self.E0 = self.cathode[1][0] - self.anode[1][0]
        self.line_notation = f"{self.anode[0]} | {self.anode[0]}{self.anode[1][1]}+ || {self.cathode[0]}{self.cathode[1][1]}+ | {self.cathode[0]}".replace("1", '')
        endings = ["2SO4", "SO4", "2(SO4)3"]
        self.anode_soln = f"{self.anode[0]}{endings[self.anode[1][1] - 1]}"
        self.cathode_soln = f"{self.cathode[0]}{endings[self.cathode[1][1] - 1]}"

        self.properties = {
            "Cell": self.line_notation,
            "Anode": self.anode[0],
            "Cathode": self.cathode[0],
            "Cell Potential": self.E0
        }

        #self.draw()
    
    def draw(self, show = True):
        def font(size):
            return ImageFont.truetype("arial.ttf", size, encoding="unic")

        img = Image.open(DIAGRAM_PATH)
        editor = ImageDraw.Draw(img)
        # Line Notation
        editor.text((160, 4), self.line_notation, (0, 0, 0), font = font(24))
        # Cell pot
        editor.text((250, 40), f"{self.E0}V", (255, 0, 0), font = font(20))
        # Anode
        editor.text((70, 230), self.anode[0], (0, 0, 0), font = font(20))
        editor.text((163, 425), "Anode", (0, 0, 0), font = font(15))
        # Cathode
        editor.text((458, 230), self.cathode[0], (0, 0, 0), font = font(20))
        editor.text((345, 425), "Cathode", (0, 0, 0), font = font(15))
        # Electrons
        editor.text((140, 45), "e-", (0, 0, 255), font = font(25))
        editor.text((400, 45), "e-", (0, 0, 255), font = font(25))
        # Ions in Solution
        editor.text((175, 327),  f"{self.anode[0]}{self.anode[1][1]}+", (0, 0, 0), font = font(15))
        editor.text((338, 327),  f"{self.cathode[0]}{self.cathode[1][1]}+", (0, 0, 0), font = font(15))
        # Solutions
        editor.text((50, 412), f"{self.anode_soln}(aq)", (0, 0, 0), font = font(15))
        editor.text((420, 412), f"{self.cathode_soln}(aq)", (0, 0, 0), font = font(15))

        self.diagram = img
        
        if show:
            self.diagram.show()

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
    g = Galvanic_Cell('Pb', 'Zn')
    g.draw()
    print(electrolysis('Ti', 4, amps=1, grams=0.839))