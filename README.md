# 🎮 Tic-Tac-Toe & Caro Multiplayer (Ranked System)

Dự án game Cờ Caro và Tic-Tac-Toe thời gian thực (Real-time) với hệ thống Xếp hạng (Ranking), Chat và Matchmaking.

## 🛠️ Công Nghệ Sử Dụng

*   **Frontend**: React 19, Tailwind CSS, Lucide Icons (Giao diện đẹp, Responsive).
*   **Backend**: Python Flask, Flask-SocketIO (Xử lý logic game, AI Minimax, Real-time communication).
*   **Database**: MySQL (Lưu trữ người dùng, lịch sử đấu, bảng xếp hạng).

---

## ⚙️ Hướng Dẫn Cài Đặt & Chạy

### 1. Yêu cầu hệ thống (Prerequisites)
*   **Python**: Phiên bản 3.8 trở lên.
*   **Node.js**: (Tùy chọn nếu bạn muốn build frontend, hiện tại code chạy trực tiếp trong môi trường React tích hợp).
*   **MySQL**: Khuyến nghị cài đặt **XAMPP** hoặc **MySQL Workbench**.

### 2. Cài đặt Database (MySQL)

1.  Mở **XAMPP Control Panel** và khởi động module **Apache** và **MySQL**.
2.  Truy cập **phpMyAdmin** (thường là `http://localhost/phpmyadmin`).
3.  Tạo một Database mới tên là: `tic_tac_toe_db`.
4.  Chọn database vừa tạo, vào tab **Import** (Nhập).
5.  Chọn file `database.sql` (nằm trong thư mục gốc của dự án) và nhấn **Import** để tạo các bảng dữ liệu (`users`, `player_rank`, `match_history`...).

### 3. Cài đặt Backend (Python Flask)

Mở Terminal (Command Prompt) và thực hiện các bước sau:

1.  Di chuyển vào thư mục backend:
    ```bash
    cd backend
    ```

2.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txtp
    ```

3.  **Cấu hình kết nối Database**:
    *   Mở file `backend/app.py`.
    *   Tìm đoạn code cấu hình `db_config`.
    *   Đảm bảo `password` khớp với mật khẩu MySQL của bạn (mặc định XAMPP là rỗng `""`).
    ```python
    db_config = {
        'user': 'root',
        'password': '',  # Điền mật khẩu MySQL của bạn nếu có
        'host': 'localhost',
        'database': 'tic_tac_toe_db'
    }
    ```

4.  Khởi chạy Server:
    ```bash
    python app.py
    ```
    *   Server sẽ chạy tại địa chỉ: `http://localhost:5000`.
    *   Bạn sẽ thấy thông báo: `Running on http://127.0.0.1:5000`.

### 4. Chạy Frontend

Trong môi trường phát triển này, Frontend (React) đã được cấu hình sẵn. Bạn chỉ cần đảm bảo Backend đang chạy.

*   Mở trình duyệt, ứng dụng sẽ tự động kết nối tới `http://localhost:5000`.
*   **Tài khoản mặc định** (do Database mới tạo chưa có user, bạn có thể đăng nhập để tạo mới):
    *   Hệ thống sẽ tự động tạo user nếu chưa tồn tại khi đăng nhập lần đầu (logic trong `backend/app.py` hàm `/api/login`).
    *   Thử nhập: Username: `player1`, Password: `password`.

---

## 📂 Cấu Trúc Thư Mục

```
.
├── backend/
│   ├── app.py           # Server chính (Socket.IO, API)
│   ├── game_engine.py   # Logic game, AI Minimax, Check Winner
│   └── requirements.txt # Thư viện Python
├── components/          # React Components (Board, Header, Button...)
├── services/            # (Đã deprecated, logic chuyển về backend)
├── App.tsx              # Main React App
├── database.sql         # Script tạo database
└── README.md            # Hướng dẫn sử dụng
```

## 🤖 Tính Năng Game

1.  **Ranked Mode (Đấu Xếp Hạng)**:
    *   Thắng: Cộng điểm Rank (+25).
    *   Thua: Trừ điểm Rank (-10).
    *   Hệ thống Rank: Bronze -> Silver -> Gold -> Crystal.

2.  **Practice Mode (Luyện Tập)**:
    *   Đấu với AI thông minh (Minimax + Alpha-Beta Pruning).
    *   AI Caro có khả năng chặn nước 3, 4 và tấn công.

3.  **Real-time**:
    *   Cập nhật bàn cờ tức thì qua Socket.IO.
    *   Hiển thị người đang online.

---

**Chúc bạn chơi game vui vẻ! 🎮**
