# cost.py
import math

def unit_cost(x1, y1, x2, y2):
    """
    Chi phí di chuyển cơ bản (mỗi bước = 1)
    """
    return 1

def manhattan_cost(x1, y1, x2, y2):
    """
    Chi phí Manhattan (|dx| + |dy|)
    """
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_cost(x1, y1, x2, y2):
    """
    Chi phí Euclidean (căn bậc 2(dx^2 + dy^2))
    """
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

DEFAULT_COST = unit_cost