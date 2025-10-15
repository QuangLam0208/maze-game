# MAZE - 
## Thông Tin Đồ Án

**Báo Cáo Cuối Kỳ - Môn: Trí Tuệ Nhân Tạo**

**GVHD:** Phan Thị Huyền Trang

| STT | Sinh viên thực hiện | MSSV |
|-----|---------------------|------|
| 1 | Lương Quang Lâm | 23110121 |
| 2 | Nguyễn Trường Minh | 23110125 |
| 3 | Nguyễn Lê Đức Tuệ | 23110165 |

---

## Giới Thiệu

Trò chơi được xây dựng nhằm mục đích **đánh giá và so sánh các thuật toán tìm kiếm** thuộc 6 nhóm thuật toán chính trong Trí Tuệ Nhân Tạo:

1. **Tìm kiếm không có thông tin** (Uninformed Search)
2. **Tìm kiếm có thông tin** (Informed Search)
3. **Tìm kiếm local search** (Local Search)
4. **Tìm kiếm trong môi trường phức tạp** (Complex Environment)
5. **Tìm kiếm thỏa mãn ràng buộc** (Constraint Satisfaction)
6. **Tìm kiếm đối kháng** (Adversarial Search)

---

## Phân Tích PEAS

### **Performance (Hiệu năng)**
- Tìm kiếm đường đến kho báu **nhanh nhất**
- Số bước đi và thời gian **ít nhất** có thể
- Tránh các vật cản trong quá trình tìm kiếm

### **Environment (Môi trường)**
- Lưu bản đồ bằng **ma trận**
- Bao gồm: tường , start node , goal node 
- **Loại môi trường:**
  - Môi trường có thể quan sát
  - Môi trường tĩnh
  - Môi trường rời rạc
  - Môi trường xác định
  - Môi trường quan sát toàn phần

### **Actuators (Bộ chấp hành)**
- Di chuyển sang **trái, phải, lên, xuống**

### **Sensors (Bộ cảm biến)**
- Vị trí xuất phát
- Vị trí goal
- 4 hướng di chuyển: vật cản hay ô có thể di chuyển được

---

## Các Nhóm Thuật Toán

### **Nhóm 1: Tìm Kiếm Không Có Thông Tin**

#### **Breadth-First Search (BFS)**

Thuật toán tìm kiếm theo chiều rộng sử dụng cấu trúc **Queue** để lưu trữ các trạng thái sinh ra. Queue hoạt động theo cơ chế **FIFO** (First In First Out).

**Đặc điểm:**
- Duyệt hết các lá ở cùng mức trước, sau đó mới đến các mức sâu hơn
- Nếu môi trường trạng thái con sinh nhiều thì độ rộng sẽ rất dài
- Khá tốn không gian lưu trữ

**Độ phức tạp:**
- Thời gian: O(b^d)
- Không gian: O(b^d)

**Hình ảnh (.gif) minh họa thuật toán:**

![BFS Demo](assets/Mazegame_GIF/Uninformed%20Search/BFS.gif)

---

#### **Depth-First Search (DFS)**

Thuật toán tìm kiếm theo chiều sâu sử dụng cấu trúc **Stack** hoạt động theo cơ chế **LIFO** (Last In First Out).

**Đặc điểm:**
- Tối ưu khi kho báu nằm ở một nhánh cụ thể
- Tốn thời gian khi duyệt độ sâu vô hạn
- Tối ưu không gian hơn BFS

**Độ phức tạp:**
- Thời gian: O(b^d) (trường hợp xấu nhất)
- Không gian: O(b·d)

**Hình ảnh (.gif) minh họa thuật toán:**

