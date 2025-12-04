# 📙 PHẦN HỌC CỦA NGUYỄN THỊ NHƯ NGỌC
## UI/UX Components & Real-time Chat System

---

## 🎯 Vai Trò Của Bạn

Bạn chịu trách nhiệm **giao diện người dùng và trải nghiệm tương tác** - tất cả những gì người chơi nhìn thấy và chạm vào. Bạn sẽ làm việc với các components UI phức tạp như Profile (527 dòng!), hệ thống chat realtime, replay viewer, và các modal thông tin. Đây là phần quyết định ứng dụng có đẹp mắt và dễ sử dụng hay không.

---

## 📚 Kiến Thức Cần Nắm

### 1. Component-Based Architecture

React làm việc theo mô hình component - mỗi phần UI là một component riêng biệt.

#### **Component Là Gì?**
Một component là một hàm JavaScript trả về JSX (HTML trong JS):

```typescript
function Button({ text, onClick }) {
  return (
    <button onClick={onClick} className="btn">
      {text}
    </button>
  );
}

// Sử dụng
<Button text="Click me" onClick={handleClick} />
```

#### **Props - Truyền Dữ Liệu**
Props là cách component cha truyền dữ liệu xuống con:

```typescript
// Component cha
function Parent() {
  const user = { name: "Ngọc", level: 42 };
  return <Profile user={user} onBack={goBack} />;
}

// Component con
function Profile({ user, onBack }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>Level: {user.level}</p>
      <button onClick={onBack}>Quay lại</button>
    </div>
  );
}
```

**Quy tắc quan trọng**: Props là **read-only** (không thể modify). Nếu muốn thay đổi, phải dùng state.

### 2. State và Re-rendering

State là dữ liệu nội bộ của component. Khi state thay đổi → component tự động re-render.

```typescript
function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  
  const handleSend = () => {
    setMessages([...messages, { text: inputText, sender: 'me' }]);
    setInputText(''); // Clear input
  };
  
  return (
    <div>
      {messages.map(msg => <div>{msg.text}</div>)}
      <input value={inputText} onChange={e => setInputText(e.target.value)} />
      <button onClick={handleSend}>Gửi</button>
    </div>
  );
}
```

**Khi nào re-render?**
- State thay đổi → component re-render
- Props thay đổi → component re-render
- Parent re-render → child cũng re-render

### 3. Controlled Components

Input fields nên được "kiểm soát" bởi React state:

```typescript
// ✅ Controlled
const [name, setName] = useState('');
<input value={name} onChange={e => setName(e.target.value)} />

// ❌ Uncontrolled (không theo dõi được giá trị)
<input />
```

**Lợi ích**:
- Luôn biết giá trị hiện tại
- Dễ validation
- Có thể reset value từ code

### 4. Conditional Rendering

Hiển thị UI khác nhau tùy điều kiện:

```typescript
function Profile({ user, isPublicView }) {
  return (
    <div>
      <h1>{user.name}</h1>
      
      {/* Chỉ hiển thị nếu KHÔNG phải public view */}
      {!isPublicView && (
        <button>Chỉnh sửa profile</button>
      )}
      
      {/* Ternary operator */}
      {user.level >= 100 ? (
        <Badge text="Cao thủ" />
      ) : (
        <Badge text="Tân binh" />
      )}
    </div>
  );
}
```

### 5. Lists và Keys

Render danh sách items:

```typescript
function MatchHistory({ matches }) {
  return (
    <div>
      {matches.map((match, index) => (
        <MatchCard
          key={match.id}  // ⚠️ Key PHẢI unique!
          match={match}
        />
      ))}
    </div>
  );
}
```

**Tại sao cần key?**
- React dùng key để track items
- Khi list thay đổi, React biết item nào thêm/xóa/di chuyển
- KHÔNG dùng `index` làm key nếu list có thể thay đổi thứ tự

### 6. Event Handling

