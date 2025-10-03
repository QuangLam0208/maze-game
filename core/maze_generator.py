import random
from core.path_finding import reset_pathfinding

def generate_maze(size: int, wall_prob: float = 0.3):
    """
    Sinh ngẫu nhiên một maze size x size.
    0 = đường đi, 1 = tường.
    """
    maze = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if random.random() < wall_prob and not (i == 0 and j == 0) and not (i == size - 1 and j == size - 1):
                maze[i][j] = 1  # Tường

    state = reset_pathfinding()
    return maze, state

def generate_beautiful_maze(size: int):
    """
    Tạo maze đẹp với pattern phức tạp như hình mẫu
    """
    # Bắt đầu với tất cả là tường
    maze = [[1 for _ in range(size)] for _ in range(size)]
    
    # Tạo đường chính từ start đến goal
    def carve_path(x, y, target_x, target_y):
        """Tạo đường đi từ (x,y) đến (target_x, target_y)"""
        current_x, current_y = x, y
        maze[current_x][current_y] = 0
        
        visited = set()
        stack = [(current_x, current_y)]
        
        while stack and (current_x != target_x or current_y != target_y):
            current_x, current_y = stack[-1]
            
            if (current_x, current_y) in visited:
                stack.pop()
                if stack:
                    current_x, current_y = stack[-1]
                continue
                
            visited.add((current_x, current_y))
            maze[current_x][current_y] = 0
            
            # Tìm hướng đi ưu tiên về phía target
            directions = []
            
            # Ưu tiên hướng về target
            if target_x > current_x and current_x + 2 < size:
                directions.append((2, 0))  # Xuống
            if target_y > current_y and current_y + 2 < size:
                directions.append((0, 2))  # Phải
            if target_x < current_x and current_x - 2 >= 0:
                directions.append((-2, 0))  # Lên
            if target_y < current_y and current_y - 2 >= 0:
                directions.append((0, -2))  # Trái
                
            # Thêm các hướng khác
            for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)]:
                if (dx, dy) not in directions:
                    new_x, new_y = current_x + dx, current_y + dy
                    if 0 <= new_x < size and 0 <= new_y < size:
                        directions.append((dx, dy))
            
            # Chọn hướng đi
            moved = False
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if (0 <= new_x < size and 0 <= new_y < size and 
                    (new_x, new_y) not in visited):
                    
                    # Carve the path (bao gồm cả ô giữa)
                    maze[current_x + dx//2][current_y + dy//2] = 0
                    maze[new_x][new_y] = 0
                    stack.append((new_x, new_y))
                    moved = True
                    break
            
            if not moved:
                stack.pop()
    
    # Tạo maze pattern với recursive backtracking
    def create_maze_pattern():
        # Bắt đầu từ (1,1) để tránh biên
        visited = set()
        
        def dfs(x, y):
            visited.add((x, y))
            maze[x][y] = 0
            
            # Tạo danh sách hướng đi ngẫu nhiên
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                # Kiểm tra biên và chưa thăm
                if (0 < new_x < size-1 and 0 < new_y < size-1 and 
                    (new_x, new_y) not in visited):
                    
                    # Carve path
                    maze[x + dx//2][y + dy//2] = 0
                    dfs(new_x, new_y)
        
        # Bắt đầu từ vị trí lẻ
        start_x = 1 if size > 1 else 0
        start_y = 1 if size > 1 else 0
        dfs(start_x, start_y)
    
    # Tạo pattern maze
    create_maze_pattern()
    
    # Đảm bảo có đường từ start đến goal
    maze[0][0] = 0  # Start
    maze[size-1][size-1] = 0  # Goal
    
    # Kết nối start với maze chính
    if size > 2:
        maze[0][1] = 0
        maze[1][0] = 0
        maze[1][1] = 0
    
    # Kết nối goal với maze chính  
    if size > 2:
        maze[size-1][size-2] = 0
        maze[size-2][size-1] = 0
        maze[size-2][size-2] = 0
    
    # Tạo thêm một số kết nối để đảm bảo có đường đi
    for _ in range(size // 4):
        x = random.randint(1, size-2)
        y = random.randint(1, size-2)
        
        # Tạo kết nối với ô lân cận
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size:
                if maze[x][y] == 0 or maze[new_x][new_y] == 0:
                    maze[x][y] = 0
                    maze[new_x][new_y] = 0
    
    state = reset_pathfinding()
    return maze, state

def generate_beautiful_maze(size: int):
    """
    Tạo maze đẹp với pattern phức tạp như trong hình
    Sử dụng thuật toán Recursive Backtracking để tạo maze có cấu trúc đẹp
    """
    # Khởi tạo maze toàn bộ là tường
    maze = [[1 for _ in range(size)] for _ in range(size)]
    
    # Stack để backtrack
    stack = []
    current = (1, 1)  # Bắt đầu từ (1,1) để có viền
    maze[current[0]][current[1]] = 0
    stack.append(current)
    
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Di chuyển 2 ô để tạo tường giữa
    
    while stack:
        current = stack[-1]
        neighbors = []
        
        # Tìm các neighbor chưa được visit
        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            
            # Kiểm tra trong bounds và chưa được visit
            if (0 < new_x < size-1 and 0 < new_y < size-1 and 
                maze[new_x][new_y] == 1):
                neighbors.append((new_x, new_y))
        
        if neighbors:
            # Chọn neighbor ngẫu nhiên
            next_cell = random.choice(neighbors)
            
            # Tạo đường đi đến neighbor
            wall_x = (current[0] + next_cell[0]) // 2
            wall_y = (current[1] + next_cell[1]) // 2
            
            maze[next_cell[0]][next_cell[1]] = 0
            maze[wall_x][wall_y] = 0
            
            stack.append(next_cell)
        else:
            stack.pop()
    
    # Đảm bảo có đường từ start đến goal
    maze[0][0] = 0  # Start
    maze[size-1][size-1] = 0  # Goal
    
    # Tạo kết nối đến start và goal
    if size > 2:
        maze[0][1] = 0
        maze[1][0] = 0
        maze[size-1][size-2] = 0
        maze[size-2][size-1] = 0
    
    # Thêm một số đường đi phụ để tăng độ phức tạp
    for _ in range(size // 4):
        x = random.randint(1, size-2)
        y = random.randint(1, size-2)
        if maze[x][y] == 1:
            # Kiểm tra xem có tạo được đường đi không
            neighbors_count = 0
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                    neighbors_count += 1
            
            # Chỉ tạo đường nếu có ít nhất 1 neighbor là đường đi
            if neighbors_count >= 1 and neighbors_count <= 2:
                maze[x][y] = 0
    
    state = reset_pathfinding()
    return maze, state