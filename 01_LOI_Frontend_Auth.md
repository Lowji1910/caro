# 📘 PHẦN HỌC CỦA NGUYỄN THÀNH LỢI
## Frontend Core & Authentication System

---

## 🎯 Vai Trò Của Bạn

Bạn chịu trách nhiệm phần **trái tim của frontend** - đó là component App.tsx chính và toàn bộ hệ thống xác thực người dùng (đăng nhập, đăng ký, quản lý session). Bạn sẽ làm việc với các công nghệ hiện đại nhất như React 19, TypeScript, và Socket.IO để tạo ra trải nghiệm người dùng mượt mà.

---

## 📚 Kiến Thức Cần Nắm

### 1. React Hooks - Trọng Tâm Của Bạn

React Hooks là cách hiện đại để quản lý state và side effects trong React. Bạn cần hiểu sâu 3 hooks chính:

#### **useState** - Quản Lý Trạng Thái
```typescript
const [view, setView] = useState<ViewState>('AUTH');
```
- `view` là giá trị hiện tại (có thể là 'AUTH', 'DASHBOARD', 'GAME', 'PROFILE'...)
- `setView` là hàm để thay đổi view
- Mỗi khi state thay đổi, component tự động re-render để cập nhật UI

**Ví dụ trong App.tsx**: Khi user login thành công, ta gọi `setView('DASHBOARD')` để chuyển từ màn hình login sang dashboard.

#### **useEffect** - Xử Lý Side Effects
```typescript
useEffect(() => {
  // Code chạy sau khi component render
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    setUser(JSON.parse(savedUser));
  }
}, []); // [] = chỉ chạy 1 lần khi component mount
```
- Dùng để gọi API, đọc localStorage, subscribe socket events
- Dependencies array `[]` quyết định khi nào effect chạy lại

**Ví dụ trong App.tsx**: Khi app khởi động, ta check localStorage xem có user đã login chưa. Nếu có thì tự động đăng nhập lại.

#### **useRef** - Lưu Giá Trị Không Trigger Re-render
```typescript
const socketRef = useRef<Socket | null>(null);
```
- Giống biến thông thường nhưng giá trị không mất khi re-render
- Truy cập qua `socketRef.current`
- Dùng để lưu socket connection, DOM elements, timers

**Ví dụ trong App.tsx**: Socket connection cần tồn tại xuyên suốt lifecycle của app, không nên tạo lại mỗi lần render.

### 2. TypeScript - Type Safety

TypeScript giúp code ít lỗi hơn bằng cách định nghĩa kiểu dữ liệu:

```typescript
interface UserProfile {
  id: number;
  username: string;
  display_name: string;
  level: number;
  xp: number;
  rank_score: number;
}

type ViewState = 'AUTH' | 'DASHBOARD' | 'GAME' | 'PROFILE';
```

**Tại sao cần TypeScript?**
- IDE sẽ gợi ý các properties có sẵn → code nhanh hơn
- Phát hiện lỗi ngay khi code, không cần chạy app
- Dễ refactor vì biết chắc đang làm việc với kiểu data nào

### 3. Socket.IO Client - Realtime Communication

Socket.IO cho phép client và server giao tiếp 2 chiều realtime:

```typescript
const socket = io(SOCKET_URL);

// Lắng nghe event từ server
socket.on('match_found', (data) => {
  setMatch(data);
  setView('GAME');
});

// Gửi event lên server
socket.emit('join_matchmaking', { userId, type, mode });
```

**Cách hoạt động**:
1. Client kết nối đến server qua WebSocket
2. Server có thể emit event cho 1 client cụ thể hoặc broadcast cho nhiều clients
3. Client lắng nghe (listen) events và xử lý

### 4. LocalStorage - Lưu Dữ Liệu Client-Side

```typescript
localStorage.setItem('user', JSON.stringify(userData));
const savedUser = localStorage.getItem('user');
if (savedUser) {
  const user = JSON.parse(savedUser);
}
```

**Khi nào dùng?**
- Lưu thông tin login để user không phải đăng nhập lại
- Lưu preferences (theme, language...)
- KHÔNG dùng cho dữ liệu nhạy cảm (password)

---

## 📂 Files Bạn Phụ Trách

### 1. `App.tsx` (743 dòng) - Component Chính

