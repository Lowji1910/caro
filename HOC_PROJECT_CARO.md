# 📚 TÀI LIỆU HỌC PROJECT CARO - 5 THÀNH VIÊN

## 📖 Mục Lục

Chào mừng đến với tài liệu phân công học project Caro! Dưới đây là danh sách các file tài liệu:

### 📄 File Chung

1. **[00_TONG_QUAN_CHUNG.md](./00_TONG_QUAN_CHUNG.md)**
   - Giới thiệu tổng quan về project
   - Kiến trúc hệ thống (Frontend, Backend, Database)
   - Tính năng chính
   - Luồng hoạt động chung
   - Kiến thức cần biết cho cả nhóm
   - Cấu trúc file tổng thể

2. **[CHECKLIST_DAY_DU.md](./CHECKLIST_DAY_DU.md)**
   - Checklist đầy đủ 87 chức năng
   - Phân công chi tiết theo chức năng
   - Bảng thống kê phần trăm công việc
   - Xác nhận đã chia hết 100% project

### 👥 File Riêng Cho Từng Thành Viên

3. **[01_LOI_Frontend_Auth.md](./01_LOI_Frontend_Auth.md)** - NGUYỄN THÀNH LỢI
   - **Vai trò**: Frontend Core & Authentication System
   - **Files phụ trách**: App.tsx (743 dòng), Login.tsx, Signup.tsx, Header.tsx
   - **Kiến thức**: React Hooks, TypeScript, Socket.IO Client, LocalStorage
   - **Nội dung**: Quản lý state toàn cục, routing, đăng nhập/đăng ký, session

4. **[02_KHOA_Game_AI.md](./02_KHOA_Game_AI.md)** - LÊ ĐĂNG KHOA
   - **Vai trò**: Game Logic & AI System
   - **Files phụ trách**: engine.py, ai.py (683 dòng), GameBoard.tsx
   - **Kiến thức**: Thuật toán Minimax, Alpha-Beta Pruning, Game Theory
   - **Nội dung**: Game engine, AI thông minh, kiểm tra thắng/thua

5. **[03_NGOC_UI_Chat.md](./03_NGOC_UI_Chat.md)** - NGUYỄN THỊ NHƯ NGỌC
   - **Vai trò**: UI/UX Components & Real-time Chat
   - **Files phụ trách**: Profile.tsx (527 dòng), ChatBox.tsx, ReplayBoard.tsx, RankInfoModal.tsx
   - **Kiến thức**: React Components, UI/UX Design, WebSocket Chat
   - **Nội dung**: Giao diện người dùng, chat realtime, replay viewer

6. **[04_KIET_Database_Ranking.md](./04_KIET_Database_Ranking.md)** - NGUYỄN VŨ TUẤN KIỆT
   - **Vai trò**: Database & Ranking System
   - **Files phụ trách**: user_service.py, rank_service.py, match_service.py, leaderboard_service.py, auth.py, user.py
   - **Kiến thức**: MySQL, SQL Queries, REST APIs, Password Hashing
   - **Nội dung**: Database operations, hệ thống ranking 500 levels + 10 tiers + 4 ranks

7. **[05_TRUONG_Socket_Matchmaking.md](./05_TRUONG_Socket_Matchmaking.md)** - TÔ NGUYỄN THIÊN TRƯỜNG
   - **Vai trò**: Socket & Matchmaking System
   - **Files phụ trách**: matchmaking.py, game.py (371 dòng), state.py
   - **Kiến thức**: WebSocket, Socket.IO, Event-Driven Architecture
   - **Nội dung**: Matchmaking, game events, realtime synchronization

---

## 🎯 Cách Sử Dụng Tài Liệu

### Bước 1: Đọc File Tổng Quan
Bắt đầu với **00_TONG_QUAN_CHUNG.md** để hiểu tổng thể project:
- Kiến trúc hệ thống
- Các tính năng chính
- Luồng hoạt động chung
- Kiến thức chung cần biết

