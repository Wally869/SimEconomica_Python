from dataclasses import dataclass


@dataclass
class PriceBelief(object):
    LowerBound: int
    HigherBound: int

    def TranslateRange_Int(self, displacement: int):
        self.LowerBound += displacement
        self.HigherBound += displacement

    def TranslateRange_Float(self, displacement: float):
        self.LowerBound = int(self.LowerBound * displacement)
        self.HigherBound = int(self.HigherBound * displacement)

    def TranslateBounds_Int(self, lowerDisplacement: int, higherDisplacement: int):
        self.LowerBound += lowerDisplacement
        self.HigherBound += higherDisplacement

    def TranslateBounds_Float(
        self, lowerDisplacement: float, higherDisplacement: float
    ):
        self.LowerBound = int(self.LowerBound * lowerDisplacement)
        self.HigherBound = int(self.HigherBound * higherDisplacement)
