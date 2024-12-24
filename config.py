HOST = '127.0.0.1'
PORT = 5252
MAX_CONNECTIONS = 10
BUFFERSIZE = 1024

PASSWORD = 'nelly'
SAVE_FILENAME = 'save.json'

import json
from dataclasses import dataclass
from typing import List

@dataclass
class Combination:
    cellType: int
    rewardType: int
    probability: float
    val: int

@dataclass
class SlotConfig:
    winchance: float
    combinations: List[Combination]

@dataclass
class UserLuck:
    winchance: float
    j_probability: float
    m_probability: float

class ConfigManager:
    luck_config: SlotConfig = None

    @staticmethod
    def inilialize():
        ConfigManager.load_luck_config('luck_config.json')

    @staticmethod
    def load_luck_config(file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        combinations = [Combination(**combo) for combo in data['combinations']]
        
        ConfigManager.luck_config = SlotConfig(
            winchance=data['winchance'],
            combinations=combinations
        )

    @staticmethod
    def default_luck() -> UserLuck:
        j, m = 0.07, 0.07
        for comb in ConfigManager.luck_config.combinations:
            if comb.cellType == 4:
                j = comb.probability
            elif comb.cellType == 1:
                m = comb.probability

        return UserLuck(ConfigManager.luck_config.winchance, j, m)