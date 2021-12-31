from dataclasses import dataclass
import numpy as np
@dataclass
class FluidEventHistory:
    bladderFillingLevels: np.ndarray = np.array([])
    bodyStorage : np.ndarray = np.array([])
    workoutLoss : np.ndarray = np.array([])
    totalLiquidLoss: np.ndarray = np.array([])
    isFinished: bool = False 