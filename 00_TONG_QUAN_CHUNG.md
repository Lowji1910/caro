# 📚 TỔNG QUAN PROJECT CARO - PHÂN CÔNG HỌC CHO 5 THÀNH VIÊN

## 🎯 Giới Thiệu Tổng Quan

Chào các bạn! Đây là một project game **Caro và Tic-Tac-Toe** online thời gian thực với hệ thống xếp hạng cực kỳ hoàn chỉnh. Project này được xây dựng bằng **React + TypeScript** cho phần giao diện và **Python Flask + SocketIO** cho phần backend. Đây là một hệ thống phức tạp kết hợp nhiều công nghệ hiện đại như realtime communication, AI game, và database management.

## 🏗️ Kiến Trúc Tổng Thể

### Frontend (React + TypeScript)
- **Framework**: React 19.2.0 với TypeScript 5.8.2
- **Styling**: Tailwind CSS 4 với glassmorphism effects
- **Realtime**: Socket.IO Client để kết nối với server
- **Components**: 11 components chính (Login, Signup, GameBoard, Profile, Header, ChatBox...)
- **State Management**: React Hooks (useState, useEffect, useRef)

### Backend (Python + Flask)
- **Framework**: Flask 3.0 với Flask-SocketIO 5.3.6
- **Database**: MySQL 8.0+ với mysql-connector-python
- **Game Logic**: Custom game engine với AI Minimax
- **Architecture**: Chia thành routes, services, sockets, game modules

### Database (MySQL)
- **users**: Thông tin người dùng (username, password, level, rank_points, xp)
- **game_levels**: 500 levels với XP progression
- **tiers**: 10 danh hiệu (Tân Thủ → Chí Tôn)
- **ranks**: 4 hạng (Bronze, Silver, Gold, Crystal)
- **match_history**: Lịch sử trận đấu với moves JSON

## 🎮 Tính Năng Chính

### 1. Hai Chế Độ Game
- **Tic-Tac-Toe (3x3)**: Game cổ điển, 3 ô liên tiếp để thắng
- **Caro (15x20)**: Game phức tạp hơn, 5 ô liên tiếp để thắng

### 2. Hai Modes Chơi
- **Ranked Mode**: Đấu với người thật, tính điểm xếp hạng, có timeout 30s/nước
- **Practice Mode**: Luyện tập với AI (3 độ khó: Easy, Medium, Hard)

### 3. Hệ Thống Xếp Hạng
- **XP System**: Luôn tăng (thắng +50, thua +15), quyết định Level (1-500)
- **Rank Points**: Có thể tăng/giảm (thắng +25, thua -10), quyết định Rank (Bronze → Crystal)
- **Tiers**: 10 danh hiệu theo level (mỗi danh hiệu 50 levels)

### 4. Realtime Features
- **Matchmaking**: Tự động ghép đối thủ qua Socket.IO
- **Live Chat**: Trò chuyện trong game (max 200 ký tự)
- **Undo Request**: Xin đi lại (cần đối thủ đồng ý)
- **Timeout Detection**: Hết giờ = thua

### 5. AI Thông Minh
- **Thuật toán**: Minimax với Alpha-Beta Pruning
- **Độ khó**:
  - Easy: depth 1-2 (dễ thắng)
  - Medium: depth 3 (cân bằng)
  - Hard: depth 4-5 (rất khó)

## 📊 Luồng Hoạt Động Chính

### A. Luồng Đăng Nhập/Đăng Ký
1. User nhập username/password trên giao diện Login
2. Frontend gửi POST request đến `/api/login` hoặc `/api/signup`
3. Backend kiểm tra database, hash password bằng werkzeug.security
4. Trả về user profile đầy đủ (bao gồm level, tier, rank info)
5. Frontend lưu user vào localStorage và hiển thị Dashboard

### B. Luồng Matchmaking (Ranked Mode)
1. User click "Trận Đấu Xếp Hạng" từ Dashboard
2. Frontend emit socket event `join_matchmaking` với userId, gameType, mode
3. Backend thêm user vào hàng đợi `matchmaking_queue`
4. Nếu đủ 2 người: tạo room, tạo board, emit `match_found` cho cả 2
5. Frontend nhận `match_found`, chuyển sang view GAME, hiển thị board

### C. Luồng Chơi Game
1. Player click vào ô trống trên bàn cờ
2. Frontend emit `make_move` với roomId, r (row), c (col), player
3. Backend kiểm tra valid move, apply move vào board
4. Backend kiểm tra thắng/thua/hòa bằng GameEngine.check_winner
5. Backend emit `game_update` cho cả 2 players với board mới
6. Nếu có winner: gọi `_handle_end_game` để update rank và lưu match history
7. Frontend hiển thị kết quả, refetch user profile để cập nhật XP/Level/Rank

### D. Luồng Practice Mode (AI)
1. User chọn "Luyện Tập", chọn độ khó (Easy/Medium/Hard)
2. Backend tạo game với player 2 là 'AI'
3. Khi đến lượt AI: gọi AIPlayer.get_ai_move
4. AI dùng Minimax để tìm nước đi tối ưu
5. Backend apply move của AI, emit `game_update` về client

### E. Luồng Chat
1. User gõ tin nhắn, nhấn Enter
2. Frontend emit `send_chat` với roomId, message, sender
3. Backend sanitize message (escape HTML), emit `receive_chat` cho room
4. Frontend append message vào chatMessages array

