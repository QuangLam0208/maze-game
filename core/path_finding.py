def reset_pathfinding():
    """
    Reset trạng thái tìm đường mặc định.
    Trả về dict chứa các giá trị khởi tạo.
    """
    return {
        "visited": set(),
        "path": [],
        "current_node": None,
        "is_running": False,
        "stats": {"nodes_visited": 0, "path_length": 0, "time": 0}
    }