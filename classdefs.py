from dataclasses import dataclass
from typing import Self
import periodictable as pt


class element_type(pt.core.Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mass = int()
        raise NotImplementedError(f"Type {type(self)} is not meant to be instantiated, it is only for static type checking")



@dataclass
class elem:
    element: element_type
    coeff: int

    def __str__(self):
        return f"<{self.coeff} {str(self.element.name).capitalize()} Mass: {self.element.mass * self.coeff}>"



class Compound:
    prefixs = {
        1: "Mono",
        2: "Di",
        3: "Tri",
        4: "Tetra",
        5: "Penta",
        6: "Hexa",
        7: "Hepta",
        8: "Octa",
        9: "Ennea",
        10: "Deca",
        11: "Hendeca",
        12: "Dodeca",
    }
    def __init__(self, elements:list=None, coeff:int=1):
        """
        COMPOUND Type, represends a chemical coumpound
        :param elements:
        :param coeff:
        """
        self.coeff = coeff
        if elements is None: elements = []
        self.elements = elements
        self._mass = 0

        for _dx, _ in enumerate(self.elements):
            if type(_) == Compound:
                index = self.elements.index(_)
                self.elements.pop(index)
                for edx, ele in enumerate(_.elements):
                    self.elements.insert(edx + index, ele)

        self.mass_calc()

    def mass_calc(self):
        self._mass = 0
        for _ in self.elements:
            # TODO compound group logic
            if type(_) == elem:
                self._mass += _.element.mass * _.coeff
            elif type(_) == type(self):
                self._mass += _.mass * _.coeff

    @property
    def mass(self):
        return round(self._mass, 3)  #Fixme Introduces Numerical Errors


    def __add__(self, other: elem | Self):
        self.elements.append(other)
        if type(other) == elem:
            self._mass += other.element.mass
        elif type(other) == Self:
            self._mass += other.mass

    def subscript_add(self, other: int):
        self.elements[-1].coeff += other
        self.mass_calc()
        #self._mass += other * self.elements[-1].element.mass

    def subs_set(self, other: int):
        self.elements[-1].coeff = other
        self.mass_calc()

    def group_multiply(self, multiple: int):
        for _ in self.elements:
            _.coeff *= multiple

    @property
    def name(self) -> str:
        """
        Method to construct and return compound name on the fly
        :return: Compound Name
        """

        #name = ' '.join([f"{self.prefixs[_.coeff] if (_.coeff != 1) and (_.coeff <= 12) else ''}"
        #                 f"{str(_.element.name).capitalize()}" for _ in self.elements])

        name_array = []
        for _ in self.elements:
            if type(_) == elem:
                name_array.append(f"{self.prefixs[_.coeff] if (_.coeff != 1) and (_.coeff <= 12) else ''}{str(_.element.name).capitalize()}")
            elif type(_) == type(self):
                name_array.append(f"({_.name}){_.coeff}")
            else:
                raise TypeError(f"Type Error: {type(_)}; Self Type: {type(self)}")

        return ' '.join(name_array)


    def __str__(self):

        #TODO introduce naming rules
        #FIXME, Naming rules
        #name = ' '.join([f"{self.prefixs[_.coeff] if (_.coeff != 1) and (_.coeff <= 12) else ''}{str(_.element.name).capitalize()}" for _ in self.elements]) #Todo Prefixs
        #symbols = ''.join([f'{_.element.symbol}{_.coeff if _.coeff != 1 else ""}' for _ in self.elements])

        name = self.name
        symbols = ""

        return f"""
Compound {name}
    {symbols}
    Mass // {self._mass}
    Coeff // {self.coeff}
"""

    def __repr__(self):
        return self.name
        #return ''.join([f'{_.element.symbol}{_.coeff if _.coeff != 1 else ""}' for _ in self.elements])