### F. Luồng Undo Request
1. Player A emit `request_undo`
2. Backend emit `undo_requested` cho Player B
3. Player B nhận popup confirm
4. Player B emit `resolve_undo` với accept=true/false
5. Nếu accept: Backend rollback board, emit `game_update`
6. Nếu decline: Backend emit `undo_declined` cho Player A

## 🔑 Kiến Thức Chung Cho Cả Nhóm

### 1. Công Nghệ & Frameworks
- **React**: Library UI với component-based architecture
- **TypeScript**: JavaScript có type safety, giúp code ít lỗi hơn
- **Flask**: Micro web framework của Python, nhẹ và linh hoạt
- **Socket.IO**: Library cho realtime bidirectional communication
- **MySQL**: Relational database, dùng SQL để query data

### 2. Concepts Quan Trọng
- **Component**: Khối UI có thể tái sử dụng (VD: Button, Header, GameBoard)
- **Props**: Dữ liệu truyền từ component cha xuống component con
- **State**: Dữ liệu nội bộ của component, khi state thay đổi → component re-render
- **Hook**: Hàm đặc biệt của React (useState, useEffect, useRef)
- **WebSocket**: Kết nối realtime 2 chiều giữa client và server
- **REST API**: Cách client gọi server qua HTTP (GET, POST, PUT, DELETE)

### 3. Game Logic Cơ Bản
- **Board Representation**: Mảng 2 chiều [[0,0,0], [0,1,0], [2,0,0]]
  - 0 = ô trống
  - 1 = Player 1 (X)
  - 2 = Player 2 (O)
- **Winner Check**: Kiểm tra 4 hướng (ngang, dọc, chéo xuống, chéo lên)
- **Minimax Algorithm**: Thuật toán tìm nước đi tối ưu bằng cách mô phỏng tất cả khả năng
- **Alpha-Beta Pruning**: Tối ưu Minimax bằng cách bỏ qua các nhánh không cần thiết

### 4. Database Schema Quan Trọng
```sql
users:
  - id, username, password_hash
  - display_name, full_name, email
  - level (1-500), xp (kinh nghiệm)
  - rank_points (điểm xếp hạng), rank_id (1-4)
  - wins, losses, draws

match_history:
  - id, player1_id, player2_id
  - winner_id, game_type, mode
  - moves (JSON array), duration
```

## 📁 Cấu Trúc File Tổng Thể

### Frontend
```
components/
  ├── Login.tsx (270 dòng) - Form đăng nhập
  ├── Signup.tsx (240 dòng) - Form đăng ký
  ├── Header.tsx (115 dòng) - Thanh header với level/rank
  ├── GameBoard.tsx (216 dòng) - Bàn cờ chính
  ├── Profile.tsx (527 dòng) - Trang profile + match history
  ├── ChatBox.tsx (160 dòng) - Chat trong game
  ├── ReplayBoard.tsx (171 dòng) - Xem lại trận đấu
  └── ...

App.tsx (743 dòng) - Component chính, quản lý state và routing
types.ts (50 dòng) - TypeScript interfaces
constants.ts (30 dòng) - Hằng số (colors, gradients, config)
```

### Backend
```
backend/
  ├── app.py (41 dòng) - Entry point, khởi tạo Flask + SocketIO
  ├── config.py (40 dòng) - Cấu hình (DB, game rules)
  │
  ├── game/
  │   ├── engine.py (149 dòng) - Game logic core
  │   └── ai.py (683 dòng) - AI Minimax
  │
  ├── routes/
  │   ├── auth.py (60 dòng) - Login/Signup APIs
  │   ├── user.py (170 dòng) - User profile APIs
  │   └── leaderboard.py (40 dòng) - Bảng xếp hạng API
  │
  ├── services/
  │   ├── user_service.py (240 dòng) - User CRUD
  │   ├── rank_service.py (176 dòng) - Xử lý ranking
  │   ├── match_service.py (130 dòng) - Lưu/lấy match history
  │   └── leaderboard_service.py (110 dòng) - Top players
  │
  └── sockets/
      ├── matchmaking.py (131 dòng) - Ghép cặp đối thủ
      ├── game.py (371 dòng) - Xử lý game events
      └── state.py (15 dòng) - Shared state
```

## 🎯 Phân Công Chi Tiết Cho 5 Thành Viên

### Nguyễn Thành Lợi - Frontend Core & Authentication
**Trọng tâm**: Hệ thống đăng nhập/đăng ký và quản lý state chính của ứng dụng

### Lê Đăng Khoa - Game Logic & AI System
**Trọng tâm**: Game engine, thuật toán AI Minimax, và logic kiểm tra thắng thua

### Nguyễn Thị Như Ngọc - UI/UX Components & Real-time Chat
**Trọng tâm**: Các components giao diện người dùng và hệ thống chat realtime

### Nguyễn Vũ Tuấn Kiệt - Database & Ranking System
**Trọng tâm**: Hệ thống xếp hạng, services xử lý database, và APIs

### Tô Nguyễn Thiên Trường - Socket & Matchmaking System
**Trọng tâm**: Socket.IO handlers, matchmaking, và realtime game events

---

## 📖 Hướng Dẫn Sử Dụng Tài Liệu

Mỗi thành viên sẽ có một file riêng với nội dung chi tiết:
- **Kiến thức cần biết**: Lý thuyết cần nắm
- **Files phụ trách**: Danh sách file cần học
- **Luồng hoạt động**: Giải thích chi tiết cách hệ thống chạy
- **Các hàm quan trọng**: Bảng liệt kê functions chính
- **Nhiệm vụ thuyết trình**: Nội dung cần trình bày

Chúc các bạn học tốt! 🚀
