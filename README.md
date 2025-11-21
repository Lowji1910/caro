# 🎮 Game Cờ Caro & Tic-Tac-Toe Online

> Game cờ caro và tic-tac-toe thời gian thực với hệ thống xếp hạng, matchmaking và AI thông minh.

[![GitHub](https://img.shields.io/badge/GitHub-Lowji1910%2Fcaro-blue)](https://github.com/Lowji1910/caro)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Tính Năng Nổi Bật

### 🏆 Hệ Thống Xếp Hạng
- **500 cấp độ** với 9 rank tier (Tân Thủ → Huyền Thánh)
- Tính điểm Elo: Thắng +25, Thua -10
- Bảng xếp hạng realtime với tier badge đẹp mắt
- Lịch sử level-up được lưu trữ

### 🎯 Chế Độ Chơi
- **Ranked Mode**: Đấu xếp hạng với người chơi thật
- **Practice Mode**: Luyện tập với AI (3 độ khó)
- **Matchmaking**: Tự động ghép cặp đối thủ cùng rank
- **Replay System**: Xem lại trận đấu đã chơi

### 🤖 AI Thông Minh
- Thuật toán Minimax với Alpha-Beta Pruning
- Đánh giá vị trí thông minh (phòng thủ & tấn công)
- Caro AI: Phát hiện nước 3, 4 liên tiếp và chặn đứng
- 3 độ khó: Dễ, Trung bình, Khó

### 🎨 Giao Diện Hiện Đại
- Responsive design (chơi được trên mobile)
- Dark mode với glassmorphism effect
- Animation mượt mà
- Avatar system với URL upload

### 💬 Tính Năng Khác
- Real-time multiplayer (Socket.IO)
- Profile cá nhân với thống kê chi tiết
- Match history với replay
- Timeout detection (30s/nước)

---

## 🛠️ Công Nghệ Sử Dụng

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Socket.IO Client** - Real-time communication
- **Lucide Icons** - Icon library

### Backend
- **Python 3.8+** - Server language
- **Flask** - Web framework
- **Flask-SocketIO** - WebSocket support
- **MySQL** - Database
- **mysql-connector-python** - DB driver

---

## 📦 Cài Đặt & Chạy Thử

### 1️⃣ Yêu Cầu Hệ Thống

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **MySQL** (XAMPP hoặc MySQL Workbench)
- **Git** ([Download](https://git-scm.com/))

### 2️⃣ Clone Repository

```bash
git clone https://github.com/Lowji1910/caro.git
cd caro
```

### 3️⃣ Setup Database

1. Mở **XAMPP** và start **MySQL**
2. Truy cập **phpMyAdmin** (`http://localhost/phpmyadmin`)
3. Tạo database `tic_tac_toe_db`
4. Import file `database.sql`
5. Chạy các migration:
   ```sql
   -- Thêm cột moves (cho replay)
   ALTER TABLE match_history ADD COLUMN moves JSON DEFAULT NULL;
   
   -- Import từ file backend/migrations/add_ranking_tables.sql
   ```

### 4️⃣ Setup Backend

```bash
cd backend

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app.py
```

Server chạy tại: `http://localhost:5000`

### 5️⃣ Setup Frontend

```bash
# Về thư mục gốc
cd ..

# Cài đặt dependencies
npm install

# Chạy dev server
npm run dev
```

Frontend chạy tại: `http://localhost:5173`

### 6️⃣ Chơi Thử!

1. Mở trình duyệt vào `http://localhost:5173`
2. Sign up tài khoản mới
3. Chọn chế độ chơi và bắt đầu!

---

## 🚀 Deploy Lên Internet

Xem hướng dẫn chi tiết trong file [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

**TL;DR:**
- **Frontend**: Vercel (miễn phí)
- **Backend**: Render (free tier)
- **Database**: PlanetScale (miễn phí)

---

## 📁 Cấu Trúc Thư Mục

```
caro/
├── backend/
│   ├── app.py                  # Flask server chính
│   ├── config.py               # Cấu hình
│   ├── database/               # Database connection
│   ├── game/                   # Game engine & AI
│   │   ├── engine.py           # Logic game
│   │   └── ai.py               # Minimax AI
│   ├── routes/                 # API endpoints
│   ├── services/               # Business logic
│   │   ├── user_service.py
│   │   ├── match_service.py
│   │   ├── rank_service.py
│   │   └── leaderboard_service.py
│   ├── sockets/                # Socket.IO handlers
│   ├── migrations/             # SQL migrations
│   └── tests/                  # Unit tests
│
├── components/                 # React components
│   ├── GameBoard.tsx           # Bàn cờ
│   ├── ReplayBoard.tsx         # Replay viewer
│   ├── Header.tsx              # Header với avatar
│   └── Profile.tsx             # Trang profile
│
├── utils/                      # Utilities
├── App.tsx                     # Main App
├── types.ts                    # TypeScript types
├── database.sql                # Schema SQL
└── README.md                   # File này
```

---

## 🎮 Hướng Dẫn Chơi

### Tic-Tac-Toe (3x3)
- Xếp 3 ô liên tiếp (ngang/dọc/chéo) để thắng
- Hòa nếu hết ô mà không ai thắng

### Caro (15x20)
- Xếp 5 ô liên tiếp để thắng
- Không giới hạn số nước đi
- Có thể block đối thủ

### Điều Khiển
- **Click chuột**: Đặt quân
- **Replay**: Dùng nút ◀ ▶ để xem lại

---

## 🏅 Hệ Thống Rank

| Rank | Tên | Cấp độ | Màu |
|------|-----|--------|-----|
| 🆕 | Tân Thủ | 1-10 | Xám |
| 🥉 | Đồng Học | 11-30 | Đồng |
| 🥈 | Bạc Học | 31-50 | Bạc |
| 🌱 | Nhập Môn | 51-100 | Xanh lá |
| 💎 | Tinh Thông | 101-150 | Xanh dương |
| 💜 | Đại Sư | 151-200 | Tím |
| 🧡 | Tôn Giả | 201-300 | Cam |
| ❤️ | Chí Tôn | 301-400 | Đỏ |
| 👑 | Huyền Thánh | 401-500 | Vàng |

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

- Icons: [Lucide Icons](https://lucide.dev/)
- Hosting: [Vercel](https://vercel.com/), [Render](https://render.com/)
- Database: [PlanetScale](https://planetscale.com/)

---

## 📸 Screenshots

_Thêm screenshots của game ở đây_

---

**⭐ Nếu bạn thấy project hay, hãy cho 1 star nhé! ⭐**

