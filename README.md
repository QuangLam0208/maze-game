# MAZE GAME
## Thông Tin Đồ Án

**Báo Cáo Cuối Kỳ - Môn: Trí Tuệ Nhân Tạo**

**GVHD:** TS. Phan Thị Huyền Trang

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

![BFS Demo](assets/BFS.gif)

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

![DFS Demo](assets/DFS.gif)

---

#### **Depth-Limited Search (DLS)**

Thuật toán **DLS** là biến thể của DFS nhưng có giới hạn độ sâu tìm kiếm. Thuật toán chỉ duyệt đến độ sâu tối đa được định trước.

**Đặc điểm:**
- Giải quyết vấn đề duyệt vô hạn của DFS
- Có thể không tìm thấy đường đi nếu goal nằm quá sâu
- Tốn ít không gian hơn BFS
- Phù hợp khi biết trước độ sâu tối ưu

**Độ phức tạp:**
- Thời gian: O(b^l) với l là depth limit
- Không gian: O(b·l)

**Hình ảnh (.gif) minh họa thuật toán:**

![DLS Demo](assets/DLS.gif)

---

#### **Uniform Cost Search (UCS)**

Thuật toán **UCS** là mở rộng của BFS, chọn node có tổng chi phí đường đi thấp nhất từ điểm xuất phát.

**Đặc điểm:**
- Sử dụng Priority Queue theo chi phí thực tế g(n)
- Đảm bảo tìm được đường đi có chi phí thấp nhất
- Tương đương BFS khi tất cả bước đi có chi phí bằng nhau
- Tốn không gian nhiều hơn DFS

**Độ phức tạp:**
- Thời gian: O(b^(C*/ε)) với C* là chi phí tối ưu
- Không gian: O(b^(C*/ε))

**Hình ảnh (.gif) minh họa thuật toán:**

![UCS Demo](assets/UCS.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Breadth-First Search** |  |  |
| **Depth-First Search** |  |  |
| **Depth-Limited Search** |  |  |
| **Uniform Cost Search** |  |  |

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

![Greedy Demo](assets/Greedy.gif)

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

![A* Demo](assets/Astar.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Greedy Best-First Search** |  |  |
| **A\* Search** |  |  |

---

### **Nhóm 3: Tìm Kiếm Cục Bộ**

#### **Simulated Annealing**

Thuật toán **Simulated Annealing (SA)** là phương pháp tìm kiếm ngẫu nhiên được lấy cảm hứng từ quá trình tôi luyện kim loại (annealing) trong vật lý.

**Nguyên lý:**
- Khi nung nóng kim loại rồi làm nguội dần, các nguyên tử có xu hướng sắp xếp lại để đạt được cấu trúc năng lượng thấp nhất
- Trong bài toán này, SA được sử dụng để tìm đường đi từ vị trí xuất phát đến kho báu trên bản đồ mê cung

**Hình ảnh (.gif) minh họa thuật toán:**

![SA Demo](assets/SA.gif)

---

#### **Hill Climbing**

Thuật toán **Hill Climbing** là phương pháp tìm kiếm cục bộ, luôn chọn bước đi tốt nhất về phía mục tiêu.

**Nguyên lý:**
- Chỉ xem xét các trạng thái lân cận
- Chọn neighbor có heuristic tốt nhất
- Dừng khi không còn neighbor nào tốt hơn
- Dễ rơi vào local optimum

**Đặc điểm:**
- Rất nhanh và tiết kiệm bộ nhớ
- Không đảm bảo tìm được lời giải tối ưu
- Có thể bị mắc kẹt tại đỉnh cục bộ
- Phù hợp với bài toán có không gian trạng thái đơn giản

**Hình ảnh (.gif) minh họa thuật toán:**

![Hill Climbing Demo](assets/Hill%20Climbing.gif)

---

#### **Beam Search**

Thuật toán **Beam Search** giữ lại k trạng thái tốt nhất ở mỗi mức, kết hợp ưu điểm của BFS và heuristic search.

**Nguyên lý:**
- Giới hạn số lượng node được mở rộng ở mỗi mức (beam width)
- Chỉ giữ lại k node có heuristic tốt nhất
- Giảm không gian lưu trữ so với BFS thông thường
- Trade-off giữa tính tối ưu và hiệu suất

**Đặc điểm:**
- Hiệu quả về mặt không gian
- Không đảm bảo tìm được lời giải tối ưu
- Beam width nhỏ: nhanh nhưng có thể bỏ lỡ lời giải
- Beam width lớn: chậm hơn nhưng tăng khả năng tìm được lời giải tốt

**Hình ảnh (.gif) minh họa thuật toán:**

![Beam Search Demo](assets/Beam.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Hill Climbing** |  |  |
| **Simulated Annealing** |  |  |
| **Beam Search** |  |  |
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

![AND-OR Demo](assets/Nondeter.gif)

---

#### **Tìm Kiếm Trong Môi Trường Nhìn Thấy Một Phần**

Thuật toán tìm kiếm trong **môi trường quan sát một phần** (Partially Observable Environment), agent chỉ nhìn thấy một phần trạng thái môi trường.

**Cách hoạt động:**
- Agent chỉ quan sát được vùng lân cận
- Xây dựng belief state dựa trên quan sát từng phần
- Sử dụng Greedy để tìm đến vị trí trung gian đã biết trước
- Từ vị trí đó tiếp tục tìm đến goal

**Đặc điểm:**
- Giảm không gian tìm kiếm so với unobservable
- Tối ưu hơn khi biết trước một số vị trí quan trọng
- Cần cân bằng giữa exploration và exploitation

**Hình ảnh (.gif) minh họa thuật toán:**

![Partially Observable Demo](assets/PartialObser.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **AND-OR Tree** |  |  |
| **Partially Observable** |  |  |
| **Unobservable Search** |  |  |

---

### **Nhóm 5: Tìm Kiếm Thỏa Mãn Ràng Buộc**

#### **CSP Backtracking**

Thuật toán **CSP Backtracking** (Constraint Satisfaction Problem) được sử dụng để giải bài toán tìm đường trong mê cung dựa trên việc thỏa mãn các ràng buộc giữa các biến (các ô của bản đồ).

**Nguyên tắc hoạt động:**
- **Thử - sai** (trial and error)
- Kiểm tra tính hợp lệ (consistency)
- Loại bỏ các đường đi không thỏa mãn trước khi tiếp tục mở rộng tìm kiếm

**Hình ảnh (.gif) minh họa thuật toán:**

![Backtracking Demo](assets/Backtracking.gif)

---

#### **Forward Checking**

Thuật toán **Forward Checking** là cải tiến của Backtracking, kiểm tra tính hợp lệ trước khi gán giá trị.

**Nguyên lý:**
- Sau mỗi lần gán biến, kiểm tra domain của các biến chưa gán
- Loại bỏ các giá trị không thỏa mãn ràng buộc với biến vừa gán
- Phát hiện sớm các nhánh không có lời giải
- Giảm số lần backtrack so với Backtracking thuần túy

**Ưu điểm:**
- Hiệu quả hơn Backtracking thông thường
- Phát hiện sớm inconsistency
- Giảm số node cần khám phá

**Hình ảnh (.gif) minh họa thuật toán:**

![Forward Checking Demo](assets/Forward%20Checking.gif)

---

#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Backtracking** |  |  |
| **Forward Checking** |  |  |
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

![Minimax Demo](assets/Minimax.gif)

---



#### **Bảng Đánh Giá Thuật Toán**

| Thuật toán | Thời gian | Số bước đi |
|------------|-----------|------------|
| **Minimax** |  |  |


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
