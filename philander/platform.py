from enum import Enum
import platform

class Platform(Enum):
    Windows = 1
    Linux = 2
    Mac = 3

current = Platform[platform.system()]
