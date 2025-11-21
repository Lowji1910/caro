# 📋 Hướng Dẫn Push Code Lên GitHub

## ✅ Đã Làm

- [x] Tạo file `.gitignore`
- [x] Sẵn sàng để push lên GitHub

## 🚀 Các Bước Push Code

### 1. Khởi tạo Git (nếu chưa có)

```bash
git init
git add .
git commit -m "Initial commit - Caro Game"
```

### 2. Tạo Repository Trên GitHub

1. Truy cập https://github.com
2. Click **New Repository**
3. Đặt tên: `caro-game` (hoặc tên khác)
4. Chọn **Public** (để bạn bè xem được)
5. **KHÔNG** tick "Initialize with README" (đã có rồi)
6. Click **Create Repository**

### 3. Kết Nối Với GitHub

Copy các lệnh GitHub cung cấp, hoặc chạy:

```bash
git remote add origin https://github.com/<username>/caro-game.git
git branch -M main
git push -u origin main
```

Thay `<username>` bằng username GitHub của bạn.

### 4. Xác Nhận

Truy cập `https://github.com/<username>/caro-game` để xem code!

---

## 📁 Các File Đã Loại Bỏ

File `.gitignore` sẽ tự động bỏ qua:

- ❌ `node_modules/` - dependencies (tải lại bằng `npm install`)
- ❌ `backend/__pycache__/` - Python cache
- ❌ `.env` - environment variables (bảo mật)
- ❌ `dist/` - build output
- ❌ `.vscode/` - IDE settings

---

## 🔐 File `.env` - QUAN TRỌNG!

File `.env` chứa **thông tin nhạy cảm** (database password) nên:

- ✅ **KHÔNG** push lên GitHub
- ✅ Tạo file `.env.example` để hướng dẫn:

```bash
# Tạo file mẫu
cp .env .env.example
```

Sau đó xóa các giá trị thật trong `.env.example`:

```
DATABASE_HOST=localhost
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_NAME=tic_tac_toe_db
```

---

## 📝 Cập Nhật Code Sau Này

```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

---

## 🎯 Tips

- Commit code thường xuyên với message rõ ràng
- Tạo branch riêng cho feature mới: `git checkout -b feature-name`
- Merge branch sau khi test OK

**Chúc mừng! Code của bạn đã sẵn sàng lên GitHub! 🎉**
