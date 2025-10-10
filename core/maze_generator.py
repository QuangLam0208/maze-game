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

    state = reset_pathfinding()
    return maze, state

def generate_beautiful_maze(size: int):
    """
    Tạo maze đẹp với pattern cân đối và có nhiều đường đi thú vị
    Sử dụng thuật toán Recursive Backtracking với cải tiến
    """
    import random
    
    # Khởi tạo maze toàn bộ là tường
    maze = [[1 for _ in range(size)] for _ in range(size)]
    
    # Hàm để kiểm tra xem có thể carve không
    def can_carve(x, y):
        return (0 <= x < size and 0 <= y < size and maze[x][y] == 1)
    
    # Hàm để carve một đường đi
    def carve(x, y):
        maze[x][y] = 0
    
    # Recursive backtracking với cải tiến
    def recursive_backtrack(x, y):
        carve(x, y)
        
        # Tạo list các hướng ngẫu nhiên
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Kiểm tra có thể carve không
            if can_carve(nx, ny):
                # Carve đường đi và tường giữa
                carve((x + nx) // 2, (y + ny) // 2)  # Tường giữa
                recursive_backtrack(nx, ny)
    
    # Bắt đầu từ (1,1) để có viền
    if size > 1:
        recursive_backtrack(1, 1)
    
    # Đảm bảo start và goal
    maze[0][0] = 0  # Start
    maze[size-1][size-1] = 0  # Goal
    
    # Tạo kết nối an toàn từ start
    if size > 2:
        maze[0][1] = 0
        maze[1][0] = 0
        if maze[1][1] == 1:
            maze[1][1] = 0
    
    # Tạo kết nối an toàn đến goal
    if size > 2:
        maze[size-1][size-2] = 0
        maze[size-2][size-1] = 0
        if maze[size-2][size-2] == 1:
            maze[size-2][size-2] = 0
    
    # Tạo một số đường đi thêm để maze thú vị hơn nhưng không quá dễ
    cycles_to_add = max(1, size // 12)  # Ít cycle hơn để giữ độ khó
    for _ in range(cycles_to_add):
        x = random.randint(1, size-2)
        y = random.randint(1, size-2)
        
        if maze[x][y] == 1:
            # Đếm các neighbor là đường đi
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0):
                    neighbors.append((nx, ny))
            
            # Chỉ carve nếu có đúng 2 neighbors (tạo cycle)
            if len(neighbors) == 2:
                # Kiểm tra 2 neighbors không nằm đối diện nhau
                if neighbors[0][0] != neighbors[1][0] or neighbors[0][1] != neighbors[1][1]:
                    maze[x][y] = 0
    
    # Tạo một số room nhỏ để maze đẹp hơn
    rooms_to_add = max(1, size // 16)
    for _ in range(rooms_to_add):
        room_x = random.randint(2, size-3)
        room_y = random.randint(2, size-3)
        
        # Tạo room 2x2
        room_created = False
        if (maze[room_x][room_y] == 1 and maze[room_x+1][room_y] == 1 and
            maze[room_x][room_y+1] == 1 and maze[room_x+1][room_y+1] == 1):
            
            # Kiểm tra có ít nhất 1 kết nối với đường đi hiện có
            connections = 0
            for dx, dy in [(-1, 0), (2, 0), (0, -1), (0, 2)]:
                for rx, ry in [(room_x, room_y), (room_x+1, room_y), 
                              (room_x, room_y+1), (room_x+1, room_y+1)]:
                    check_x, check_y = rx + dx, ry + dy
                    if (0 <= check_x < size and 0 <= check_y < size and 
                        maze[check_x][check_y] == 0):
                        connections += 1
                        break
                if connections > 0:
                    break
            
            if connections > 0:
                maze[room_x][room_y] = 0
                maze[room_x+1][room_y] = 0
                maze[room_x][room_y+1] = 0
                maze[room_x+1][room_y+1] = 0
                room_created = True
    
    # Đảm bảo có đường đi từ start đến goal bằng cách tạo đường backup
    # Tạo đường thẳng đơn giản từ start về goal (nếu cần)
    if size > 8:
        # Đường ngang từ start
        for i in range(min(4, size//3)):
            if maze[0][i] == 1:
                maze[0][i] = 0
        
        # Đường dọc đến goal  
        for i in range(max(size-4, size*2//3), size):
            if maze[i][size-1] == 1:
                maze[i][size-1] = 0
    
    state = reset_pathfinding()
    return maze, state