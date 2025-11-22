# 🎮 Ranked Arena - Tic-Tac-Toe & Caro Game

> Game Tic-Tac-Toe (3x3) và Caro (15x20) thời gian thực với hệ thống xếp hạng, matchmaking tự động và AI thông minh.

[![GitHub](https://img.shields.io/badge/GitHub-Lowji1910%2Fcaro-blue)](https://github.com/Lowji1910/caro)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Tính Năng Nổi Bật

### 🏆 Hệ Thống Xếp Hạng Đầy Đủ
- **100,000 cấp độ** (Level 1-100,000) với hệ thống XP progression
- **10 Tier Ranks** từ Tân Thủ đến Thần Thoại (lưu trong bảng `tiers`)
- Tính điểm Elo: **Thắng +25 XP**, **Thua -10 XP**
- Bảng xếp hạng realtime với tier badge màu sắc đẹp mắt
- Mỗi level cần 100 XP để lên cấp

### 🎯 Chế Độ Chơi
- **Ranked Mode**: Đấu xếp hạng với người chơi thật qua matchmaking tự động
- **Practice Mode**: Luyện tập với AI (3 độ khó: Easy, Medium, Hard)
- **Matchmaking Tự Động**: Ghép cặp đối thủ realtime qua Socket.IO
- **Replay System**: Xem lại trận đấu với dữ liệu moves từ database
- **In-Game Chat**: Trò chuyện realtime trong trận đấu

### 🤖 AI Thông Minh
- **Thuật toán Minimax** với Alpha-Beta Pruning
- **Đánh giá vị trí thông minh**: Phòng thủ & tấn công
- **Caro AI**: Phát hiện nước 3, 4 liên tiếp và chặn đứng
- **3 độ khó**: Easy (depth 1-2), Medium (depth 3), Hard (depth 4-5)

### 🎨 Giao Diện Hiện Đại
- **Responsive Design** - Chơi được trên mobile, tablet, desktop
- **Glassmorphism Effect** với gradient background
- **Animation mượt mà** với Tailwind CSS
- **Avatar System** - Upload avatar qua URL
- **Font Fredoka** - Typography chuyên nghiệp

### 💬 Tính Năng Nổi Bật Khác
- **Real-time Multiplayer** qua Socket.IO
- **Live Chat** trong trận đấu với emoji support
- **Auto-Forfeit**: Rời trận = thua ngay (có modal xác nhận)
- **Profile cá nhân** với thống kê chi tiết
- **Match History** với replay đầy đủ
- **Timeout Detection** (30s/nước đi)
- **Undo Request** - Xin đi lại trong ranked mode
- **Public Profile** - Xem profile người chơi khác

---

## 🛠️ Công Nghệ Sử Dụng

### Frontend
- **React 19.2.0** - UI framework
- **TypeScript 5.8.2** - Type safety
- **Tailwind CSS 4.1.17** - Styling framework
- **Vite 6.2.0** - Build tool & dev server
- **Socket.IO Client 4.8.1** - Real-time communication
- **Lucide React 0.554.0** - Icon library

### Backend
- **Python 3.8+** - Server language
- **Flask 3.0.0** - Web framework
- **Flask-SocketIO 5.3.6** - WebSocket support
- **Flask-CORS 4.0.0** - CORS handling
- **MySQL (MariaDB 10.4.32)** - Relational database
- **mysql-connector-python 8.2.0** - MySQL driver
- **Werkzeug** - Password hashing (scrypt)
- **eventlet 0.33.3** - Async server
- **python-dotenv 1.0.0** - Environment variables

### Database Schema
- **users** - Thông tin người dùng (username, password hash, email, rank_score, user_level, avatar_url)
- **match_history** - Lịch sử trận đấu (player1_id, player2_id, winner_id, game_type, mode, moves JSON)
- **game_levels** - 100,000 level với XP progression (level, required_score, xp_to_next)
- **tiers** - 10 tier ranks (name, color, min_level, max_level, description)

---

## 📦 Cài Đặt & Chạy Thử

### 1️⃣ Yêu Cầu Hệ Thống

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **MySQL/MariaDB** (XAMPP hoặc MySQL Workbench)
- **Git** ([Download](https://git-scm.com/))

### 2️⃣ Clone Repository

```bash
git clone https://github.com/Lowji1910/caro.git
cd caro
```

### 3️⃣ Setup Database

1. Mở **XAMPP** và start **Apache + MySQL**
2. Truy cập **phpMyAdmin** (`http://localhost/phpmyadmin`)
3. Tạo database mới tên `tic_tac_toe_db`
4. Import file `tic_tac_toe_db.sql` (chứa đầy đủ schema + data)

**Database sẽ có:**
- 100,000 game levels (level 1-100,000)
- 10 tiers (Tân Thủ → Thần Thoại)
- 6 user mẫu (admin, test_user, test_p1, test_p2, etc.)
- 16 match history mẫu

### 4️⃣ Setup Backend

```bash
cd backend

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env (tùy chọn)
# DB_USER=root
# DB_PASSWORD=
# DB_HOST=localhost
# DB_NAME=tic_tac_toe_db
# SECRET_KEY=your_secret_key
# FRONTEND_ORIGIN=*

# Chạy migration password (nếu cần)
python migrate_passwords.py

# Chạy server
python app.py
```

**Backend chạy tại:** `http://localhost:5000`

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

**Frontend chạy tại:** `http://localhost:3000`

### 6️⃣ Chơi Thử!

1. Mở trình duyệt vào `http://localhost:3000`
2. **Login** với tài khoản mẫu:
   - Username: `admin` / Password: `admin123`
   - Username: `test_user` / Password: `password123`
3. Hoặc **Sign up** tài khoản mới
4. Chọn chế độ chơi và bắt đầu!

---

## 🚀 Deploy Lên Internet

Xem hướng dẫn chi tiết trong file [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

**Recommended Stack:**
- **Frontend**: Vercel (miễn phí, auto deploy từ GitHub)
- **Backend**: Render (free tier, Python support)
- **Database**: PlanetScale hoặc Railway (MySQL miễn phí)

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
│   │   └── db.py                   # MySQL connection & query utilities
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
│   │   └── game.py                 # Game socket handlers (move, undo, timeout, chat, leave)
│   │
│   ├── migrations/                 # SQL migration files
│   └── tests/                      # Unit tests
│
├── components/                     # React components
│   ├── Button.tsx                  # Reusable button component
│   ├── GameBoard.tsx               # Bàn cờ chính (Tic-Tac-Toe & Caro)
│   ├── ReplayBoard.tsx             # Replay viewer với controls
│   ├── Header.tsx                  # Header với avatar & logout
│   ├── Profile.tsx                 # Trang profile + match history
│   ├── Signup.tsx                  # Form đăng ký
│   ├── RankInfoModal.tsx           # Modal hiển thị thông tin rank
│   ├── PracticeDifficultySelector.tsx  # Chọn độ khó AI
│   ├── ChatBox.tsx                 # In-game chat component
│   └── LevelSelector.tsx           # Level selector component
│
├── utils/
│   └── tierUtils.ts                # Tier calculation utilities
│
├── App.tsx                         # Main App component
├── index.tsx                       # React entry point
├── types.ts                        # TypeScript type definitions
├── constants.ts                    # Game config, colors, gradients
├── vite.config.ts                  # Vite configuration
├── package.json                    # NPM dependencies
├── tsconfig.json                   # TypeScript config
├── index.html                      # HTML entry point
├── tic_tac_toe_db.sql              # Full database dump (100k levels)
├── README.md                       # File này
├── DEPLOY_GUIDE.md                 # Hướng dẫn deploy
└── GITHUB_GUIDE.md                 # Hướng dẫn push lên GitHub
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
- **Chiếm trung tâm**: Ô giữa (2,2) là vị trí mạnh nhất
- **Tạo nhánh đôi**: Tạo 2 đường thắng cùng lúc để đối thủ không thể chặn
- **Phòng thủ**: Luôn chặn đối thủ khi họ có 2 ô liên tiếp
- **Góc mạnh hơn cạnh**: Ưu tiên chiếm 4 góc trước khi chiếm cạnh

#### Thời Gian
- **Ranked Mode**: 30 giây/nước đi
- **Practice Mode**: Không giới hạn thời gian
- **Timeout**: Nếu hết giờ, đối thủ có thể claim thắng

---

### 🎲 Caro / Gomoku (15x20)

#### Luật Chơi Cơ Bản
- Bàn cờ **15 hàng x 20 cột** (300 ô)
- Hai người chơi lần lượt đặt quân **X** và **O**
- **Mục tiêu**: Xếp **5 quân liên tiếp** theo hàng ngang, dọc hoặc chéo
- **Không giới hạn** số nước đi
- **Không có hòa** (trừ khi hết bàn cờ - rất hiếm)

#### Chiến Thuật Nâng Cao

**1. Các Hình Thế Cơ Bản**
- **Nước 2**: 2 quân liên tiếp (X X _ _)
- **Nước 3**: 3 quân liên tiếp (X X X _ _)
  - **Nước 3 chết**: Bị chặn 1 đầu (O X X X _)
  - **Nước 3 sống**: Cả 2 đầu đều trống (_ X X X _)
- **Nước 4**: 4 quân liên tiếp
  - **Nước 4 chết**: Bị chặn 1 đầu (O X X X X _)
  - **Nước 4 sống**: Cả 2 đầu trống (_ X X X X _) → **BẮT BUỘC PHẢI CHẶN**

**2. Kỹ Thuật Tấn Công**
- **Tạo nước 3 sống**: Ép đối thủ phải chặn
- **Tạo nhánh đôi**: Tạo 2 nước 3 cùng lúc → Thắng chắc chắn
- **Tạo nước 4 sống**: Đối thủ không thể chặn được

**3. Kỹ Thuật Phòng Thủ**
- **Ưu tiên chặn nước 4**: Nước 4 sống = thua ngay
- **Chặn nước 3 sống**: Tránh để đối thủ tạo nhánh đôi
- **Phản công**: Vừa chặn vừa tạo nước 3 của mình

**4. Chiến Lược Tổng Thể**
- **Mở đầu**: Chiếm trung tâm bàn cờ (gần ô 8,10)
- **Giữa trận**: Tạo nhiều nước 2, nước 3 để tăng áp lực
- **Kết thúc**: Tìm cơ hội tạo nhánh đôi hoặc nước 4 sống

#### Thời Gian
- **Ranked Mode**: 30 giây/nước đi
- **Practice Mode**: Không giới hạn
- **Timeout**: Claim thắng nếu đối thủ hết giờ

---

### 🎮 Các Chế Độ Chơi

#### 🏆 Ranked Mode (Trận Đấu Xếp Hạng)
- **Đối thủ**: Người chơi thật qua matchmaking tự động
- **Tính điểm**: Thắng +25 XP, Thua -10 XP
- **Tính năng**:
  - ⏱️ Giới hạn thời gian 30s/nước
  - 🔄 Undo Request (xin đi lại, cần đối thủ đồng ý)
  - ⚠️ Timeout Detection (claim thắng nếu đối thủ hết giờ)
  - 💬 Live Chat (trò chuyện trong trận, max 200 ký tự)
  - 🚪 Leave Game (rời trận = thua ngay lập tức, có modal xác nhận)
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

---

### 🕹️ Điều Khiển

- **Click chuột trái**: Đặt quân vào ô trống
- **Nút "Undo"**: Xin đi lại (chỉ ranked, cần đối thủ đồng ý)
- **Nút "Leave Game"**: Rời trận (sẽ có modal xác nhận nếu game đang chơi)
- **Chat Box**: Nhập tin nhắn và Enter để gửi (max 200 ký tự)
- **Replay Controls**:
  - ◀ **Previous**: Lùi 1 nước
  - ▶ **Next**: Tiến 1 nước
  - ⏮ **First**: Về nước đầu tiên
  - ⏭ **Last**: Đến nước cuối cùng

---

## 🏅 Hệ Thống Xếp Hạng Chi Tiết

### 📊 Cách Tính Điểm

#### Điểm Kinh Nghiệm (XP)
- **Thắng Ranked**: +25 XP
- **Thua Ranked**: -10 XP
- **Practice Mode**: Không tính điểm
- **Leave Game giữa chừng**: Tính thua (-10 XP)

#### Lên Cấp (Level Up)
- Mỗi level cần **100 XP**
- Công thức: `Level = floor(Total XP / 100) + 1`
- Ví dụ:
  - 0-99 XP → Level 1
  - 100-199 XP → Level 2
  - 1000-1099 XP → Level 11

#### Hệ Thống Tier (Cấp Bậc)
- Dựa trên **Level**, không phải XP
- Có **10 Tier** từ Tân Thủ đến Thần Thoại
- Mỗi Tier có màu sắc và biểu tượng riêng

---

### 🎖️ Bảng Tier Chi Tiết

| Tier | Tên | Level | Màu | Icon | Mô Tả Chi Tiết |
|------|-----|-------|-----|------|----------------|
| **I** | **Tân Thủ** | 1-50 | ![#9E9E9E](https://via.placeholder.com/15/9E9E9E/000000?text=+) Xám | 🆕 | Người mới bắt đầu, đang làm quen với luật chơi và cơ bản |
| **II** | **Đồng Học** | 51-100 | ![#CD7F32](https://via.placeholder.com/15/CD7F32/000000?text=+) Đồng | 🥉 | Đã nắm vững luật chơi, bắt đầu hiểu chiến thuật cơ bản |
| **III** | **Bạc Học** | 101-150 | ![#C0C0C0](https://via.placeholder.com/15/C0C0C0/000000?text=+) Bạc | 🥈 | Người chơi có kinh nghiệm, biết phòng thủ và tấn công |
| **IV** | **Nhập Môn** | 151-200 | ![#4CAF50](https://via.placeholder.com/15/4CAF50/000000?text=+) Xanh lá | 🌱 | Bắt đầu hiểu sâu về chiến thuật, tạo nhánh đôi |
| **V** | **Tinh Thông** | 201-250 | ![#2196F3](https://via.placeholder.com/15/2196F3/000000?text=+) Xanh dương | 💎 | Thành thạo kỹ thuật, biết đọc nước đi của đối thủ |
| **VI** | **Đại Sư** | 251-300 | ![#9C27B0](https://via.placeholder.com/15/9C27B0/000000?text=+) Tím | 💜 | Bậc thầy chiến thuật, ít khi mắc lỗi |
| **VII** | **Tôn Giả** | 301-350 | ![#FF9800](https://via.placeholder.com/15/FF9800/000000?text=+) Cam | 🧡 | Đẳng cấp cao thủ, thống trị bảng xếp hạng |
| **VIII** | **Chí Tôn** | 351-400 | ![#F44336](https://via.placeholder.com/15/F44336/000000?text=+) Đỏ | ❤️ | Kẻ mạnh nhất server, rất khó đánh bại |
| **IX** | **Huyền Thánh** | 401-450 | ![#FFD700](https://via.placeholder.com/15/FFD700/000000?text=+) Vàng | 👑 | Huyền thoại bất bại, chỉ có 1-2 người đạt được |
| **X** | **Thần Thoại** | 451-500 | ![#E91E63](https://via.placeholder.com/15/E91E63/000000?text=+) Hồng | ⚡ | Vượt qua mọi giới hạn, đỉnh cao tuyệt đối |

---

### 📈 Progression System

#### Hiển Thị Trên UI
- **Level Number**: Số level hiện tại (1-100,000)
- **Tier Badge**: Huy hiệu màu sắc với tên tier
- **Progress Bar**: Thanh tiến trình đến level tiếp theo
- **XP Display**: `1250 / 1300 XP` (XP hiện tại / XP cần cho level tiếp theo)

#### Ví Dụ Cụ Thể
```
Player: admin
Level: 127
Tier: Bạc Học (Level 101-150)
XP: 12,650 / 12,700 (còn 50 XP nữa lên Level 128)
Rank Score: 12,650 pts
```

#### Leaderboard
- Hiển thị **Top 100 players** theo rank_score
- Sắp xếp: Cao → Thấp
- Thông tin: Rank, Display Name, Tier Badge, Level, Points
- Real-time update sau mỗi trận đấu

---

### 🎯 Mục Tiêu Progression

| Mốc | Level | Tier | Thành Tựu |
|-----|-------|------|-----------|
| 🎯 | 50 | Tân Thủ → Đồng Học | Hoàn thành giai đoạn tập sự |
| 🎯 | 100 | Đồng Học → Bạc Học | Trở thành người chơi có kinh nghiệm |
| 🎯 | 200 | Nhập Môn → Tinh Thông | Bước vào hàng ngũ cao thủ |
| 🎯 | 300 | Đại Sư → Tôn Giả | Top player của server |
| 🎯 | 400 | Chí Tôn → Huyền Thánh | Huyền thoại sống |
| 🎯 | 500 | Thần Thoại | Đỉnh cao tuyệt đối |

---

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
- `POST /api/login` - Đăng nhập (username, password)
- `POST /api/signup` - Đăng ký (username, password, display_name, email)

### User
- `GET /api/user/:id` - Lấy thông tin user
- `PUT /api/user/:id` - Cập nhật profile (display_name, avatar_url)
- `GET /api/public/:id` - Lấy public profile
- `GET /api/user/:id/matches` - Lấy match history

### Leaderboard
- `GET /api/leaderboard` - Top 100 players theo rank_score

### Match
- `GET /api/match/:id` - Lấy chi tiết trận đấu (cho replay)

---

## 🔌 Socket.IO Events

### Client → Server
- `join_matchmaking` - Tham gia matchmaking (userId, type, mode, difficulty)
- `make_move` - Thực hiện nước đi (roomId, r, c, player)
- `send_chat` - Gửi tin nhắn chat (roomId, message, sender, senderId)
- `request_undo` - Xin đi lại (roomId)
- `resolve_undo` - Phản hồi yêu cầu undo (roomId, accept)
- `claim_timeout` - Claim thắng do timeout (roomId)
- `leave_game` - Rời trận đấu (roomId)

### Server → Client
- `match_found` - Tìm thấy trận đấu (roomId, opponent, board, gameType, mode, playerNumber)
- `game_update` - Cập nhật trạng thái game (board, currentPlayer, winner, winningLine, lastMove)
- `receive_chat` - Nhận tin nhắn chat (sender, senderId, message)
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

1. Fork repo này
2. Tạo branch mới (`git checkout -b feature/TinhNangMoi`)
3. Commit changes (`git commit -m 'Thêm tính năng X'`)
4. Push lên branch (`git push origin feature/TinhNangMoi`)
5. Tạo Pull Request

---

## 📝 License

Project này được phát hành dưới giấy phép MIT. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 👨‍💻 Tác Giả

**Lowji1910**
- GitHub: [@Lowji1910](https://github.com/Lowji1910)
- Project: [Caro Game](https://github.com/Lowji1910/caro)

---

## 🙏 Credits

- **Icons**: [Lucide Icons](https://lucide.dev/)
- **Font**: [Fredoka (Google Fonts)](https://fonts.google.com/specimen/Fredoka)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Hosting**: [Vercel](https://vercel.com/), [Render](https://render.com/)
- **Database**: [PlanetScale](https://planetscale.com/)

---

## 📸 Screenshots

_Coming soon..._

---

## 🐛 Known Issues

- Replay có thể bị lỗi nếu moves không được lưu đúng format JSON
- Avatar URL cần validate để tránh broken images
- Timeout detection có thể có race condition trong một số trường hợp

---

## 🔮 Roadmap

- [x] Chat trong game
- [x] Auto-forfeit khi leave game
- [ ] Spectator mode
- [ ] Tournament system
- [ ] Achievement badges
- [ ] Friend system
- [ ] Mobile app (React Native)

---

**⭐ Nếu bạn thấy project hay, hãy cho 1 star nhé! ⭐**