Xử lý sự kiện user interaction:

```typescript
// Click
<button onClick={handleClick}>Click me</button>

// Input change
<input onChange={(e) => setName(e.target.value)} />

// Form submit
<form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
  ...
</form>

// Key press
<input onKeyDown={(e) => {
  if (e.key === 'Enter') sendMessage();
}} />
```

**Lưu ý**: Phải dùng `e.preventDefault()` với form để ngăn reload trang.

### 7. Tailwind CSS - Utility-First Styling

Project dùng Tailwind CSS để styling:

```typescript
<div className="flex items-center gap-4 p-6 bg-white rounded-xl shadow-lg">
  <img className="w-16 h-16 rounded-full" src={avatar} />
  <div className="flex-1">
    <h3 className="text-xl font-bold text-gray-800">{name}</h3>
    <p className="text-sm text-gray-500">Level {level}</p>
  </div>
</div>
```

**Các class thường dùng**:
- **Layout**: `flex`, `grid`, `items-center`, `justify-between`
- **Spacing**: `p-4` (padding), `m-4` (margin), `gap-2` (khoảng cách)
- **Size**: `w-20` (width), `h-20` (height), `max-w-md`
- **Colors**: `bg-blue-500`, `text-white`, `border-gray-300`
- **Rounding**: `rounded-xl`, `rounded-full`
- **Shadow**: `shadow-md`, `shadow-lg`

### 8. WebSocket Chat

Realtime chat dùng Socket.IO:

```typescript
// Lắng nghe tin nhắn từ server
socket.on('receive_chat', (data) => {
  setChatMessages(prev => [...prev, {
    sender: data.sender,
    message: data.message,
    timestamp: Date.now()
  }]);
});

// Gửi tin nhắn lên server
const sendMessage = (text) => {
  socket.emit('send_chat', {
    roomId: currentRoom,
    message: text,
    sender: userName,
    senderId: userId
  });
};
```

**Lưu ý bảo mật**: Phải escape HTML để tránh XSS attacks:
```typescript
// Backend làm:
import html
sanitized = html.escape(message)  // < → &lt;
```

---

## 📂 Files Bạn Phụ Trách

### 1. `Profile.tsx` (527 dòng) - Trang Profile Người Dùng

**Vai trò**: Trang cá nhân của người chơi, hiển thị stats và match history

**Các phần chính**:

#### A. User Info Section
Hiển thị avatar, display name, level, tier badge, rank, stats (wins/losses/draws)

```typescript
<div className="flex items-center gap-6">
  <img src={user.avatar_url} className="w-32 h-32 rounded-full" />
  <div>
    <h1 className="text-4xl font-black">{user.display_name}</h1>
    <div className="flex items-center gap-2">
      <span className="text-2xl font-bold">Lv {user.level}</span>
      <span className="tier-badge" style={{backgroundColor: tierColor}}>
        {tierName}
      </span>
    </div>
  </div>
</div>
```

#### B. Progress Bars
Hiển thị tiến độ Level và Rank:

```typescript
const levelProgress = getLevelProgress(user.xp, user.level);
// → { current: 1250, required: 1300, percentage: 96.15 }

<div className="relative w-full h-4 bg-gray-200 rounded-full">
  <div
    className="h-full bg-blue-500 rounded-full transition-all"
    style={{ width: `${levelProgress.percentage}%` }}
  />
</div>
<p>{levelProgress.current} / {levelProgress.required} XP</p>
```

#### C. Stats Cards
Grid hiển thị các thống kê:

```typescript
<div className="grid grid-cols-3 gap-4">
  <StatCard label="Thắng" value={user.wins} color="green" />
  <StatCard label="Thua" value={user.losses} color="red" />
  <StatCard label="Hòa" value={user.draws} color="gray" />
</div>
```

#### D. Edit Profile Form
Form chỉnh sửa thông tin (chỉ hiện khi KHÔNG phải public view):