**Vai trò**: Brain của toàn bộ frontend, quản lý:
- State toàn cục (user, view, match, game state)
- Socket connection
- Routing giữa các views
- API calls

**Các state quan trọng**:
```typescript
const [view, setView] = useState<ViewState>('AUTH');
const [user, setUser] = useState<UserProfile | null>(null);
const [match, setMatch] = useState<MatchConfig | null>(null);
const [gameState, setGameState] = useState<GameState>({
  board: [],
  currentPlayer: 1,
  winner: 0,
  ...
});
```

**Vị trí**: `c:\xampp\htdocs\Caro\App.tsx`

### 2. `Login.tsx` (270 dòng) - Form Đăng Nhập

**Vai trò**: UI và logic cho màn hình login

**Tính năng chính**:
- Form nhập username/password
- Validation (kiểm tra rỗng)
- Gọi API login khi submit
- Hiển thị lỗi nếu sai thông tin
- Link chuyển sang trang Signup

**Vị trí**: `c:\xampp\htdocs\Caro\components\Login.tsx`

### 3. `Signup.tsx` (240 dòng) - Form Đăng Ký

**Vai trò**: UI và logic cho màn hình đăng ký

**Tính năng chính**:
- Form nhập username, password, display_name, email
- Validation (password phải >= 6 ký tự, email hợp lệ)
- Gọi API signup
- Xử lý lỗi (username đã tồn tại...)
- Link quay lại trang Login

**Vị trí**: `c:\xampp\htdocs\Caro\components\Signup.tsx`

### 4. `Header.tsx` (115 dòng) - Thanh Header

**Vai trò**: Hiển thị thông tin user ở đầu trang

**Tính năng chính**:
- Hiển thị avatar, display name
- Progress bar cho Level và Rank
- Nút Profile và Logout
- Tier badge với màu sắc đẹp mắt

**Vị trí**: `c:\xampp\htdocs\Caro\components\Header.tsx`

---

## 🔄 Luồng Hoạt Động Chi Tiết

### A. Luồng Khởi Động App

**Bước 1: User mở trang web**
- Browser load file `index.html`
- React khởi tạo component `App`
- useEffect với dependency `[]` chạy ngay lập tức

**Bước 2: Check localStorage**
```typescript
useEffect(() => {
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    try {
      const parsed = JSON.parse(savedUser);
      setUser(parsed);
      setView('DASHBOARD');
    } catch (err) {
      localStorage.removeItem('user');
    }
  }
}, []);
```
- Đọc key 'user' từ localStorage
- Nếu tồn tại: parse JSON, set user, chuyển sang DASHBOARD
- Nếu không: giữ nguyên view='AUTH' (màn hình login)

**Bước 3: Kết nối Socket**
```typescript
useEffect(() => {
  const socket = io(SOCKET_URL);
  socketRef.current = socket;

  socket.on('connect', () => console.log('Connected'));
  socket.on('match_found', (data) => { ... });
  socket.on('game_update', (data) => { ... });

  return () => socket.disconnect();
}, []);
```
- Tạo connection đến backend Socket.IO server
- Đăng ký listeners cho các events
- Cleanup khi component unmount (return function)

**Bước 4: Render UI**
- Nếu `view === 'AUTH'`: hiển thị `<Login />`
- Nếu `view === 'DASHBOARD'`: hiển thị dashboard với 2 game cards
- Nếu `view === 'GAME'`: hiển thị `<GameBoard />`

### B. Luồng Đăng Nhập

**Bước 1: User nhập thông tin**
- Component `Login.tsx` render form với 2 input fields
- User gõ username và password
- State `loginForm` được cập nhật mỗi khi user gõ

