from tkinter import Tk, Canvas, Label, RIDGE, CENTER, Menu
from chemlib.chemistry import PeriodicTable, Element

PTE = PeriodicTable()

COLORSET = {
    "type": {
        "Alkali Metal": "#51c447",
        "Alkaline Earth Metal": "#7beb71",
        "Transition Metal": "#8ab0e6",
        "Halogen": "#c187ff",
        "Metalloid": "#f7a659",
        "Nonmetal": "#f0f266",
        "Metal": "#f06565",
        "Noble Gas": "#ababab",
        "Actinide": "#6ca695",
        "Lanthanide": "#7282ad",
    }
}


class InfoBox(Canvas):
    def __init__(self, master, properties):
        super().__init__(master)
        self.config(
            bg="#86cbf0",
            highlightbackground="black",
            relief=RIDGE,
            width=600,
            height=200,
        )
        self.attrs = properties
        self.write_attrs()

    def show(self):
        self.place(relx=0.39, rely=0.2, anchor=CENTER)

    def hide(self):
        self.place_forget()

    def write(self, x, y, text, font=("Calibri", 10)):
        self.create_text(x, y, text=text, font=font, anchor=CENTER)

    def write_attrs(self):
        element = self.attrs.get("Element")
        self.write(
            300, 20, f"Properties - {element}", ("Calibri", 16, "bold", "underline")
        )


class ElementTile(Element):
    WIDTH = 66
    HEIGHT = 80
    XOFF = 10
    YOFF = 40
    prevTile = None

    def __init__(self, master, symbol):
        super().__init__(symbol)
        self.color = self.assign_color()
        self.tile = Canvas(
            master,
            bg=self.color,
            relief=RIDGE,
            width=self.WIDTH,
            height=self.HEIGHT,
            highlightbackground="black",
        )
        self.infobox = InfoBox(master, self.properties)
        self.mode = "hover"

        self.bind()
        self.setup()
        self.place()

    def set_mode(self, mode):
        if mode != self.mode:
            self.mode = mode
            self.bind()

    def bind(self):
        for binding in ("<Enter>", "<Leave>", "<Button-1>"):
            self.tile.bind(binding, lambda e: None)
        if self.mode == "click":
            self.tile.bind("<Button-1>", self.click)
        else:
            self.tile.bind("<Enter>", self.hover)
            self.tile.bind("<Leave>", self.hover)

    def hover(self, event):
        if str(event.type) == "Enter":
            self.tile.config(bg="white")
            self.infobox.show()
        else:
            self.tile.config(bg=self.color)
            self.infobox.hide()

    def click(self, event):
        prev = ElementTile.prevTile
        if prev is not None:
            prev.tile.config(bg=prev.color)
            prev.infobox.hide()
        self.tile.config(bg="white")
        self.infobox.show()
        ElementTile.prevTile = self

    def setup(self):
        self.make_label("AtomicNumber", 0.15, 10, type_=int)
        self.make_label("Symbol", 0.45, 25)
        self.make_label("Element", 0.7, 8)
        self.make_label("AtomicMass", 0.85, 8, type_=float)

    def place(self):
        if getattr(self, "Type") == "Lanthanide":
            x = self.XOFF + (3 + int(getattr(self, "AtomicNumber")) - 57) * (
                self.WIDTH + 2
            )
            y = 8 * self.HEIGHT
        elif getattr(self, "Type") == "Actinide":
            x = self.XOFF + (3 + int(getattr(self, "AtomicNumber")) - 89) * (
                self.WIDTH + 2
            )
            y = 9 * self.HEIGHT
        else:
            x = self.XOFF + int(getattr(self, "Group") - 1) * (self.WIDTH + 2)
            y = self.YOFF + int(getattr(self, "Period") - 1) * (self.HEIGHT + 2)
        self.tile.place(x=x, y=y)

    def make_label(self, attr, rely, fontsize, type_=str):
        text = getattr(self, attr)
        if type_ is str:
            text = text.strip()
        else:
            text = round(type_(text), 3)
        self.tile.create_text(
            self.WIDTH // 2 + 2,
            rely * self.HEIGHT,
            text=text,
            font=("Calibri", fontsize, "bold"),
            anchor=CENTER,
        )

    def assign_color(self):
        eleType = getattr(self, "Type")
        return COLORSET.get("type").get(eleType)


class PTEGUI(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1250x850")
        self.title("Periodic Table of Elements")
        self.resizable(False, False)

        title = Label(
            self,
            text="The Periodic Table of Elements",
            bg="white",
            font=("Calibri", 25, "bold", "underline"),
        )
        title.place(relx=0.4, rely=0.05, anchor=CENTER)

        self.menu_setup()
        self.tiles = set()
        self.make_table()

    def menu_setup(self):
        menu = Menu(self)
        modeMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Modes", menu=modeMenu)
        modeMenu.add_command(label="Hover", command=lambda: self.mode("hover"))
        modeMenu.add_command(label="Click", command=lambda: self.mode("click"))
        self.config(bg="white", menu=menu)

    def mode(self, nmode):
        for tile in self.tiles:
            tile.set_mode(nmode)

    def make_table(self):
        for symb in PTE["Symbol"]:
            tile = ElementTile(self, symb)
            self.tiles.add(tile)


def GUI(): 
    PTEGUI().mainloop()