![DFS Demo](assets/Mazegame_GIF/Uninformed%20Search/DFS.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Breadth-First Search** |  |  |
| **Depth-First Search** |  |  |

---

### **Nhóm 2: Tìm Kiếm Có Thông Tin**

#### **Greedy Best-First Search**

Thuật toán Greedy sử dụng cấu trúc lưu trữ **Priority Queue**. Chọn đường đi có chi phí ước lượng thấp nhất.

**Hàm đánh giá:**
- Sử dụng hàm **h(n)** (Heuristics) để ước lượng chi phí từ vị trí hiện tại đến kho báu
- h(n) được tính dựa trên khoảng cách Manhattan

**Đặc điểm:**
- Muốn tối ưu phải ước lượng chi phí chính xác
- Nếu ước lượng sai có thể tìm ra đường đi không tối ưu

**Hình ảnh (.gif) minh họa thuật toán:**

![Greedy Demo](assets/Mazegame_GIF/Informed%20Search/Greedy.gif)

---

#### **A\* Search**

Thuật toán A* sử dụng cấu trúc lưu trữ **Priority Queue**. Chọn hướng đi có chi phí thấp nhất.

**Hàm đánh giá:**
```
f(n) = g(n) + h(n)
```
Trong đó:
- **f(n)**: Tổng chi phí
- **g(n)**: Chi phí từ vị trí xuất phát đến vị trí hiện tại (Path Cost)
- **h(n)**: Ước lượng chi phí từ vị trí hiện tại đến kho báu (Heuristics)

**Hình ảnh (.gif) minh họa thuật toán:**

![A* Demo](assets/Mazegame_GIF/Informed%20Search/Astar.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Greedy Best-First Search** |  |  |
| **A\* Search** |  |  |

---

### **Nhóm 3: Tìm Kiếm Local Search**

#### **Simulated Annealing**

Thuật toán **Simulated Annealing (SA)** là phương pháp tìm kiếm ngẫu nhiên được lấy cảm hứng từ quá trình tôi luyện kim loại (annealing) trong vật lý.

**Nguyên lý:**
- Khi nung nóng kim loại rồi làm nguội dần, các nguyên tử có xu hướng sắp xếp lại để đạt được cấu trúc năng lượng thấp nhất
- Trong bài toán này, SA được sử dụng để tìm đường đi từ vị trí xuất phát đến kho báu trên bản đồ mê cung

**Hình ảnh (.gif) minh họa thuật toán:**

![SA Demo](assets/Mazegame_GIF/Local%20Search/SA.gif)

---

#### **Genetic Algorithm**

Giải thuật di truyền được thực hiện qua các bước chính:
1. **Khởi tạo quần thể**
2. **Chọn lọc** các cá thể phù hợp
3. **Lai ghép** các cặp cá thể
4. **Đột biến** cá thể

**Triển khai trong trò chơi:**
- Quần thể có **6 cá thể**
- Các cá thể là mảng lưu vị trí được random ngẫu nhiên hướng đi
- Quá trình lặp: **21 lần**

**Công thức Fitness:**
```
Fitness = √(soHang² + soCot²) - √((goalX - x)² + (goalY - y)²)
```

**Chiến thuật:**
- **Chọn lọc:** 2 cá thể có fitness cao nhất + 1 cá thể random
- **Lai ghép:** Phép lai đồng nhất với tỷ lệ **65%**
- **Đột biến:** Phép đồng nhất với tỷ lệ **5%**

**Hình ảnh (.gif) minh họa thuật toán:**

_Genetic Algorithm đang được phát triển_

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Simulated Annealing** |  |  |
| **Genetic Algorithm** |  |  |

---

### **Nhóm 4: Tìm Kiếm Trong Môi Trường Phức Tạp**

#### **AND-OR Tree Search**

Thuật toán **AND-OR Tree Search** là dạng mở rộng của tìm kiếm theo cây (Tree Search) dùng để giải quyết bài toán có nhiều khả năng hoặc điều kiện rẽ nhánh.

**Đặc điểm:**
- Một số hành động có thể dẫn đến nhiều trạng thái con (**AND nodes**)
- Từ mỗi trạng thái có thể có nhiều lựa chọn hành động khác nhau (**OR nodes**)
- Mỗi ô là một trạng thái
- Việc di chuyển đến các ô kề là các hành động khả thi

**Hình ảnh (.gif) minh họa thuật toán:**

![AND-OR Demo](assets/Mazegame_GIF/Complex%20Environment/Nondeter.gif)

---

#### **Tìm Kiếm Trong Môi Trường Nhìn Thấy Một Phần**

Thuật toán này có thể được sử dụng với các nhóm thuật toán tìm kiếm có thông tin và không có thông tin. Trong chương trình sử dụng với thuật toán **Greedy**.

**Cách hoạt động:**
- Giống như trong bản đồ kho báu biết trước được một vị trí có thể tìm đến kho báu
- Vị trí được biết sẽ tìm đến được mục tiêu là vị trí giả sử **(1, 3)**
- Ban đầu thuật toán xây dựng các niềm tin ban đầu dùng Greedy để tìm đường đi đến vị trí đó
- Khi tìm thấy, thuật toán sẽ bắt đầu tìm đường đến kho báu

**Ưu điểm:**
- Loại bỏ được các đường đi vô nghĩa
- Tối ưu hơn thuật toán tìm kiếm trong môi trường không nhìn thấy

**Hình ảnh (.gif) minh họa thuật toán:**

![Partially Observable Demo](assets/Mazegame_GIF/Complex%20Environment/PartialObser.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **AND-OR Tree** |  |  |
| **Partially Observable** |  |  |

---

### **Nhóm 5: Tìm Kiếm Thỏa Mãn Ràng Buộc**

#### **CSP Backtracking**

Thuật toán **CSP Backtracking** (Constraint Satisfaction Problem) được sử dụng để giải bài toán tìm đường trong mê cung dựa trên việc thỏa mãn các ràng buộc giữa các biến (các ô của bản đồ).

**Nguyên tắc hoạt động:**
- **Thử - sai** (trial and error)
- Kiểm tra tính hợp lệ (consistency)
- Loại bỏ các đường đi không thỏa mãn trước khi tiếp tục mở rộng tìm kiếm

**Hình ảnh (.gif) minh họa thuật toán:**

![Backtracking Demo](assets/Mazegame_GIF/Constraint%20Satisfied/Backtracking.gif)

---

#### **Arc Consistency (AC3)**

Thuật toán **AC3** có thể được coi là phiên bản tốt hơn của Backtracking.

**Ưu điểm:**
- Trước khi đưa vào backtracking, thuật toán sẽ giới hạn các miền giá trị
- Làm tăng khả năng tìm thấy kho báu nhanh hơn

**Hình ảnh (.gif) minh họa thuật toán:**

![AC3 Demo](assets/Mazegame_GIF/Constraint%20Satisfied/AC3.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **CSP Backtracking** |  |  |
| **AC3** |  |  |

---

### **Nhóm 6: Tìm Kiếm Đối Kháng**

#### **Minimax**

Thuật toán **MiniMax** là kỹ thuật tìm kiếm thường được áp dụng trong các trò chơi đối kháng (như cờ vua, cờ caro, hoặc bài toán đường đi có chướng ngại).

**Nguyên lý hoạt động:**
- **Người chơi (MAX):** Cố gắng tối đa hóa điểm số (giá trị heuristic)
- **Đối thủ (MIN):** Cố gắng tối thiểu hóa điểm số (làm cho người chơi thua)
- MiniMax duyệt qua toàn bộ cây trạng thái đến độ sâu xác định (depth)
- Đánh giá nước đi nào mang lại kết quả tốt nhất trong tình huống xấu nhất

**Trong bài toán tìm kho báu:**
- **Người chơi là MAX:** Muốn đi gần đến kho báu
- **Môi trường (đối thủ) là MIN:** Khiến người chơi đi xa hơn hoặc bị kẹt

**Hình ảnh (.gif) minh họa thuật toán:**

![Minimax Demo](assets/Mazegame_GIF/Game%20Theory/Minimax.gif)

---

#### **Alpha-Beta Pruning**

Thuật toán **Alpha-Beta** là phiên bản tối ưu hơn của Minimax.

**Cách hoạt động:**
- Thay vì thử hết đường, Alpha-Beta chỉ chọn những đường đảm bảo ngưỡng giá trị **alpha** và **beta**
- Nếu lối đi nào vượt quá thì thuật toán sẽ không xét

**Ưu điểm:**
- Cắt tỉa bớt các trường hợp không hợp lệ
- Chạy nhanh và hiệu quả hơn thuật toán Minimax

**Hình ảnh (.gif) minh họa thuật toán:**

_Alpha-Beta Pruning đang được phát triển_

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Minimax** |  |  |
| **Alpha-Beta Pruning** |  |  |

---

## Cài Đặt và Chạy Chương Trình

### **Yêu cầu hệ thống**
- Python 3.8 trở lên
- Pygame
- Matplotlib
- Pillow (PIL)
- Tkinter

### **Cài đặt thư viện**

```bash
pip install pygame matplotlib pillow
```

### **Chạy chương trình**

```bash
cd maze-game
python main.py
```

---

## Cấu Trúc Dự Án

```
maze-game/
├── main.py                      # File chính để chạy game
├── title_screen.py              # Màn hình tiêu đề
├── MapSelectionScreen.py        # Màn hình chọn map
├── algorithms/                  # Thư mục chứa các thuật toán
│   ├── bfs.py                  # Breadth-First Search
│   ├── dfs.py                  # Depth-First Search
│   ├── astar.py                # A* Search
│   ├── gbf.py                  # Greedy Best-First
│   ├── ucs.py                  # Uniform Cost Search
│   ├── sa.py                   # Simulated Annealing
│   ├── hillclimbing.py         # Hill Climbing
│   ├── beam.py                 # Beam Search
│   ├── and_or_search.py        # AND-OR Tree Search
│   ├── partial_observable.py   # Partially Observable
│   ├── unobservable.py         # Unobservable Search
│   ├── backtracking.py         # CSP Backtracking
│   ├── forward_checking.py     # Forward Checking
│   ├── AC3.py                  # Arc Consistency 3
│   ├── minimax.py              # Minimax Algorithm
│   └── heuristic.py            # Heuristic functions
├── core/                        # Core game logic
│   ├── maze_generator.py       # Sinh bản đồ
│   └── path_finding.py         # Xử lý đường đi
├── ui/                          # Giao diện người dùng
│   ├── game.py                 # Game logic chính
│   └── renderer.py             # Render đồ họa
├── utils/                       # Utilities
│   └── algorithm_runner.py     # Chạy thuật toán
└── assets/                      # Tài nguyên
    ├── fonts/                  # Font chữ
    └── pics/                   # Hình ảnh
```

---

## Hướng Dẫn Sử Dụng

1. **Chọn thuật toán** từ danh sách bên trái
2. **Tùy chỉnh bản đồ:**
   - Generate New Maze: Tạo mê cung mới
   - Beautiful Maze: Tạo mê cung đẹp hơn
   - Set Start/End: Đặt điểm bắt đầu/kết thúc
3. **Chạy thuật toán:** Nhấn nút "Run"
4. **Xem kết quả:** Quan sát đường đi, thời gian và số bước
5. **So sánh:** Chạy nhiều thuật toán và xem biểu đồ so sánh

---

## Kết Luận

<!-- Phần kết luận sẽ được cập nhật sau khi có đủ dữ liệu đánh giá -->

---

## Đóng Góp

Dự án được phát triển bởi:
- **Lương Quang Lâm** - 23110121
- **Nguyễn Trường Minh** - 23110125
- **Nguyễn Lê Đức Tuệ** - 23110165

Dưới sự hướng dẫn của: **TS. Phan Thị Huyền Trang**

---

**© 2025 - MAZE**