```typescript
const [isEditing, setIsEditing] = useState(false);
const [editForm, setEditForm] = useState({
  display_name: user.display_name,
  full_name: user.full_name,
  bio: user.bio,
  avatar_url: user.avatar_url
});

const handleSave = async () => {
  const res = await fetch(`/api/profile/${user.id}`, {
    method: 'PUT',
    body: JSON.stringify(editForm)
  });
  
  if (res.ok) {
    onUpdate(editForm);  // Update parent state
    setIsEditing(false);
  }
};
```

#### E. Match History
Danh sách các trận đã chơi với pagination:

```typescript
const [matchHistory, setMatchHistory] = useState<MatchHistory[]>([]);
const [page, setPage] = useState(1);
const itemsPerPage = 10;

useEffect(() => {
  fetch(`/api/history/${user.id}`)
    .then(res => res.json())
    .then(data => setMatchHistory(data));
}, [user.id]);

// Pagination
const displayedMatches = matchHistory.slice(
  (page - 1) * itemsPerPage,
  page * itemsPerPage
);

{displayedMatches.map(match => (
  <MatchCard
    key={match.id}
    match={match}
    onReplay={() => onReplayMatch(match.id)}
  />
))}
```

**Vị trí**: `c:\xampp\htdocs\Caro\components\Profile.tsx`

### 2. `ChatBox.tsx` (160 dòng) - Live Chat

**Vai trò**: Chat realtime trong trận đấu

**Tính năng**:
- Hiển thị danh sách messages
- Auto-scroll xuống tin nhắn mới nhất
- Input để gõ tin nhắn (max 200 ký tự)
- Phân biệt tin nhắn của mình và đối thủ

**Code quan trọng**:

```typescript
function ChatBox({ messages, currentUserId, onSendMessage, disabled }) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSend = () => {
    if (inputText.trim() && inputText.length <= 200) {
      onSendMessage(inputText);
      setInputText('');
    }
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.senderId === currentUserId ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`px-4 py-2 rounded-xl max-w-[80%] ${
              msg.senderId === currentUserId
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-800'
            }`}>
              <p className="text-xs font-semibold">{msg.sender}</p>
              <p>{msg.message}</p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <input
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            maxLength={200}
            disabled={disabled}
            placeholder="Nhập tin nhắn..."
            className="flex-1 px-4 py-2 rounded-xl border"
          />
          <button
            onClick={handleSend}
            disabled={disabled || !inputText.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-xl"
          >
            Gửi
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {inputText.length} / 200
        </p>
      </div>
    </div>
  );
}
```

**Vị trí**: `c:\xampp\htdocs\Caro\components\ChatBox.tsx`

### 3. `ReplayBoard.tsx` (171 dòng) - Replay Viewer

**Vai trò**: Xem lại trận đấu với controls (prev, next, first, last)

**Tính năng**:
- Load moves từ database (JSON array)
- Step through moves với buttons
- Hiển thị board tại mỗi bước
- Highlight move hiện tại

**Code quan trọng**:

```typescript
function ReplayBoard({ matchData, onBack }) {
  const [currentStep, setCurrentStep] = useState(0);
  const moves = JSON.parse(matchData.moves);
  
  // Rebuild board tại step hiện tại
  const board = useMemo(() => {
    const emptyBoard = createEmptyBoard(matchData.game_type);
    for (let i = 0; i <= currentStep; i++) {
      const move = moves[i];
      if (move) {
        emptyBoard[move.r][move.c] = move.player;
      }
    }
    return emptyBoard;
  }, [currentStep, moves]);
  
  const goNext = () => setCurrentStep(Math.min(currentStep + 1, moves.length - 1));
  const goPrev = () => setCurrentStep(Math.max(currentStep - 1, 0));
  const goFirst = () => setCurrentStep(0);
  const goLast = () => setCurrentStep(moves.length - 1);
  
  return (
    <div>
      <GameBoard
        board={board}
        type={matchData.game_type}
        onCellClick={() => {}}  // Read-only
        disabled={true}
        lastMove={moves[currentStep]}
      />
      
      <div className="flex gap-2 justify-center mt-4">
        <button onClick={goFirst}>⏮ First</button>
        <button onClick={goPrev}>◀ Prev</button>
        <span>{currentStep + 1} / {moves.length}</span>
        <button onClick={goNext}>Next ▶</button>
        <button onClick={goLast}>Last ⏭</button>
      </div>
    </div>
  );
}
```

