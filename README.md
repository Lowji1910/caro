# 🎮 Ranked Arena - Game Tic-Tac-Toe & Caro

Game **Tic-Tac-Toe (3x3)** và **Caro (15x20)** thời gian thực với hệ thống xếp hạng đầy đủ, matchmaking tự động và AI thông minh.

[![GitHub](https://img.shields.io/badge/GitHub-Lowji1910%2Fcaro-blue)](https://github.com/Lowji1910/caro)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Tính Năng Nổi Bật

### 🏆 Hệ Thống Xếp Hạng Đầy Đủ

- **500 cấp độ (Level 1-500)** với hệ thống XP progression:
  - Level 1-100: 100 XP/level
  - Level 101-200: 200 XP/level  
  - Level 201-300: 500 XP/level
  - Level 301-400: 1000 XP/level
  - Level 401-500: 2000 XP/level
- **10 Danh Hiệu (Tier)** từ Tân Thủ đến Chí Tôn (mỗi tier 50 level)
- **4 Hạng (Rank)** cạnh tranh: Bronze, Silver, Gold, Crystal
- Hệ thống điểm kép:
  - **XP** (Kinh nghiệm): Lên cấp độ (Level) - **luôn tăng**
  - **Rank Points** (Điểm xếp hạng): Tăng/Giảm hạng - **có thể giảm**
- Bảng xếp hạng realtime với tier badge màu sắc đẹp mắt
- Thanh tiến trình (Progress Bar) cho cả Level và Rank

### 🎯 Chế Độ Chơi

- **Ranked Mode**: Đấu xếp hạng với người chơi thật qua matchmaking tự động
- **Practice Mode**: Luyện tập với AI (3 độ khó: Easy, Medium, Hard)
- **Matchmaking Tự Động**: Ghép cặp đối thủ realtime qua Socket.IO
- **Replay System**: Xem lại trận đấu với dữ liệu moves từ database
- **In-Game Chat**: Trò chuyện realtime trong trận đấu (tối đa 200 ký tự)

### 🤖 AI Thông Minh

- Thuật toán **Minimax** với **Alpha-Beta Pruning**
- Đánh giá vị trí thông minh: Phòng thủ & tấn công
- Caro AI: Phát hiện nước 3, 4 liên tiếp và chặn đứng
- **3 độ khó**:
  - **Easy**: depth 1-2 (dễ thắng)
  - **Medium**: depth 3 (thử thách)
  - **Hard**: depth 4-5 (rất khó)

### 🎨 Giao Diện Hiện Đại

- **Responsive Design** - Chơi được trên mobile, tablet, desktop
- **Glassmorphism Effect** với gradient background
- Animation mượt mà với **Tailwind CSS 4**
- **Avatar System** - Upload avatar qua URL
- **Drag-to-Pan**: Kéo để di chuyển bàn cờ Caro (Desktop & Touch)
- Typography chuyên nghiệp

### 💬 Tính Năng Nổi Bật Khác

- ✅ **Real-time Multiplayer** qua Socket.IO
- ✅ **Live Chat** trong trận đấu với HTML escape (bảo mật)
- ✅ **Auto-Forfeit**: Rời trận = thua ngay (có modal xác nhận)
- ✅ **Profile cá nhân** với thống kê chi tiết
- ✅ **Match History** với replay đầy đủ
- ✅ **Timeout Detection** (30s/nước đi trong Ranked)
- ✅ **Undo Request** - Xin đi lại trong ranked mode (cần đối thủ đồng ý)
- ✅ **Public Profile** - Xem profile người chơi khác
- ✅ **Header thông minh** - Hiển thị Level, Rank, Tier, Points, Avatar
- ✅ **Progress Bar** - Tiến độ Level và Rank ngay trên Header

---

## 🛠️ Công Nghệ Sử Dụng

### Frontend

| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| **React** | 19.2.0 | UI framework |
| **TypeScript** | 5.8.2 | Type safety |
| **Tailwind CSS** | 4.1.17 | Styling framework |
| **Vite** | 6.2.0 | Build tool & dev server |
| **Socket.IO Client** | 4.8.1 | Real-time communication |
| **Lucide React** | 0.554.0 | Icon library |

### Backend

| Công nghệ | Phiên bản | Mô tả |
|-----------|-----------|-------|
| **Python** | 3.8+ | Server language |
| **Flask** | 3.0.0 | Web framework |
| **Flask-SocketIO** | 5.3.6 | WebSocket support |
| **Flask-CORS** | 4.0.0 | CORS handling |
| **MySQL** | 8.0+ | Relational database |
| **mysql-connector-python** | 8.2.0 | MySQL driver |
| **Werkzeug** | - | Password hashing (scrypt) |
| **eventlet** | 0.33.3 | Async server |
| **python-dotenv** | 1.0.0 | Environment variables |

### Database Schema

```
tic_tac_toe_db
├── users              - Thông tin người dùng
├── ranks              - 4 Hạng (Bronze → Crystal) theo rank_points
├── game_levels        - 500 Level với XP progression
├── tiers              - 10 Danh hiệu theo user_level
├── match_history      - Lịch sử trận đấu với moves JSON
└── user_levels_history - Lịch sử lên cấp
```

---

## 📦 Cài Đặt & Chạy Thử

### 1️⃣ Yêu Cầu Hệ Thống

- ✅ **Python 3.8+** ([Download](https://www.python.org/downloads/))
- ✅ **Node.js 16+** ([Download](https://nodejs.org/))
- ✅ **MySQL/MariaDB** (XAMPP hoặc MySQL Workbench)
- ✅ **Git** ([Download](https://git-scm.com/))

### 2️⃣ Clone Repository

```bash
git clone https://github.com/Lowji1910/caro.git
cd caro
```

### 3️⃣ Setup Database

1. Mở **XAMPP** và start **Apache** + **MySQL**
2. Truy cập **phpMyAdmin** (`http://localhost/phpmyadmin`)
3. Tạo database mới tên `tic_tac_toe_db`
4. Import file `backend/database/tic_tac_toe_db.sql`

> Database sẽ có:
> - ✅ 500 game levels (Level 1-500)
> - ✅ 10 tiers (Tân Thủ → Chí Tôn)
> - ✅ 4 ranks (Bronze, Silver, Gold, Crystal)
> - ✅ 2 user mẫu (player1, player2)

### 4️⃣ Setup Backend

```bash
cd backend

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env (tùy chọn, có thể bỏ qua nếu dùng localhost)
# DB_USER=root
# DB_PASSWORD=
# DB_HOST=localhost
# DB_NAME=tic_tac_toe_db
# SECRET_KEY=your_secret_key
# FRONTEND_ORIGIN=*

# Chạy server
python app.py
```

✅ Backend chạy tại: **http://localhost:5000**

### 5️⃣ Setup Frontend

```bash
# Về thư mục gốc
cd ..

# Cài đặt dependencies
npm install

# Tạo file .env (tùy chọn)
# VITE_BACKEND_URL=http://localhost:5000

# Chạy dev server
npm run dev
```

✅ Frontend chạy tại: **http://localhost:5173** (hoặc 3000 tùy cấu hình)

### 6️⃣ Chơi Thử!

1. Mở trình duyệt vào `http://localhost:5173`
2. **Sign up** tài khoản mới hoặc login với user mẫu:
   - Username: `player1` / Password: `scrypt:32768:8:1$fakehashedpassword1`
   - Username: `player2` / Password: `scrypt:32768:8:1$fakehashedpassword2`
3. Chọn chế độ chơi và bắt đầu!

---

## 📁 Cấu Trúc Thư Mục

```
caro/
├── backend/
│   ├── app.py                      # Flask + SocketIO server chính
│   ├── config.py                   # Cấu hình (DB, game, ranking)
│   ├── requirements.txt            # Python dependencies
│   ├── migrate_passwords.py        # Script migration password
│   │
│   ├── database/
│   │   ├── db.py                   # MySQL connection & query utilities
│   │   └── tic_tac_toe_db.sql      # Database schema với 500 levels + 10 tiers
│   │
│   ├── game/
│   │   ├── engine.py               # Game logic (check winner, valid move)
│   │   └── ai.py                   # Minimax AI với alpha-beta pruning
│   │
│   ├── routes/
│   │   ├── auth.py                 # Login, Signup endpoints
│   │   ├── user.py                 # User profile, update, match history
│   │   └── leaderboard.py          # Leaderboard API
│   │
│   ├── services/
│   │   ├── user_service.py         # User authentication, profile
│   │   ├── match_service.py        # Save match, get history
│   │   ├── rank_service.py         # Update rank, calculate level
│   │   └── leaderboard_service.py  # Get top players
│   │
│   ├── sockets/
│   │   ├── state.py                # Shared state (games, queues, SID mapping)
│   │   ├── matchmaking.py          # Matchmaking socket handlers
│   │   └── game.py                 # Game socket handlers (move, undo, timeout, chat)
│   │
│   ├── migrations/                 # SQL migration files
│   └── tests/                      # Unit tests
│
├── components/                     # React components
│   ├── Button.tsx                  # Reusable button component
│   ├── GameBoard.tsx               # Bàn cờ chính (Tic-Tac-Toe & Caro)
│   ├── ReplayBoard.tsx             # Replay viewer với controls
│   ├── Header.tsx                  # Header với progress bar, avatar
│   ├── Profile.tsx                 # Trang profile + match history
│   ├── Login.tsx                   # Form đăng nhập
│   ├── Signup.tsx                  # Form đăng ký
│   ├── RankInfoModal.tsx           # Modal hiển thị thông tin rank
│   ├── PracticeDifficultySelector.tsx  # Chọn độ khó AI
│   ├── ChatBox.tsx                 # In-game chat component
│   └── LevelSelector.tsx           # Level selector component
│
├── utils/
│   ├── tierUtils.ts                # Tier calculation utilities
│   └── levelUtils.ts               # Level & Rank progress utilities
│
├── App.tsx                         # Main App component
├── index.tsx                       # React entry point
├── types.ts                        # TypeScript type definitions
├── constants.ts                    # Game config, colors, gradients
├── vite.config.ts                  # Vite configuration
├── package.json                    # NPM dependencies
├── tsconfig.json                   # TypeScript config
├── index.html                      # HTML entry point
└── README.md                       # File này
```

---

## 🎮 Hướng Dẫn Chơi Chi Tiết

### 🎯 Tic-Tac-Toe (3x3)

#### Luật Chơi Cơ Bản

- Bàn cờ **3x3** (9 ô vuông)
- Hai người chơi lần lượt đánh dấu **X** (người chơi 1) và **O** (người chơi 2)
- **Mục tiêu**: Xếp **3 ký hiệu liên tiếp** theo hàng ngang, dọc hoặc chéo
- **Hòa**: Khi hết ô mà không ai thắng

#### Chiến Thuật

1. **Chiếm trung tâm**: Ô giữa (2,2) là vị trí mạnh nhất
2. **Tạo nhánh đôi**: Tạo 2 đường thắng cùng lúc để đối thủ không thể chặn
3. **Phòng thủ**: Luôn chặn đối thủ khi họ có 2 ô liên tiếp
4. **Góc mạnh hơn cạnh**: Ưu tiên chiếm 4 góc trước khi chiếm cạnh

#### Thời Gian

- **Ranked Mode**: 30 giây/nước đi
- **Practice Mode**: Không giới hạn thời gian
- **Timeout**: Nếu hết giờ, đối thủ có thể claim thắng

### 🎲 Caro / Gomoku (15x20)

#### Luật Chơi Cơ Bản

- Bàn cờ **15 hàng x 20 cột** (300 ô)
- Hai người chơi lần lượt đặt quân **X** và **O**
- **Mục tiêu**: Xếp **5 quân liên tiếp** theo hàng ngang, dọc hoặc chéo
- Không giới hạn số nước đi
- Không có hòa (trừ khi hết bàn cờ - rất hiếm)

#### Chiến Thuật Nâng Cao

##### 1. Các Hình Thế Cơ Bản

- **Nước 2**: 2 quân liên tiếp (`X X _ _`)
- **Nước 3**: 3 quân liên tiếp (`X X X _ _`)
  - **Nước 3 chết**: Bị chặn 1 đầu (`O X X X _`)
  - **Nước 3 sống**: Cả 2 đầu đều trống (`_ X X X _`)
- **Nước 4**: 4 quân liên tiếp
  - **Nước 4 chết**: Bị chặn 1 đầu (`O X X X X _`)
  - **Nước 4 sống**: Cả 2 đầu trống (`_ X X X X _`) → **BẮT BUỘC PHẢI CHẶN**

##### 2. Kỹ Thuật Tấn Công

- **Tạo nước 3 sống**: Ép đối thủ phải chặn
- **Tạo nhánh đôi**: Tạo 2 nước 3 cùng lúc → Thắng chắc chắn
- **Tạo nước 4 sống**: Đối thủ không thể chặn được

##### 3. Kỹ Thuật Phòng Thủ

- **Ưu tiên chặn nước 4**: Nước 4 sống = thua ngay
- **Chặn nước 3 sống**: Tránh để đối thủ tạo nhánh đôi
- **Phản công**: Vừa chặn vừa tạo nước 3 của mình

##### 4. Chiến Lược Tổng Thể

- **Mở đầu**: Chiếm trung tâm bàn cờ (gần ô 8,10)
- **Giữa trận**: Tạo nhiều nước 2, nước 3 để tăng áp lực
- **Kết thúc**: Tìm cơ hội tạo nhánh đôi hoặc nước 4 sống

#### Thời Gian

- **Ranked Mode**: 30 giây/nước đi
- **Practice Mode**: Không giới hạn
- **Timeout**: Claim thắng nếu đối thủ hết giờ

### 🎮 Các Chế Độ Chơi

#### 🏆 Ranked Mode (Trận Đấu Xếp Hạng)

- **Đối thủ**: Người chơi thật qua matchmaking tự động
- **Tính điểm**: 
  - **Thắng**: +50 XP, +25 Rank Points
  - **Thua**: +15 XP, -10 Rank Points
- **Tính năng**:
  - ⏱️ Giới hạn thời gian **30s/nước**
  - 🔄 **Undo Request** (xin đi lại, cần đối thủ đồng ý)
  - ⚠️ **Timeout Detection** (claim thắng nếu đối thủ hết giờ)
  - 💬 **Live Chat** (trò chuyện trong trận, max 200 ký tự)
  - 🚪 **Leave Game** (rời trận = thua ngay lập tức, có modal xác nhận)
- **Lưu lịch sử**: Tất cả trận đấu được lưu vào database
- **Replay**: Có thể xem lại sau này

#### 🤖 Practice Mode (Luyện Tập)

- **Đối thủ**: AI thông minh với 3 độ khó
  - **Easy**: Minimax depth 1-2 (dễ thắng)
  - **Medium**: Minimax depth 3 (thử thách)
  - **Hard**: Minimax depth 4-5 (rất khó)
- **Không tính điểm**: Không ảnh hưởng rank
- **Không giới hạn thời gian**: Suy nghĩ thoải mái
- **Không lưu lịch sử**: Chỉ để luyện tập

### 🕹️ Điều Khiển

- **Click chuột trái**: Đặt quân vào ô trống
- **Nút "Undo"**: Xin đi lại (chỉ ranked, cần đối thủ đồng ý)
- **Nút "Leave Game"**: Rời trận (sẽ có modal xác nhận nếu game đang chơi)
- **Chat Box**: Nhập tin nhắn và Enter để gửi (max 200 ký tự)
- **Drag-to-Pan** (Caro): Nhấn giữ và kéo để di chuyển bàn cờ
- **Replay Controls**:
  - ◀ **Previous**: Lùi 1 nước
  - ▶ **Next**: Tiến 1 nước
  - ⏮ **First**: Về nước đầu tiên
  - ⏭ **Last**: Đến nước cuối cùng

---

## 🏅 Hệ Thống Xếp Hạng Chi Tiết

### 📊 Cách Tính Điểm

#### Điểm Kinh Nghiệm (XP) - Chỉ Tăng, Không Giảm

- **Thắng Ranked**: +50 XP
- **Thua Ranked**: +15 XP
- **Practice Mode**: Không tính điểm
- **Leave Game giữa chừng**: Tính thua (+15 XP)

#### Điểm Xếp Hạng (Rank Points) - Có Thể Tăng/Giảm

- **Thắng Ranked**: +25 Rank Points
- **Thua Ranked**: -10 Rank Points
- **Practice Mode**: Không tính điểm
- **Leave Game giữa chừng**: Tính thua (-10 Rank Points)

#### Lên Cấp (Level Up)

- Công thức: **Level** dựa vào **XP** tích lũy
- Chi tiết xem bảng dưới

### 🎖️ Bảng Level Chi Tiết

| Nhóm Level | Level Range | XP/Level | XP Cần Tích Lũy |
|------------|-------------|----------|-----------------|
| Nhóm 1 | 1-100 | 100 | 0 - 9,900 |
| Nhóm 2 | 101-200 | 200 | 10,000 - 29,900 |
| Nhóm 3 | 201-300 | 500 | 30,000 - 79,900 |
| Nhóm 4 | 301-400 | 1,000 | 80,000 - 179,900 |
| Nhóm 5 | 401-500 | 2,000 | 180,000 - 379,900 |

#### Ví Dụ Cụ Thể

- **Level 1**: 0 XP
- **Level 2**: 100 XP
- **Level 50**: 4,900 XP
- **Level 100**: 9,900 XP
- **Level 101**: 10,000 XP
- **Level 200**: 29,900 XP
- **Level 500**: 379,900 XP

### 🎖️ 10 Danh Hiệu (Tier) - Theo Level

| Tier | Tên | Level | Màu | Icon | Mô Tả Chi Tiết |
|------|-----|-------|-----|------|----------------|
| I | **Tân Thủ** | 1-50 | `#9E9E9E` Xám | 🆕 | Người mới bắt đầu, đang làm quen với luật chơi |
| II | **Nhập Môn** | 51-100 | `#4CAF50` Xanh lá | 🌱 | Đã nắm vững luật chơi, hiểu chiến thuật cơ bản |
| III | **Xuất Sắc** | 101-150 | `#2196F3` Xanh dương | 💎 | Người chơi có kinh nghiệm, biết phòng thủ và tấn công |
| IV | **Tinh Anh** | 151-200 | `#9C27B0` Tím | 💜 | Bắt đầu hiểu sâu về chiến thuật, tạo nhánh đôi |
| V | **Cao Thủ** | 201-250 | `#F44336` Đỏ | ❤️ | Thành thạo kỹ thuật, biết đọc nước đi của đối thủ |
| VI | **Danh Thủ** | 251-300 | `#FF9800` Cam | 🧡 | Bậc thầy chiến thuật, ít khi mắc lỗi |
| VII | **Đại Sư** | 301-350 | `#FFD700` Vàng | 👑 | Đẳng cấp cao thủ, thống trị bảng xếp hạng |
| VIII | **Tông Sư** | 351-400 | `#E91E63` Hồng | ⚡ | Kẻ mạnh nhất server, rất khó đánh bại |
| IX | **Huyền Thoại** | 401-450 | `#00BCD4` Cyan | 🌟 | Huyền thoại bất bại, chỉ có 1-2 người đạt được |
| X | **Chí Tôn** | 451-500 | `#000000` Đen | ⚔️ | Vượt qua mọi giới hạn, đỉnh cao tuyệt đối |

### 🎖️ 4 Hạng Cạnh Tranh (Rank) - Theo Rank Points

| Rank | Tên | Điểm Rank | Màu | Icon | Mô Tả |
|------|-----|-----------|-----|------|-------|
| I | **Bronze** | 0-499 | `#CD7F32` Đồng | 🥉 | Hạng mới - Người chơi đang phát triển |
| II | **Silver** | 500-999 | `#C0C0C0` Bạc | 🥈 | Hạng trung bình - Đang phát triển kỹ năng |
| III | **Gold** | 1,000-1,999 | `#FFD700` Vàng | 🥇 | Hạng cao - Người chơi mạnh |
| IV | **Crystal** | 2,000+ | `#00BCD4` Pha lê | 💎 | Hạng cao nhất - Người chơi chuyên nghiệp |

### 📈 Progression System

#### Hiển Thị Trên UI

- **Level Number**: Số level hiện tại (1-500)
- **Tier Badge**: Huy hiệu màu sắc với tên danh hiệu
- **Rank Badge**: Huy hiệu hạng (Bronze/Silver/Gold/Crystal)
- **Progress Bar (Level)**: Thanh tiến trình đến level tiếp theo
- **Progress Bar (Rank)**: Thanh tiến trình đến hạng tiếp theo  
- **XP Display**: `1250 / 1300 XP` (XP hiện tại / XP cần cho level tiếp theo)
- **Points Display**: `850 pts` (Rank Points hiện tại)

#### Ví Dụ Cụ Thể

**Player: admin**
- **Level**: 127 (Tier: **Xuất Sắc**)
- **XP**: 12,650 / 12,700 (còn 50 XP nữa lên Level 128)
- **Rank**: Gold (990 Rank Points)
- **Rank Progress**: 990/1000 (còn 10 pts nữa lên Crystal)

#### Leaderboard

- Hiển thị **Top 100 players** theo `rank_points`
- Sắp xếp: **Cao → Thấp**
- Thông tin: **Rank Badge**, Display Name, **Tier Badge**, Level, Points
- **Real-time update** sau mỗi trận đấu

### 🎯 Mốc Progression

| Mốc | Level | Danh hiệu | Thành Tựu |
|-----|-------|-----------|-----------|
| 🎯 | 50 | Tân Thủ → Nhập Môn | Hoàn thành giai đoạn tập sự |
| 🎯 | 100 | Nhập Môn → Xuất Sắc | Trở thành người chơi có kinh nghiệm |
| 🎯 | 200 | Tinh Anh → Cao Thủ | Bước vào hàng ngũ cao thủ |
| 🎯 | 300 | Danh Thủ → Đại Sư | Top player của server |
| 🎯 | 400 | Tông Sư → Huyền Thoại | Huyền thoại sống |
| 🎯 | 500 | Chí Tôn | Đỉnh cao tuyệt đối |

### 💡 Tips Tăng Rank Nhanh

1. **Chơi nhiều Ranked**: Practice không tính điểm
2. **Học chiến thuật**: Xem replay của người chơi giỏi
3. **Tránh timeout**: Luôn chú ý đồng hồ đếm ngược
4. **Không leave game**: Rời giữa chừng = thua + mất điểm
5. **Luyện với AI Hard**: Cải thiện kỹ năng trước khi ranked
6. **Phân tích lỗi**: Xem lại replay để học từ sai lầm

---

## 🔧 API Endpoints

### Authentication

- `POST /api/login` - Đăng nhập
  - Body: `{ username, password }`
  - Response: User object với full profile
  
- `POST /api/signup` - Đăng ký
  - Body: `{ username, password, display_name, email }`
  - Response: User object với full profile

### User

- `GET /api/user/:id` - Lấy thông tin user (với rank, tier info)
- `PUT /api/profile/:id` - Cập nhật profile
  - Body: `{ display_name?, full_name?, avatar_url?, bio?, date_of_birth? }`
- `GET /api/public/:id` - Lấy public profile (cho public view)
- `POST /api/change-password/:id` - Đổi mật khẩu
  - Body: `{ oldPassword, newPassword }`

### Leaderboard

- `GET /api/leaderboard` - Top 100 players theo rank_score
  - Response: Array of user objects (rank_score, level, tier_name, tier_color)

### Match

- `GET /api/history/:userId` - Lấy match history của user
- `GET /api/match/:matchId` - Lấy chi tiết trận đấu (cho replay)
  - Response: Match với moves JSON

---

## 🔌 Socket.IO Events

### Client → Server

- `join_matchmaking` - Tham gia matchmaking
  - Data: `{ userId, type, mode, difficulty? }`
  
- `make_move` - Thực hiện nước đi
  - Data: `{ roomId, r, c, player }`
  
- `send_chat` - Gửi tin nhắn chat
  - Data: `{ roomId, message, sender, senderId }`
  
- `request_undo` - Xin đi lại
  - Data: `{ roomId }`
  
- `resolve_undo` - Phản hồi yêu cầu undo
  - Data: `{ roomId, accept: boolean }`
  
- `claim_timeout` - Claim thắng do timeout
  - Data: `{ roomId }`
  
- `leave_game` - Rời trận đấu
  - Data: `{ roomId }`

### Server → Client

- `match_found` - Tìm thấy trận đấu
  - Data: `{ roomId, opponent, board, gameType, mode, playerNumber, difficulty? }`
  
- `game_update` - Cập nhật trạng thái game
  - Data: `{ board, currentPlayer, winner, winningLine, lastMove }`
  
- `receive_chat` - Nhận tin nhắn chat
  - Data: `{ sender, senderId, message }`
  
- `undo_requested` - Nhận yêu cầu undo từ đối thủ
  
- `undo_declined` - Undo bị từ chối

---

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend (nếu có)
npm run test
```

---

## 🤝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy:

1. **Fork** repo này
2. Tạo branch mới (`git checkout -b feature/TinhNangMoi`)
3. Commit changes (`git commit -m 'Thêm tính năng X'`)
4. Push lên branch (`git push origin feature/TinhNangMoi`)
5. Tạo **Pull Request**

---

## 📝 License

Project này được phát hành dưới giấy phép **MIT**. Xem file `LICENSE` để biết thêm chi tiết.

---

## 👨‍💻 Tác Giả

**Lowji1910**

- GitHub: [@Lowji1910](https://github.com/Lowji1910)
- Project: [Caro Game](https://github.com/Lowji1910/caro)

---

## 🙏 Credits

- **Icons**: [Lucide Icons](https://lucide.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Framework**: [React](https://react.dev/) + [Flask](https://flask.palletsprojects.com/)

---

## 🐛 Known Issues

- ⚠️ Replay có thể bị lỗi nếu moves không được lưu đúng format JSON
- ⚠️ Avatar URL cần validate để tránh broken images
- ⚠️ Timeout detection có thể có race condition trong một số trường hợp
- ⚠️ Game result display có thể hiển thị không chính xác trong một số trường hợp (đang sửa)

---

## 🔮 Roadmap

- [x] Chat trong game
- [x] Auto-forfeit khi leave game
- [x] Replay system
- [x] Drag-to-pan bàn cờ
- [x] Header với progress bar
- [ ] Spectator mode
- [ ] Tournament system
- [ ] Achievement badges
- [ ] Friend system
- [ ] Mobile app (React Native)

---

## ⭐ Nếu bạn thấy project hay, hãy cho 1 star nhé! ⭐

---