### Bước 2: Đọc File Cá Nhân
Mỗi thành viên đọc file riêng của mình:
- **Lợi** → 01_LOI_Frontend_Auth.md
- **Khoa** → 02_KHOA_Game_AI.md
- **Ngọc** → 03_NGOC_UI_Chat.md
- **Kiệt** → 04_KIET_Database_Ranking.md
- **Trường** → 05_TRUONG_Socket_Matchmaking.md

### Bước 3: Học Theo Cấu Trúc File
Mỗi file cá nhân có cấu trúc:
1. **Vai trò của bạn** - Tổng quan về nhiệm vụ
2. **Kiến thức cần nắm** - Lý thuyết với ví dụ code
3. **Files bạn phụ trách** - Danh sách files cần học
4. **Luồng hoạt động chi tiết** - Giải thích từng bước
5. **Bảng các hàm quan trọng** - Functions chính
6. **Nội dung thuyết trình** - 8 phút presentation
7. **Tips học hiệu quả** - Gợi ý cách học

### Bước 4: Kiểm Tra Checklist
Đối chiếu với **CHECKLIST_DAY_DU.md** để đảm bảo:
- Đã hiểu hết các chức năng được giao
- Không bỏ sót tính năng nào
- Phần của mình liên quan đến ai khác

---

## 📊 Phân Bổ Công Việc

| Thành viên | Vai trò | Files chính | Tỷ lệ |
|------------|---------|-------------|-------|
| **Lợi** | Frontend Core & Auth | App.tsx, Login, Signup, Header | 17% |
| **Khoa** | Game Logic & AI | engine.py, ai.py, GameBoard.tsx | 13% |
| **Ngọc** | UI/UX & Chat | Profile, ChatBox, ReplayBoard | 21% |
| **Kiệt** | Database & Ranking | services, routes, APIs | 32% |
| **Trường** | Socket & Matchmaking | matchmaking.py, game.py | 17% |

**Tổng: 87 chức năng đã được phân công 100%** ✅

---

## 🎤 Hướng Dẫn Thuyết Trình

Mỗi thành viên có **8 phút** để thuyết trình phần của mình:

1. **Giới thiệu vai trò** (1 phút)
2. **Giải thích kiến thức nền tảng** (2-3 phút)
3. **Demo luồng hoạt động** (2-3 phút)
4. **Tổng kết** (0.5-1 phút)

Chi tiết nội dung thuyết trình xem trong file cá nhân!

---

## 💡 Tips Chung

### 1. Học Theo Luồng
- Không đọc code từ đầu file
- Trace theo 1 luồng cụ thể (VD: luồng login)
- Hiểu input → xử lý → output

### 2. Chạy Và Debug
- Chạy app thực tế
- Đặt breakpoint hoặc console.log
- Xem data flow

### 3. Vẽ Diagram
- Vẽ sơ đồ luồng hoạt động
- Vẽ kiến trúc hệ thống
- Giúp hiểu và nhớ lâu hơn

### 4. Hỏi Nhóm
- Phần của mình liên quan đến của ai → hỏi họ
- Học theo nhóm hiệu quả hơn học một mình

---

## 📝 Ghi Chú Quan Trọng

- ✅ Tất cả file đều được viết bằng **Markdown** (.md)
- ✅ Có thể đọc bằng bất kỳ text editor nào
- ✅ Recommend: VS Code, Typora, hoặc GitHub để render đẹp
- ✅ Mỗi file có **table of contents** tự động (nếu dùng đúng tool)

---

## 🚀 Chúc Các Bạn Học Tốt!

Nếu có thắc mắc, đọc lại phần tương ứng hoặc hỏi nhóm.
Project này rất đầy đủ và chuyên nghiệp, học được nhiều lắm! 💪

---

*Tài liệu được tạo tự động từ phân tích chi tiết project Caro*
*Ngày tạo: 2024-12-02*