**Vị trí**: `c:\xampp\htdocs\Caro\components\ReplayBoard.tsx`

### 4. `RankInfoModal.tsx` (220 dòng) - Modal Thông Tin Rank

**Vai trò**: Modal hiển thị chi tiết hệ thống xếp hạng

**Tính năng**:
- Giải thích cách tính XP và Rank Points
- Bảng 10 danh hiệu (tiers)
- Bảng 4 hạng (ranks)
- Bảng 500 levels với XP requirements

**Vị trí**: `c:\xampp\htdocs\Caro\components\RankInfoModal.tsx`

### 5. `Button.tsx`, `LevelSelector.tsx`, `PracticeDifficultySelector.tsx`

Các components UI nhỏ hơn để tái sử dụng.

---

## 🔄 Luồng Hoạt Động Chi Tiết

### A. Luồng Hiển Thị Profile

**Bước 1: User click "Profile" trên Header**
```typescript
// In App.tsx
<Header onProfile={() => setView('PROFILE')} />
```

**Bước 2: App render Profile component**
```typescript
{view === 'PROFILE' && (
  <Profile
    user={user}
    onBack={() => setView('DASHBOARD')}
    onUpdate={handleUpdateProfile}
    socketURL={SOCKET_URL}
  />
)}
```

**Bước 3: Profile fetch match history**
```typescript
useEffect(() => {
  const fetchMatchHistory = async () => {
    const res = await fetch(`${socketURL}/api/history/${user.id}`);
    const data = await res.json();
    setMatchHistory(data);
  };
  fetchMatchHistory();
}, [user.id]);
```

**Bước 4: Render UI với dữ liệu**
- User info section với avatar, name, level
- Progress bars cho XP và Rank
- Stats cards (wins/losses/draws)
- Match history list

### B. Luồng Chỉnh Sửa Profile

**Bước 1: User click "Edit Profile"**
```typescript
setIsEditing(true);
```

**Bước 2: Show form với values hiện tại**
```typescript
<input
  value={editForm.display_name}
  onChange={e => setEditForm({...editForm, display_name: e.target.value})}
/>
```

**Bước 3: User sửa và click "Save"**
```typescript
const handleSave = async () => {
  const res = await fetch(`/api/profile/${user.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(editForm)
  });
  
  if (res.ok) {
    onUpdate(editForm);  // Gọi callback từ App.tsx
    setIsEditing(false);
  }
};
```

**Bước 4: App.tsx cập nhật user state**
```typescript
const handleUpdateProfile = async (updated) => {
  // Refetch full user profile
  const res = await fetch(`/api/user/${user.id}`);
  const freshUser = await res.json();
  setUser(freshUser);
  localStorage.setItem('user', JSON.stringify(freshUser));
};
```

### C. Luồng Chat Realtime

**Bước 1: User gõ tin nhắn và nhấn Enter**
```typescript
const handleKeyDown = (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    handleSend();
  }
};

const handleSend = () => {
  if (inputText.trim()) {
    onSendMessage(inputText);  // Callback từ App.tsx
    setInputText('');
  }
};
```

**Bước 2: App.tsx emit socket event**
```typescript
const handleSendChatMessage = (message) => {
  socketRef.current?.emit('send_chat', {
    roomId: match.id,
    message: message.trim(),
    sender: user.display_name,
    senderId: user.id
  });
};
```

**Bước 3: Backend broadcast tin nhắn**
```python
# In sockets/game.py
@socketio.on('send_chat')
def handle_chat(data):
    room_id = data['roomId']
    message = html.escape(data['message'])  # Sanitize
    
    emit('receive_chat', {
        'sender': data['sender'],
        'senderId': data['senderId'],
        'message': message
    }, room=room_id)
