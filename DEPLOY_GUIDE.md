# 🚀 Hướng Dẫn Deploy Game Caro (Miễn Phí)

Hướng dẫn deploy game để **gửi link cho bạn bè test**. Hoàn toàn **MIỄN PHÍ** cho sinh viên!

## 📋 Tổng Quan

- **Frontend**: Deploy lên **Vercel** (miễn phí, nhanh)
- **Backend**: Deploy lên **Render** (free tier)
- **Database**: Dùng **PlanetScale** hoặc **Railway** (miễn phí)

---

## 🎯 Bước 1: Chuẩn Bị Database (PlanetScale)

### 1.1. Tạo Tài Khoản

1. Truy cập https://planetscale.com
2. Sign up với **GitHub** (miễn phí)
3. Create New Database:
   - Name: `caro-game-db`
   - Region: **AWS ap-southeast-1** (Singapore - gần VN)

### 1.2. Import Database Schema

1. Click **Console** tab
2. Paste và run từng lệnh SQL:

```sql
-- Tạo bảng users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    display_name VARCHAR(50),
    full_name VARCHAR(100),
    date_of_birth DATE,
    bio TEXT,
    avatar_url VARCHAR(255),
    rank_score INT DEFAULT 0,
    rank_level VARCHAR(20) DEFAULT 'Bronze',
    user_level INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tạo bảng match_history
CREATE TABLE match_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player1_id INT,
    player2_id INT,
    winner_id INT,
    game_type VARCHAR(20),
    mode VARCHAR(20),
    moves JSON DEFAULT NULL,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player1_id) REFERENCES users(id),
    FOREIGN KEY (player2_id) REFERENCES users(id)
);

-- Tạo bảng user_levels_history
CREATE TABLE user_levels_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    level INT NOT NULL,
    rank_score INT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tạo bảng game_levels
CREATE TABLE game_levels (
    level INT PRIMARY KEY,
    required_score INT NOT NULL,
    INDEX idx_score (required_score)
);

-- Tạo bảng tiers
CREATE TABLE tiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL,
    description TEXT,
    min_level INT NOT NULL,
    max_level INT NOT NULL,
    INDEX idx_level_range (min_level, max_level)
);
```

3. **Copy Connection String**:
   - Click **Connect**
   - Chọn **Python**
   - Copy connection string (giữ lại để dùng sau)

---

## 🔧 Bước 2: Deploy Backend (Render)

### 2.1. Chuẩn Bị Code

Tạo file `requirements.txt` trong thư mục `backend/`:

```txt
Flask==2.3.0
Flask-SocketIO==5.3.0
Flask-CORS==4.0.0
python-socketio==5.9.0
mysql-connector-python==8.1.0
python-engineio==4.7.0
gunicorn==21.2.0
eventlet==0.33.3
```

Tạo file `Procfile` trong thư mục `backend/`:

```
web: gunicorn --worker-class eventlet -w 1 app:app
```

### 2.2. Tạo Tài Khoản Render

1. Truy cập https://render.com
2. Sign up với **GitHub**
3. Click **New +** → **Web Service**

### 2.3. Cấu Hình Deploy

- **Repository**: Chọn repo GitHub của bạn
- **Name**: `caro-backend`
- **Root Directory**: `backend`
- **Environment**: **Python 3**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn --worker-class eventlet -w 1 app:app
  ```

### 2.4. Thêm Environment Variables

Click **Environment** tab, thêm:

```
DATABASE_HOST=<từ PlanetScale>
DATABASE_USER=<từ PlanetScale>
DATABASE_PASSWORD=<từ PlanetScale>
DATABASE_NAME=caro-game-db
PORT=5000
```

### 2.5. Deploy

- Click **Create Web Service**
- Đợi 5-10 phút
- Copy URL backend (vd: `https://caro-backend.onrender.com`)

---

## 🎨 Bước 3: Deploy Frontend (Vercel)

### 3.1. Cập Nhật Config

Sửa file `constants.ts`:

```typescript
export const SOCKET_URL = 'https://caro-backend.onrender.com'; // URL backend từ Render
```

Build frontend:

```bash
npm run build
```

### 3.2. Deploy Lên Vercel

1. Truy cập https://vercel.com
2. Sign up với **GitHub**
3. Click **Add New** → **Project**
4. Chọn repo của bạn
5. Cấu hình:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (thư mục gốc)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

6. Click **Deploy**
7. Đợi 2-3 phút
8. Copy link (vd: `https://caro-game.vercel.app`)

---

## ✅ Bước 4: Test & Chia Sẻ

### 4.1. Kiểm Tra

1. Truy cập link Vercel
2. Tạo tài khoản
3. Chơi thử 1 game
4. Check xem có lỗi không

### 4.2. Gửi Cho Bạn Bè

**Link game**: `https://caro-game.vercel.app`

Bạn bè chỉ cần:
1. Click vào link
2. Sign up
3. Chơi ngay!

---

## 🔥 Giải Pháp Thay Thế (Nếu Render Chậm)

### Option 2: Railway (Nhanh hơn)

1. Truy cập https://railway.app
2. Deploy backend + database cùng 1 nơi
3. Free $5/tháng credit

### Option 3: Ngrok (Test Nhanh)

Nếu chỉ muốn test ngay:

```bash
# Backend
cd backend
python app.py

# Terminal mới
ngrok http 5000
```

Copy URL ngrok, gửi cho bạn bè!

---

## 🐛 Troubleshooting

### Lỗi CORS
Thêm vào `backend/app.py`:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

### Database Connection Error
- Check environment variables
- Verify PlanetScale IP whitelist (allow all)

### SocketIO Not Working
- Đảm bảo dùng `eventlet` worker
- Check WebSocket support trên Render

---

## 💰 Chi Phí

| Dịch Vụ | Miễn Phí? | Giới Hạn |
|---------|-----------|----------|
| Vercel | ✅ | 100GB bandwidth/tháng |
| Render | ✅ | Server sleep sau 15 phút không dùng |
| PlanetScale | ✅ | 5GB storage, 1 billion reads/tháng |

**→ Đủ cho vài trăm người test!**

---

## 📱 Nâng Cao (Sau Này)

- **Custom Domain**: Mua domain .tech ($5/năm)
- **Analytics**: Thêm Google Analytics
- **Monitoring**: Dùng Sentry (free) để track lỗi

---

## 🎓 Lưu Ý Cho Sinh Viên

- ✅ Deploy **miễn phí hoàn toàn**
- ✅ Có thể thêm vào **CV/Portfolio**
- ✅ Link công khai để demo cho nhà tuyển dụng
- ⚠️ Free tier có giới hạn, không dùng cho production thực

**Good luck với project! 🚀**
