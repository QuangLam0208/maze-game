from collections import deque
import time
import pygame
from utils.algorithm_runner import update_game_state, check_goal, handle_frame, algorithm_finished

class AndOrNode:
    """Node trong AND-OR Search Tree"""
    def __init__(self, position, path, node_type="OR", children=None):
        self.position = position  # (x, y)
        self.path = path  # Đường đi đến node này
        self.node_type = node_type  # "OR" hoặc "AND"
        self.children = children if children else []
        self.solved = False  # Node đã được giải hay chưa
        self.expanded = False  # Node đã được mở rộng hay chưa
    
    def __str__(self):
        return f"{self.node_type}({self.position})"

def run_and_or_search(game):
    """Chạy thuật toán AND-OR Search cho MazeGame"""
    
    game.alg_name = "AND-OR Search"

    # Sử dụng custom start và end nếu có
    start_pos = getattr(game, 'custom_start', (0, 0))
    if start_pos is None:
        start_pos = (0, 0)
    
    goal_pos = getattr(game, 'custom_end', None)
    if goal_pos is None:
        goal_pos = (len(game.maze)-1, len(game.maze[0])-1)

    # Khởi tạo root node (OR node)
    root = AndOrNode(start_pos, [start_pos], "OR")
    
    # Queue để duyệt các nodes
    queue = deque([root])
    visited_set = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    step_count = 0
    solution_path = []

    while queue and game.is_running:
        # Animation & sự kiện
        result = handle_frame(game, step_count)
        if result is None:
            return
        step_count, ok = result
        if not ok:
            return
        
        # Lấy node tiếp theo
        current_node = queue.popleft()
        x, y = current_node.position
        
        if (x, y) in visited_set:
            continue
            
        # Cập nhật trạng thái
        update_game_state(game, x, y, visited_set)
        
        # Cập nhật path để hiển thị nhánh đang xét bằng màu vàng
        game.path = current_node.path
        
        step_count += 1
        
        # Kiểm tra goal
        if check_goal(game, x, y, current_node.path):
            return
        
        # Mở rộng node nếu chưa được mở rộng
        if not current_node.expanded:
            expand_node(game, current_node, directions, queue)
            current_node.expanded = True
        
        # Cập nhật trạng thái solved cho node
        update_solved_status(current_node)
    
    # Kết thúc thuật toán
    game.is_running = False
    game.current_node = None
    
    # Add to history if no path was found
    algorithm_finished(game)

def expand_node(game, node, directions, queue):
    """Mở rộng một node trong AND-OR tree"""
    x, y = node.position
    
    # Tìm tất cả các hướng có thể đi
    valid_moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (0 <= nx < len(game.maze) and 0 <= ny < len(game.maze[0]) and 
            game.maze[nx][ny] == 0):  # Ô trống
            valid_moves.append((nx, ny))
            game.stats["nodes_expanded"] += 1
    
    if len(valid_moves) == 0:
        # Dead end - không có đường đi
        node.solved = False
        return
    elif len(valid_moves) == 1:
        # Chỉ có 1 đường đi - tạo OR node
        nx, ny = valid_moves[0]
        child_path = node.path + [(nx, ny)]
        child = AndOrNode((nx, ny), child_path, "OR")
        node.children.append(child)
        queue.append(child)
    else:
        # Có nhiều đường đi - tạo AND node với các OR children
        if node.node_type == "OR":
            # OR node với nhiều lựa chọn -> tạo AND node trung gian
            and_node = AndOrNode(node.position, node.path, "AND")
            node.children.append(and_node)
            
            for nx, ny in valid_moves:
                child_path = node.path + [(nx, ny)]
                or_child = AndOrNode((nx, ny), child_path, "OR")
                and_node.children.append(or_child)
                queue.append(or_child)
        else:
            # AND node - tất cả children phải thành công
            for nx, ny in valid_moves:
                child_path = node.path + [(nx, ny)]
                child = AndOrNode((nx, ny), child_path, "OR")
                node.children.append(child)
                queue.append(child)

def update_solved_status(node):
    """Cập nhật trạng thái solved cho node dựa trên children"""
    if not node.children:
        # Leaf node - chưa biết solved hay không
        return
    
    if node.node_type == "OR":
        # OR node: solved nếu ít nhất 1 child solved
        node.solved = any(child.solved for child in node.children)
    else:
        # AND node: solved nếu tất cả children solved
        node.solved = all(child.solved for child in node.children)

def and_or_graph_search(problem, node, path):
    """
    Thuật toán AND-OR Graph Search chuẩn
    (Phiên bản đơn giản cho tham khảo)
    """
    if problem.is_goal(node.position):
        return [node.position]
    
    if node.position in path:
        return None  # Cycle detected
    
    # Mở rộng node
    successors = problem.get_successors(node.position)
    
    if not successors:
        return None  # Dead end
    
    if len(successors) == 1:
        # OR node - chỉ cần 1 successor thành công
        new_path = path + [node.position]
        result = and_or_graph_search(problem, successors[0], new_path)
        if result is not None:
            return [node.position] + result
    else:
        # AND node - tất cả successors phải thành công
        new_path = path + [node.position]
        all_paths = []
        for successor in successors:
            result = and_or_graph_search(problem, successor, new_path)
            if result is None:
                return None  # Một trong các nhánh thất bại
            all_paths.extend(result)
        return [node.position] + all_paths
    
    return None

# Thêm vào game.py algorithms mapping:
# "AND-OR Search": run_and_or_search