```

**Bước 4: Tất cả clients trong room nhận tin**
```typescript
// In App.tsx (useEffect)
socket.on('receive_chat', (data) => {
  setChatMessages(prev => [...prev, {
    sender: data.sender,
    senderId: data.senderId,
    message: data.message,
    timestamp: Date.now()
  }]);
});
```

**Bước 5: ChatBox re-render và auto-scroll**
```typescript
useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);
```

### D. Luồng Xem Replay

**Bước 1: User click nút "Xem lại" ở Match History**
```typescript
<button onClick={() => onReplayMatch(match.id)}>
  Xem lại
</button>
```

**Bước 2: App.tsx fetch match data**
```typescript
const handleReplay = async (matchId) => {
  const res = await fetch(`/api/match/${matchId}`);
  const data = await res.json();
  // data = { id, player1_id, player2_id, moves: "[{r:0,c:0,player:1}, ...]", ... }
  
  setReplayData(data);
  setView('REPLAY');
};
```

**Bước 3: Render ReplayBoard**
```typescript
{view === 'REPLAY' && (
  <ReplayBoard
    matchData={replayData}
    onBack={() => setView('PROFILE')}
  />
)}
```

**Bước 4: ReplayBoard parse moves và rebuild board**
```typescript
const moves = JSON.parse(matchData.moves);
// moves = [{r:0,c:0,player:1}, {r:1,c:1,player:2}, ...]

const board = useMemo(() => {
  const emptyBoard = createEmptyBoard();
  for (let i = 0; i <= currentStep; i++) {
    const move = moves[i];
    emptyBoard[move.r][move.c] = move.player;
  }
  return board;
}, [currentStep]);
```

**Bước 5: User control với buttons**
```typescript
<button onClick={() => setCurrentStep(prev => prev + 1)}>Next</button>
```

---

## 📋 Bảng Các Hàm Quan Trọng

| Hàm | File | Tham số | Chức năng |
|-----|------|---------|-----------|
| `fetchMatchHistory` | Profile.tsx | - | Lấy lịch sử trận đấu từ API |
| `handleUpdateProfile` | Profile.tsx | - | Gửi PUT request cập nhật profile |
| `handleChangePassword` | Profile.tsx | - | Đổi mật khẩu (gọi API /api/change-password) |
| `getRankColor` | Profile.tsx | level: string | Tính màu rank badge dựa vào level |
| `handleSend` | ChatBox.tsx | - | Gửi tin nhắn qua callback onSendMessage |
| `handleKeyDown` | ChatBox.tsx | e: KeyboardEvent | Bắt phím Enter để gửi tin nhắn |
| `goNext` / `goPrev` | ReplayBoard.tsx | - | Chuyển bước replay |
| `goFirst` / `goLast` | ReplayBoard.tsx | - | Nhảy đến đầu/cuối replay |
| `useMemo (board)` | ReplayBoard.tsx | currentStep | Rebuild board tại step hiện tại |

---

## 🎤 Nội Dung Thuyết Trình

### 1. Giới Thiệu Vai Trò (1 phút)
"Em phụ trách phần **UI/UX Components và Chat Realtime**, tức là tất cả giao diện người dùng tương tác. Bao gồm:
- Trang Profile với stats và match history
- Chat box realtime trong game
- Replay viewer để xem lại trận đấu
- Các modal và components UI khác"

### 2. Component Profile.tsx - Complexity Cao Nhất (2.5 phút)

**Demo slides với screenshots**:

"Component Profile.tsx có 527 dòng, là component phức tạp nhất em phụ trách. Nó có 5 phần chính:

**1. User Info Section**: Hiển thị avatar, tên, level, tier badge, và hạng hiện tại. Em sử dụng Tailwind CSS để tạo layout flexbox đẹp mắt.

**2. Progress Bars**: Hai thanh tiến trình - một cho Level (dựa vào XP), một cho Rank (dựa vào Rank Points). Em dùng hàm `getLevelProgress` và `getRankProgress` từ utils để tính phần trăm.

**3. Stats Grid**: Grid 3 cột hiển thị số trận thắng/thua/hòa với màu sắc rõ ràng.

**4. Edit Profile Form**: Chỉ hiện khi người dùng xem profile của chính mình (không phải public view). Dùng state `isEditing` để toggle giữa view mode và edit mode.

**5. Match History**: Danh sách các trận đã chơi, có pagination để không load hết 1000 trận cùng lúc. Mỗi match card có nút 'Xem lại' để trigger replay."

**Demo code**:
```typescript
const [isEditing, setIsEditing] = useState(false);

