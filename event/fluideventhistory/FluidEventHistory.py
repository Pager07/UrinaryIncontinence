from dataclasses import dataclass
@dataclass
class ModelParameters:
    mu: int  = 50 #suggested [40-60] min
    sigma: int = 4.6 #suggested [3-6] min
    maxFillingRate: int = 5 #suggest [4-8]ml/min