**Bước 2: User submit form**
```typescript
const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault(); // Ngăn form reload trang

  setIsLoading(true); // Hiển thị loading spinner

  try {
    const res = await fetch(`${BACKEND_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) throw new Error('Login failed');

    const data = await res.json();
    // data = { id, username, display_name, level, xp, ... }
  } catch (err) {
    alert('Tên đăng nhập hoặc mật khẩu không đúng');
  } finally {
    setIsLoading(false);
  }
};
```

**Bước 3: Gửi request đến backend**
- `POST /api/login` với body `{ username, password }`
- Backend kiểm tra database
- Nếu đúng: trả về full user profile
- Nếu sai: trả về status 401 Unauthorized

**Bước 4: Xử lý response**
```typescript
const data = await res.json();
setUser(data); // Lưu vào state
localStorage.setItem('user', JSON.stringify(data)); // Lưu vào localStorage
setView('DASHBOARD'); // Chuyển màn hình
```

**Tại sao lưu cả state và localStorage?**
- **State**: Để UI cập nhật ngay lập tức
- **LocalStorage**: Để giữ đăng nhập khi refresh trang

### C. Luồng Đăng Ký

**Bước 1: User click "Sign Up" từ màn Login**
- `setView('SIGNUP')` → App render component `<Signup />`

**Bước 2: User điền form và submit**
```typescript
const handleSignup = async () => {
  // Validation
  if (password.length < 6) {
    alert('Mật khẩu phải >= 6 ký tự');
    return;
  }

  // Call API
  const res = await fetch(`${BACKEND_URL}/api/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, display_name, email })
  });

  if (!res.ok) {
    const error = await res.json();
    alert(error.message); // VD: "Username đã tồn tại"
    return;
  }

  const data = await res.json();
  setUser(data);
  localStorage.setItem('user', JSON.stringify(data));
  setView('DASHBOARD');
};
```

**Bước 3: Backend xử lý**
- Kiểm tra username có trùng không
- Hash password bằng werkzeug.security
- Insert vào database
- Trả về user profile mới

### D. Luồng Logout

```typescript
const handleLogout = () => {
  setUser(null); // Xóa user khỏi state
  setView('AUTH'); // Quay về màn login
  localStorage.removeItem('user'); // Xóa localStorage
};
```

Đơn giản nhưng hiệu quả!

### E. Luồng Matchmaking (Phần Frontend)

**Bước 1: User click "Trận Đấu Xếp Hạng"**
```typescript
const startMatchmaking = (type: GameType, mode: GameMode) => {
  setView('MATCHMAKING'); // Hiển thị loading screen
  socketRef.current?.emit('join_matchmaking', {
    userId: user?.id,
    type, // 'tic-tac-toe' hoặc 'caro'
    mode // 'ranked' hoặc 'practice'
  });
};
```

**Bước 2: Chờ server tìm trận**
- UI hiển thị animation "Đang kết nối đến máy chủ..."
- Backend tìm đối thủ trong hàng đợi

**Bước 3: Nhận event `match_found`**
```typescript
socket.on('match_found', (data) => {
  setPlayerNumber(data.playerNumber); // 1 hoặc 2
  setMatch({
    id: data.roomId,
    type: data.gameType,
    mode: data.mode,
    opponent: data.opponent
  });
  setGameState({
    board: data.board,
    currentPlayer: 1,
    winner: 0,
    ...
  });
  setView('GAME'); // Chuyển sang màn hình game
});
```

---

## 📋 Bảng Các Hàm Quan Trọng

| Hàm | File | Tham số | Chức năng |
|-----|------|---------|-----------|
| `handleLoginWithCredentials` | App.tsx | username, password | Xử lý đăng nhập, gọi API, lưu user |
| `handleSignup` | App.tsx | username, password, display_name, email | Xử lý đăng ký tài khoản mới |
| `handleLogout` | App.tsx | - | Đăng xuất, xóa user và localStorage |
| `handleUpdateProfile` | App.tsx | updated: Partial\<UserProfile\> | Cập nhật thông tin profile |
| `startMatchmaking` | App.tsx | type, mode, difficulty? | Bắt đầu tìm trận đấu |
| `returnToDashboard` | App.tsx | - | Quay lại dashboard, refetch user profile |
| `socket.on('connect')` | App.tsx | - | Xử lý khi kết nối socket thành công |
| `socket.on('match_found')` | App.tsx | data | Nhận thông tin trận đấu từ server |
| `socket.on('game_update')` | App.tsx | data | Cập nhật board sau mỗi nước đi |
| `useEffect (localStorage check)` | App.tsx | - | Kiểm tra user đã login chưa khi app khởi động |
| `useEffect (socket setup)` | App.tsx | - | Khởi tạo socket connection |

---

## 🎤 Nội Dung Thuyết Trình

### 1. Giới Thiệu Vai Trò (1 phút)
"Em phụ trách phần **Frontend Core và Authentication**, bao gồm component App.tsx chính và toàn bộ hệ thống đăng nhập/đăng ký. Đây là phần nền tảng để các tính năng khác hoạt động."

### 2. Kiến Trúc Component App.tsx (2 phút)

**Nói**:
"Component App.tsx là trái tim của frontend với 743 dòng code. Nó quản lý toàn bộ state của ứng dụng thông qua React Hooks:

- **useState** để quản lý `view` (màn hình hiện tại), `user` (thông tin người dùng), `match` (trận đấu), và `gameState` (trạng thái bàn cờ)
- **useEffect** để kết nối Socket.IO và check localStorage khi app khởi động
- **useRef** để lưu socket connection không bị mất khi re-render"

**Demo code** (hiển thị đoạn code):
```typescript
const [view, setView] = useState<ViewState>('AUTH');
const [user, setUser] = useState<UserProfile | null>(null);
const socketRef = useRef<Socket | null>(null);

useEffect(() => {
  const socket = io(SOCKET_URL);
  socketRef.current = socket;
  // Register event listeners...
}, []);
```

### 3. Luồng Đăng Nhập (2 phút)

**Vẽ sơ đồ hoặc dùng slide**:
```
User nhập username/password
      ↓
Frontend gửi POST /api/login
      ↓
Backend check database
      ↓
Trả về user profile (id, level, xp, rank...)
      ↓
Frontend lưu user vào state + localStorage
      ↓
setView('DASHBOARD')
```

**Nói**:
"Khi user nhập thông tin và nhấn Login, em sử dụng `fetch` API để gửi POST request đến backend. Nếu thành công, backend trả về đầy đủ thông tin user bao gồm level, XP, rank points. Em lưu vào cả **state** (để UI cập nhật ngay) và **localStorage** (để giữ đăng nhập khi refresh)."

**Demo code**:
```typescript
const res = await fetch(`${BACKEND_URL}/api/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const data = await res.json();
setUser(data);
localStorage.setItem('user', JSON.stringify(data));
setView('DASHBOARD');
```

### 4. Socket.IO Integration (1.5 phút)

**Nói**:
"Để hỗ trợ realtime multiplayer, em tích hợp Socket.IO. Khi app khởi động, em tạo connection và đăng ký các listeners:

- `match_found`: Khi server ghép xong đối thủ
- `game_update`: Khi có nước đi mới
- `receive_chat`: Khi nhận tin nhắn

Mỗi khi nhận event, em cập nhật state tương ứng và React tự động re-render UI."

**Demo code**:
```typescript
socket.on('match_found', (data) => {
  setMatch({ id: data.roomId, type: data.gameType, ... });
  setGameState({ board: data.board, ... });
  setView('GAME');
});
```

### 5. Quản Lý Views (1 phút)

**Nói**:
"Em dùng state `view` để điều khiển màn hình nào hiển thị:
- `AUTH`: Màn login
- `DASHBOARD`: Màn chọn game
- `MATCHMAKING`: Màn chờ tìm trận
- `GAME`: Màn chơi game
- `PROFILE`: Màn profile cá nhân

Đây là cách routing đơn giản nhưng hiệu quả cho single-page app."

### 6. Tổng Kết (0.5 phút)

"Phần của em đảm bảo user có thể đăng nhập, đăng ký, và app luôn giữ được trạng thái đúng. Đây là nền tảng để các bạn khác xây dựng các tính năng game, chat, ranking."

---

## 💡 Tips Học Hiệu Quả

1. **Đọc code theo luồng, không đọc từ đầu file**
   - Bắt đầu từ `useEffect` → hiểu app khởi động như thế nào
   - Trace theo 1 luồng (VD: login flow) từ đầu đến cuối

2. **Chạy thử và debug**
   - Đặt `console.log` để xem state thay đổi ra sao
   - Dùng React DevTools để inspect components

3. **Hiểu TypeScript interfaces**
   - Mở file `types.ts`, đọc các interface
   - Biết `UserProfile` có gì, `GameState` có gì

4. **So sánh với ví dụ đơn giản**
   - Tạo app React nhỏ chỉ có login/logout để hiểu cơ bản
   - Sau đó áp dụng vào project này

---

Chúc bạn học tốt! Nếu có thắc mắc hãy hỏi nhóm nhé! 🚀