{!isPublicView && (
  <button onClick={() => setIsEditing(true)}>
    Chỉnh sửa
  </button>
)}
```

### 3. Chat Realtime (2 phút)

"Chat box sử dụng Socket.IO để realtime communication. Có 3 features chính:

**1. Auto-scroll**: Mỗi khi có tin nhắn mới, em dùng `useRef` để scroll xuống bottom tự động.

**2. Character Limit**: Giới hạn 200 ký tự và hiển thị counter `150/200`.

**3. Enter to Send**: User nhấn Enter để gửi, Shift+Enter để xuống dòng.

Về bảo mật, backend đã escape HTML để tránh XSS attacks."

**Demo code**:
```typescript
const messagesEndRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);
```

### 4. Replay Viewer (1.5 phút)

"Replay viewer cho phép xem lại trận đấu bằng cách step through moves:

- Fetch match data từ `/api/match/:id`
- Parse moves từ JSON string: `[{r:0,c:0,player:1}, ...]`
- Rebuild board từ đầu đến step hiện tại bằng `useMemo`
- 4 buttons: First, Prev, Next, Last để navigate

Em dùng `useMemo` để avoid rebuild board mỗi lần render - chỉ rebuild khi `currentStep` thay đổi."

**Demo code**:
```typescript
const board = useMemo(() => {
  const emptyBoard = createEmptyBoard();
  for (let i = 0; i <= currentStep; i++) {
    const move = moves[i];
    emptyBoard[move.r][move.c] = move.player;
  }
  return board;
}, [currentStep, moves]);
```

### 5. UI/UX Design Principles (1 phút)

"Em áp dụng các nguyên tắc UI/UX:

- **Consistency**: Tất cả buttons đều có style giống nhau
- **Feedback**: Loading states, hover effects, transitions
- **Accessibility**: Color contrast đủ, font size dễ đọc
- **Responsive**: Dùng Tailwind breakpoints (`sm:`, `md:`, `lg:`) để responsive trên mobile"

### 6. Tổng Kết (0.5 phút)

"Phần UI/UX quyết định trải nghiệm người dùng. Em đảm bảo giao diện đẹp, dễ dùng, và mượt mà."

---

## 💡 Tips Học Hiệu Quả

1. **Chạy app và inspect UI**
   - Dùng React DevTools để xem component tree
   - Inspect mỗi component để hiểu props và state

2. **Thử edit Profile**
   - Xem form hoạt động ra sao
   - Trace code từ onClick → API call → re-render

3. **Test chat**
   - Mở 2 tabs, login 2 user khác nhau
   - Chat và xem messages realtime

4. **Học Tailwind**
   - Đọc docs: https://tailwindcss.com/docs
   - Thử thay đổi classes để hiểu effect

Chúc bạn học tốt! UI/UX là phần thú vị nhất! 🎨
