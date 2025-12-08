import streamlit as st
import pandas as pd
import os
import random
import hashlib
from datetime import datetime, date, timedelta
import time
import uuid

# =====================================================
# 🎨 0. 世界級 UI 設定
# =====================================================

st.set_page_config(
    # ... (上面是 import 和 st.set_page_config) ...

st.set_page_config(
    page_title="LingoLove - 兩人專屬英語小屋",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 👇👇👇 請插入這段 CSS 代碼來隱藏所有標記 👇👇👇
st.markdown("""
    <style>
        /* 隱藏右上角漢堡選單 (皇冠/選單) */
        #MainMenu {visibility: hidden;}
        
        /* 隱藏頁尾 "Made with Streamlit" (創作者資訊) */
        footer {visibility: hidden;}
        
        /* 隱藏上方彩色裝飾條 */
        header {visibility: hidden;}
        
        /* 隱藏右下角的 "Deploy" 按鈕 (如果有的話) */
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# ... (下面接著 st.markdown 你的其他 CSS ...)
    page_title="LingoLove - 兩人專屬英語小屋",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Quicksand:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans TC', 'Quicksand', sans-serif;
        background-color: #FAFAFA;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div.block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* 卡片特效 */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px -10px rgba(0,0,0,0.12);
    }

    .hero-card {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        border-radius: 24px;
        padding: 32px;
        color: #5d5d5d;
        text-align: center;
        box-shadow: 0 20px 40px -10px rgba(255, 154, 158, 0.4);
        margin-bottom: 30px;
        animation: slideDown 0.8s ease-out;
    }
    .hero-card h1 {
        margin: 0;
        font-size: 2.2rem;
        color: #4a4a4a;
        font-weight: 700;
    }

    /* 故事模式樣式 */
    .story-container {
        background-color: #fff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #a29bfe;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .vocab-tag {
        display: inline-block;
        background-color: #e0e0e0;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 3px;
        font-size: 0.9em;
        font-weight: bold;
        color: #555;
    }

    /* 規則說明框樣式 */
    .rule-box-blue {
        background-color: #e3f2fd; padding: 15px; border-radius: 12px;
        border-left: 6px solid #2196f3; margin-bottom: 20px; color: #0d47a1;
    }
    .rule-box-pink {
        background-color: #fce4ec; padding: 15px; border-radius: 12px;
        border-left: 6px solid #e91e63; margin-bottom: 20px; color: #880e4f;
    }
    .rule-box-orange {
        background-color: #fff3e0; padding: 15px; border-radius: 12px;
        border-left: 6px solid #ff9800; margin-bottom: 20px; color: #e65100;
    }

    /* 情書樣式 */
    .secret-msg-locked {
        background: #f1f3f5;
        border-left: 6px solid #adb5bd;
        padding: 16px;
        border-radius: 12px;
        color: #868e96;
        font-style: italic;
        margin-bottom: 12px;
    }
    .secret-msg-unlocked {
        background: #e3fafc;
        border-left: 6px solid #66d9e8;
        padding: 16px;
        border-radius: 12px;
        color: #0c8599;
        margin-bottom: 12px;
    }

    /* 寵物動畫 */
    .pet-container {
        text-align: center;
        padding: 20px;
        background: radial-gradient(circle, #fff0f6 0%, #fff 70%);
        border-radius: 50%;
        width: 140px;
        height: 140px;
        margin: 0 auto 15px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 70px;
        box-shadow: inset 0 0 30px rgba(255, 182, 193, 0.3);
        animation: pulse 3s infinite;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }

    .stat-number { font-size: 28px; font-weight: 800; color: #ff6b81; font-family: 'Quicksand', sans-serif; }
    .small-muted { font-size: 13px; color: #a4b0be; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 💾 1. 資料庫與檔案管理
# =====================================================

USER_DB_FILE    = "users_v7.csv"
ROOM_DB_FILE    = "rooms_v7.csv"
MESSAGE_DB_FILE = "messages_v7.csv"
MEMORY_DB_FILE  = "memories_v7.csv"
QUEST_DB_FILE   = "quests_v7.csv"
GAME_DATA_FILE_PREFIX = "lingo_data_"
IMAGES_DIR      = "images"

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

AVATARS = [
    "🧸","🐻","🐼","🐨","🐯","🦊","🐱","🐶","🦁","🐰",
    "🦋","🌸","🌙","⭐","🍑","🍓","🍒","🧁","☕","🎧"
]

def load_csv(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df
    return pd.read_csv(file_path)

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

def save_uploaded_image(uploaded_file):
    if uploaded_file is None:
        return None
    file_ext = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(IMAGES_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# --- 使用者 ---
def get_user(username):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"])
    df = df.astype(str)
    user = df[df["username"] == str(username)]
    return user.iloc[0].to_dict() if not user.empty else None

def create_user(username, password, nickname, gender, avatar):
    cols = ["username","password","nickname","gender","room_id","avatar","join_date"]
    df = load_csv(USER_DB_FILE, cols)
    if username in df["username"].astype(str).values:
        return False, "帳號已存在"
    new_user = pd.DataFrame([{
        "username": username, "password": hash_password(password), "nickname": nickname,
        "gender": gender, "room_id": "None", "avatar": avatar, "join_date": date.today().isoformat()
    }])
    save_csv(pd.concat([df, new_user], ignore_index=True), USER_DB_FILE)
    return True, "註冊成功！"

def update_user_room(username, new_room_id):
    cols = ["username","password","nickname","gender","room_id","avatar","join_date"]
    df = load_csv(USER_DB_FILE, cols)
    df.loc[df["username"].astype(str) == str(username), "room_id"] = str(new_room_id)
    save_csv(df, USER_DB_FILE)

def get_room_users(room_id):
    cols = ["username","password","nickname","gender","room_id","avatar","join_date"]
    df = load_csv(USER_DB_FILE, cols)
    return df[df["room_id"].astype(str) == str(room_id)]

# --- 房間 ---
def check_room_exists(room_id):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary"])
    return str(room_id) in df["room_id"].astype(str).values

def create_room(room_id, password, room_name, anniversary):
    cols = ["room_id","room_name","password","created_at","anniversary"]
    df = load_csv(ROOM_DB_FILE, cols)
    if str(room_id) in df["room_id"].astype(str).values:
        return False, "房號已被使用"
    new_room = pd.DataFrame([{
        "room_id": str(room_id), "room_name": room_name, "password": hash_password(password),
        "created_at": datetime.now().isoformat(), "anniversary": anniversary
    }])
    save_csv(pd.concat([df, new_room], ignore_index=True), ROOM_DB_FILE)
    return True, "房間創建成功"

def verify_room_password(room_id, password):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary"])
    room = df[df["room_id"].astype(str) == str(room_id)]
    if room.empty: return False
    return room.iloc[0]["password"] == hash_password(password)

def get_room_info(room_id):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary"])
    room = df[df["room_id"].astype(str) == str(room_id)]
    return room.iloc[0].to_dict() if not room.empty else {}

# --- 遊戲數據 ---
def get_game_df(room_id):
    f = f"{GAME_DATA_FILE_PREFIX}{room_id}.csv"
    return load_csv(f, ["時間","使用者名稱","性別","動作","項目","點數"])

def save_action(room_id, user_name, gender, action_type, item, points):
    f = f"{GAME_DATA_FILE_PREFIX}{room_id}.csv"
    df = load_csv(f, ["時間","使用者名稱","性別","動作","項目","點數"])
    new_rec = pd.DataFrame([{
        "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "使用者名稱": user_name, "性別": gender, "動作": action_type, "項目": item, "點數": points
    }])
    save_csv(pd.concat([df, new_rec], ignore_index=True), f)

def has_today_action(df, name, action_type):
    if df.empty: return False
    today = datetime.now().strftime("%Y-%m-%d")
    return ((df["使用者名稱"]==name) & (df["動作"]==action_type) & (df["時間"].astype(str).str.startswith(today))).any()

def reset_room_data(room_id):
    f = f"{GAME_DATA_FILE_PREFIX}{room_id}.csv"
    pd.DataFrame(columns=["時間","使用者名稱","性別","動作","項目","點數"]).to_csv(f, index=False)

def can_afford(current_score, cost):
    return current_score + cost >= 0

# --- 情書 / 回憶 ---
def send_secret_message(room_id, sender, content, image_path=None):
    cols = ["room_id","sender","content","status","timestamp","likes", "image_path"]
    df = load_csv(MESSAGE_DB_FILE, cols)
    new_msg = pd.DataFrame([{
        "room_id": str(room_id), "sender": sender, "content": content, "status": "LOCKED",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "likes": 0,
        "image_path": str(image_path) if image_path else "None"
    }])
    save_csv(pd.concat([df, new_msg], ignore_index=True), MESSAGE_DB_FILE)

def get_room_messages(room_id):
    df = load_csv(MESSAGE_DB_FILE, ["room_id","sender","content","status","timestamp","likes", "image_path"])
    return df[df["room_id"].astype(str) == str(room_id)].sort_values("timestamp", ascending=False)

def unlock_message(room_id, timestamp):
    df = load_csv(MESSAGE_DB_FILE, ["room_id","sender","content","status","timestamp","likes", "image_path"])
    cond = (df["room_id"].astype(str) == str(room_id)) & (df["timestamp"] == str(timestamp))
    df.loc[cond, "status"] = "OPEN"
    save_csv(df, MESSAGE_DB_FILE)

def like_message(room_id, timestamp):
    df = load_csv(MESSAGE_DB_FILE, ["room_id","sender","content","status","timestamp","likes", "image_path"])
    cond = (df["room_id"].astype(str) == str(room_id)) & (df["timestamp"] == str(timestamp))
    df.loc[cond, "likes"] = df.loc[cond, "likes"].fillna(0).astype(int) + 1
    save_csv(df, MESSAGE_DB_FILE)

def add_memory(room_id, title, desc, mood, image_path=None):
    cols = ["room_id","date","title","desc","mood", "image_path"]
    df = load_csv(MEMORY_DB_FILE, cols)
    new_mem = pd.DataFrame([{
        "room_id": str(room_id), "date": date.today().isoformat(), "title": title, "desc": desc, "mood": mood,
        "image_path": str(image_path) if image_path else "None"
    }])
    save_csv(pd.concat([df, new_mem], ignore_index=True), MEMORY_DB_FILE)

def get_memories(room_id):
    df = load_csv(MEMORY_DB_FILE, ["room_id","date","title","desc","mood", "image_path"])
    return df[df["room_id"].astype(str) == str(room_id)].sort_values("date", ascending=False)

# ---------- 每日任務 ----------

def init_quest_db():
    if not os.path.exists(QUEST_DB_FILE):
        pd.DataFrame(columns=["room_id","date","quest_key","desc","reward","emoji"]).to_csv(QUEST_DB_FILE, index=False)

def ensure_today_quests(room_id):
    init_quest_db()
    df = load_csv(QUEST_DB_FILE, ["room_id","date","quest_key","desc","reward","emoji"])
    today = date.today().isoformat()
    if not ((df["room_id"] == str(room_id)) & (df["date"] == today)).any():
        # 使用 QUEST_POOL 全域變數
        selected = random.sample(QUEST_POOL, 3)
        new_rows = []
        for q in selected:
            new_rows.append({
                "room_id": str(room_id), "date": today, "quest_key": q["type"],
                "desc": q["desc"], "reward": q["reward"], "emoji": q["emoji"]
            })
        save_csv(pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True), QUEST_DB_FILE)

def get_today_quests(room_id):
    init_quest_db()
    df = load_csv(QUEST_DB_FILE, ["room_id","date","quest_key","desc","reward","emoji"])
    today = date.today().isoformat()
    return df[(df["room_id"].astype(str) == str(room_id)) & (df["date"] == today)]

# =====================================================
# 🧠 2. 遊戲內容 (Stories & Quests)
# =====================================================

def get_pet_status(score):
    if score < 500:   return "🥚", "神秘的蛋", "正在孵化中... 請多餵我英文單字！"
    if score < 1500:  return "🐣", "呆萌小雞", "世界好大喔！我想要學更多單字！"
    if score < 3000:  return "🦉", "博學貓頭鷹", "Hoo-Hoo! 我已經變聰明了！"
    if score < 5000:  return "🦄", "夢幻獨角獸", "你們的愛讓我充滿了魔力！"
    return "🐲", "傳奇神龍", "你們是世界最強的英語情侶檔！"

# 📚 故事庫
STORY_BANK = [
    {
        "id": "story_001",
        "title": "Rainy Day Coffee (雨天咖啡)",
        "image": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=600&q=80",
        "content_en": "It was a rainy afternoon. Alice ran into a small coffee shop to hide from the rain. She ordered a hot latte. Suddenly, a man walked in, shaking his wet umbrella. Their eyes met, and time seemed to stop.",
        "content_ch": "這是一個下雨的下午。Alice 跑進一家小咖啡廳躲雨。她點了一杯熱拿鐵。突然，一個男人走了進來，甩著他濕淋淋的雨傘。他們的眼神交會，時間彷彿靜止了。",
        "vocab": [
            {"word": "Shelter", "ch": "庇護所/躲避處"},
            {"word": "Latte", "ch": "拿鐵"},
            {"word": "Suddenly", "ch": "突然地"},
            {"word": "Umbrella", "ch": "雨傘"}
        ]
    },
    {
        "id": "story_002",
        "title": "The Lost Puppy (迷路的小狗)",
        "image": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=600&q=80",
        "content_en": "Ben found a small puppy shivering under a bench in the park. It looked hungry and scared. Ben gently picked it up and decided to take it home. He named it 'Lucky'.",
        "content_ch": "Ben 在公園的長椅下發現了一隻發抖的小狗。它看起來又餓又害怕。Ben 溫柔地抱起它，決定帶它回家。他給它取名叫「Lucky」。",
        "vocab": [
            {"word": "Shiver", "ch": "發抖"},
            {"word": "Bench", "ch": "長椅"},
            {"word": "Scared", "ch": "害怕的"},
            {"word": "Gently", "ch": "溫柔地"}
        ]
    },
    {
        "id": "story_003",
        "title": "Starry Night (星空之夜)",
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=600&q=80",
        "content_en": "They drove up the mountain to see the stars. The sky was clear and full of sparkling lights. He held her hand and whispered, 'You are brighter than any star.'",
        "content_ch": "他們開車上山去看星星。天空很晴朗，滿是閃爍的光點。他握住她的手，輕聲說：「你比任何星星都耀眼。」",
        "vocab": [
            {"word": "Mountain", "ch": "山"},
            {"word": "Sparkling", "ch": "閃爍的"},
            {"word": "Whisper", "ch": "低語"},
            {"word": "Bright", "ch": "明亮的"}
        ]
    }
]

# 🗂️ 獨立單字庫 (用於首頁每日情話 & 情書解鎖)
# 這裡必須包含 sentence 欄位，才不會報錯！
CONTENT_BANK = [
    {"word": "Cherish", "ch": "珍惜", "sentence": "I cherish every moment with you.", "context": "深情告白"},
    {"word": "Cuddle", "ch": "擁抱", "sentence": "Let's cuddle and watch a movie.", "context": "想討抱抱"},
    {"word": "Support", "ch": "支持", "sentence": "I support you no matter what.", "context": "互相打氣"},
    {"word": "Trust", "ch": "信任", "sentence": "I trust you completely.", "context": "內心話"},
    {"word": "Destiny", "ch": "命運", "sentence": "Meeting you was my destiny.", "context": "浪漫時刻"},
    {"word": "Forgive", "ch": "原諒", "sentence": "Please forgive me.", "context": "道歉求和"},
    {"word": "Adore", "ch": "愛慕", "sentence": "I absolutely adore you.", "context": "表達愛意"},
    {"word": "Promise", "ch": "承諾", "sentence": "I promise to always be there.", "context": "許下承諾"},
    {"word": "Spark", "ch": "火花", "sentence": "You still give me that spark.", "context": "熱戀感"},
    {"word": "Eternity", "ch": "永恆", "sentence": "I want to be with you for all eternity.", "context": "求婚"},
    {"word": "Adventure", "ch": "冒險", "sentence": "Life with you is my favorite adventure.", "context": "旅行"},
]

DATE_IDEAS = [
    {"title": "🎬 電影馬拉松", "desc": "準備爆米花和飲料，在家連看三部電影！"},
    {"title": "🍳 廚神大賽", "desc": "用冰箱現有食材，一人做一道創意料理。"},
    {"title": "🚶 城市漫遊", "desc": "不看地圖，隨意搭公車去一個陌生的地方冒險。"},
    {"title": "🧺 公園野餐", "desc": "買點三明治，去草地上躺著發呆看雲。"},
    {"title": "🎮 遊戲對戰", "desc": "一起玩桌遊、Switch 或手遊，輸的要按摩！"},
]

QUEST_POOL = [
    {"type": "quest_compliment", "desc": "給對方一個真誠的讚美", "reward": 25, "emoji": "💝"},
    {"type": "quest_photo",      "desc": "拍一張今天的合照或自拍", "reward": 30, "emoji": "📸"},
    {"type": "quest_surprise",   "desc": "給對方一個小驚喜",      "reward": 40, "emoji": "🎁"},
    {"type": "quest_call",       "desc": "通話或視訊至少 10 分鐘", "reward": 35, "emoji": "📞"},
    {"type": "quest_date",       "desc": "一起計畫下一次約會",    "reward": 50, "emoji": "💑"},
]

def get_weekly_story():
    year, week, _ = date.today().isocalendar()
    random.seed(year * 100 + week)
    story = random.choice(STORY_BANK)
    random.seed()
    return story

def get_today_word():
    random.seed(date.today().toordinal())
    res = random.choice(CONTENT_BANK)
    random.seed()
    return res

def ensure_today_quests(room_id):
    cols = ["room_id","date","quest_key","desc","reward","emoji"]
    df = load_csv(QUEST_DB_FILE, cols)
    today = date.today().isoformat()
    if not ((df["room_id"] == str(room_id)) & (df["date"] == today)).any():
        selected = random.sample(QUEST_POOL, 3)
        new_rows = []
        for q in selected:
            new_rows.append({
                "room_id": str(room_id), "date": today, "quest_key": q["type"],
                "desc": q["desc"], "reward": q["reward"], "emoji": q["emoji"]
            })
        save_csv(pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True), QUEST_DB_FILE)

def get_today_quests(room_id):
    df = load_csv(QUEST_DB_FILE, ["room_id","date","quest_key","desc","reward","emoji"])
    today = date.today().isoformat()
    return df[(df["room_id"].astype(str) == str(room_id)) & (df["date"] == today)]

# =====================================================
# 📱 3. 介面呈現 (UI)
# =====================================================

if "user_session" not in st.session_state: st.session_state.user_session = None

# 初始化測驗狀態
if "quiz_phase" not in st.session_state: st.session_state.quiz_phase = "reading"
if "quiz_q_index" not in st.session_state: st.session_state.quiz_q_index = 0
if "quiz_score_sheet" not in st.session_state: st.session_state.quiz_score_sheet = []
if "quiz_start_time" not in st.session_state: st.session_state.quiz_start_time = None

# A. 登入
if st.session_state.user_session is None:
    st.markdown("<h1 style='text-align:center;'>💖 LingoLove</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;'>v10.2 Ultimate Fix</p>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔑 登入", "✨ 註冊"])
    
    with t1:
        u = st.text_input("帳號", key="l_u")
        p = st.text_input("密碼", type="password", key="l_p")
        if st.button("登入", use_container_width=True, type="primary"):
            user = get_user(u)
            if user and user["password"] == hash_password(p):
                st.session_state.user_session = user
                st.toast(f"歡迎回來，{user['nickname']}！", icon="👋")
                time.sleep(0.5)
                st.rerun()
            else: st.error("帳號或密碼錯誤")
    
    with t2:
        ru = st.text_input("設定帳號", key="r_u")
        rp = st.text_input("設定密碼", type="password", key="r_p")
        rn = st.text_input("你的暱稱", key="r_n")
        rg = st.radio("角色", ["👦 男生", "👧 女生"], horizontal=True)
        ra = st.selectbox("選擇頭像", AVATARS)
        if st.button("註冊", use_container_width=True):
            if ru and rp and rn:
                ok, msg = create_user(ru, rp, rn, rg, ra)
                if ok: 
                    st.success(msg)
                else: 
                    st.error(msg)
            else: st.warning("請填寫完整")

# B. 主程式
else:
    me = st.session_state.user_session
    room_id = str(me["room_id"])
    
    # 大廳
    if room_id == "None" or room_id == "nan":
        st.markdown(f"## Hi, {me['nickname']} {me['avatar']}")
        st.info("🏠 歡迎來到 LingoLove！請建立或加入小屋。")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🔨 創建小屋")
                n_rid = st.text_input("設定房號")
                n_pass = st.text_input("設定密碼")
                n_name = st.text_input("小屋名稱 (選填)")
                n_anni = st.date_input("紀念日", value=None)
                if st.button("創建", use_container_width=True, type="primary"):
                    if n_rid and n_pass:
                        anni_str = n_anni.strftime("%Y-%m-%d") if n_anni else ""
                        ok, msg = create_room(n_rid, n_pass, n_name or f"{n_rid}的小屋", anni_str)
                        if ok:
                            update_user_room(me["username"], n_rid)
                            st.session_state.user_session["room_id"] = n_rid
                            st.toast("創建成功！", icon="🎉")
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                    else: st.warning("請輸入房號與密碼")
        with c2:
            with st.container(border=True):
                st.subheader("🔑 加入小屋")
                j_rid = st.text_input("輸入房號")
                j_pass = st.text_input("輸入密碼", type="password")
                if st.button("加入", use_container_width=True):
                    if not check_room_exists(j_rid): st.error("房間不存在")
                    elif not verify_room_password(j_rid, j_pass): st.error("密碼錯誤")
                    elif len(get_room_users(j_rid)) >= 2: st.error("房間已滿")
                    else:
                        update_user_room(me["username"], j_rid)
                        st.session_state.user_session["room_id"] = j_rid
                        st.toast("加入成功！", icon="🏠")
                        time.sleep(1)
                        st.rerun()
        st.divider()
        if st.button("登出", key="btn_logout_lobby"):
            st.session_state.user_session = None
            st.rerun()

    # 小屋
    else:
        r_info = get_room_info(room_id)
        room_name = r_info.get("room_name", "愛的小屋")
        r_users = get_room_users(room_id)
        partner = r_users[r_users["username"] != str(me["username"])]
        if not partner.empty:
            partner = partner.iloc[0].to_dict()
            p_name, p_avatar, p_gender = partner["nickname"], partner["avatar"], partner["gender"]
        else:
            p_name, p_avatar, p_gender = "等待中...", "⏳", "unknown"

        df = get_game_df(room_id)
        my_score = df[df["使用者名稱"]==me["nickname"]]["點數"].sum() if not df.empty else 0
        p_score = df[df["使用者名稱"]==p_name]["點數"].sum() if not df.empty else 0
        joint_score = int(my_score + p_score)
        
        pet_icon, pet_title, pet_desc = get_pet_status(joint_score)
        
        st.markdown(f"""<div class="hero-card"><h1>{room_name}</h1><p>{me['avatar']} {me['nickname']} &nbsp;&nbsp;×&nbsp;&nbsp; {p_avatar} {p_name}</p></div>""", unsafe_allow_html=True)

        col_top1, col_top2 = st.columns([4,1])
        with col_top2:
            if st.button("🚪 登出", key="btn_logout_top"):
                st.session_state.user_session = None
                st.rerun()

        tabs = st.tabs(["🏡 首頁", "📖 故事挑戰", "💌 情書", "📸 回憶", "🎯 任務", "🎁 商城", "⚙️ 設定"])

        # Tab 1: 首頁
        with tabs[0]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h3 style="color:#FF9A9E; margin-bottom:15px;">🐣 我們的寵物</h3>
                <div class="pet-container">{pet_icon}</div>
                <h2 style="margin:10px 0;">{pet_title}</h2>
                <p style="color:#888; font-style:italic;">"{pet_desc}"</p>
                <div style="margin-top:25px;"><progress value="{min(joint_score, 5000)}" max="5000" style="width:100%; height:10px; border-radius:5px;"></progress></div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px;"><h4>{me['avatar']} 我</h4><div class="stat-number">{int(my_score)}</div></div>""", unsafe_allow_html=True)
            with c2: st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px;"><h4>{p_avatar} 伴侶</h4><div class="stat-number">{int(p_score)}</div></div>""", unsafe_allow_html=True)
            
            today_w = get_today_word()
            today_date = date.today().strftime("%Y-%m-%d")
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin-bottom:10px;">📅 {today_date} 今日情話</h4>
                <h2 style="color:#6c5ce7; margin:0;">{today_w['word']}</h2>
                <p style="font-size:1.1em;"><b>{today_w['ch']}</b></p>
                <p style="color:#666; font-style:italic;">"{today_w['sentence']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            if has_today_action(df, me["nickname"], "口說"):
                st.button("✅ 今日已打卡", disabled=True, use_container_width=True)
            else:
                if st.button("🗣️ 每日口說打卡 (+30pt)", type="primary", use_container_width=True):
                    save_action(room_id, me["nickname"], me["gender"], "口說", today_w["word"], 30)
                    st.toast("打卡成功！寵物獲得能量 ✨", icon="🍖")
                    time.sleep(1)
                    st.rerun()

        # Tab 2: 故事挑戰
        with tabs[1]:
            st.header("📖 故事閱讀 & 極限挑戰")
            
            story = get_weekly_story()
            
            # 階段 1: 閱讀模式
            if st.session_state.quiz_phase == "reading":
                st.markdown("""
                <div class="rule-box-blue">
                    <b>📜 遊戲規則：</b><br>
                    1. 先閱讀下方的短篇故事，學習重點單字。<br>
                    2. 按下開始挑戰後，進入隨堂考。<br>
                    3. 每題限時 <b>40秒</b>，必須 <b>全對</b> 才能獲得 <b>100分</b>！
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"### {story['title']}")
                st.image(story['image'], use_container_width=True)
                
                with st.expander("📖 閱讀故事 (中英對照)", expanded=True):
                    st.markdown(f"**{story['content_en']}**")
                    st.divider()
                    st.markdown(f"{story['content_ch']}")
                
                st.subheader("🔑 重點單字")
                for v in story['vocab']:
                    st.markdown(f"<span class='vocab-tag'>{v['word']}</span> : {v['ch']}", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔥 我準備好了！開始挑戰", type="primary", use_container_width=True):
                    st.session_state.quiz_phase = "testing"
                    st.session_state.quiz_q_index = 0
                    st.session_state.quiz_score_sheet = []
                    st.session_state.quiz_start_time = time.time()
                    st.rerun()

            # 階段 2: 測驗模式
            elif st.session_state.quiz_phase == "testing":
                q_idx = st.session_state.quiz_q_index
                questions = story['vocab']
                
                if q_idx < len(questions):
                    q_data = questions[q_idx]
                    
                    st.progress((q_idx) / len(questions))
                    st.markdown(f"### Question {q_idx + 1} / {len(questions)}")
                    
                    st.warning("⏱️ 限時 40 秒！")
                    st.info(f"請翻譯： **{q_data['ch']}**")
                    
                    user_ans = st.text_input("請輸入英文單字", key=f"q_input_{q_idx}")
                    
                    if st.button("送出答案"):
                        time_used = time.time() - st.session_state.quiz_start_time
                        if time_used > 40:
                            st.error(f"❌ 超時了！(用了 {int(time_used)} 秒)")
                            st.session_state.quiz_score_sheet.append(False)
                        elif user_ans.strip().lower() == q_data['word'].lower():
                            st.session_state.quiz_score_sheet.append(True)
                        else:
                            st.error(f"❌ 答錯了！正確答案是 {q_data['word']}")
                            st.session_state.quiz_score_sheet.append(False)
                        
                        st.session_state.quiz_q_index += 1
                        st.session_state.quiz_start_time = time.time()
                        time.sleep(0.5)
                        st.rerun()
                else:
                    st.session_state.quiz_phase = "result"
                    st.rerun()

            # 階段 3: 結算模式
            elif st.session_state.quiz_phase == "result":
                results = st.session_state.quiz_score_sheet
                is_perfect = all(results)
                
                st.markdown("### 📊 挑戰結果")
                cols = st.columns(len(results))
                for i, res in enumerate(results):
                    cols[i].metric(f"Q{i+1}", "O" if res else "X")
                
                if is_perfect:
                    st.balloons()
                    st.success("🎉 太強了！全部答對！獲得 100 分！")
                    if st.button("領取獎勵並返回"):
                        save_action(room_id, me["nickname"], me["gender"], "挑戰", f"完美通關: {story['title']}", 100)
                        st.session_state.quiz_phase = "reading"
                        st.rerun()
                else:
                    st.error("😢 很遺憾，沒有全對... 這次不能拿分喔。")
                    if st.button("重新挑戰"):
                        st.session_state.quiz_phase = "reading"
                        st.rerun()

        # Tab 3: 情書
        with tabs[2]:
            st.header("💌 密碼情書")
            st.markdown("""<div class="rule-box-pink"><b>📜 規則：</b> 寫下悄悄話並上鎖（可附照片），對方解鎖成功可得 <b>+20 分</b>。</div>""", unsafe_allow_html=True)

            with st.expander("✍️ 寫新情書 (可附圖)"):
                txt = st.text_area("內容")
                img_file = st.file_uploader("附上照片 (選填)", type=["png", "jpg", "jpeg"])
                if st.button("🔒 上鎖發送"):
                    if txt:
                        img_path = save_uploaded_image(img_file)
                        send_secret_message(room_id, me["nickname"], txt, img_path)
                        st.toast("已發送！", icon="📨")
                        st.rerun()
                    else: st.warning("請輸入內容")
            
            msgs = get_room_messages(room_id)
            if not msgs.empty:
                for idx, msg in msgs.iterrows():
                    is_mine = str(msg["sender"]) == str(me["nickname"])
                    status_cls = "secret-msg-unlocked" if msg["status"]=="OPEN" else "secret-msg-locked"
                    icon = "🔓" if msg["status"]=="OPEN" else "🔒"
                    content_display = msg['content'] if (msg['status']=='OPEN' or is_mine) else '********'
                    
                    st.markdown(f"""<div class="{status_cls}"><small>{msg['sender']} ({str(msg['timestamp'])[5:16]})</small><br><b>{icon} {content_display}</b></div>""", unsafe_allow_html=True)
                    
                    if (msg['status'] == "OPEN" or is_mine) and str(msg['image_path']) != "None":
                        if os.path.exists(str(msg['image_path'])):
                            st.image(str(msg['image_path']), caption="附圖", width=300)
                    
                    c1, c2 = st.columns([1, 4])
                    if msg["status"] == "LOCKED" and not is_mine:
                        if c1.button("🗝️ 解鎖", key=f"unlock_{idx}"):
                            st.session_state.unlock_target = msg["timestamp"]
                            st.session_state.unlock_quiz = random.choice(CONTENT_BANK)
                            st.rerun()
                    if msg["status"] == "OPEN" and not is_mine:
                        if c1.button(f"❤️ {int(float(msg['likes']))}", key=f"like_{idx}"):
                            like_message(room_id, msg["timestamp"])
                            st.rerun()
            
            if "unlock_target" in st.session_state:
                st.divider()
                with st.container(border=True):
                    st.warning("🔥 解鎖挑戰！")
                    q = st.session_state.unlock_quiz
                    st.write(f"翻譯：**{q['ch']}**")
                    u_ans = st.text_input("答案", key="u_ans")
                    c1, c2 = st.columns(2)
                    if c1.button("確認", type="primary"):
                        if u_ans.strip().lower() == q["word"].lower():
                            unlock_message(room_id, st.session_state.unlock_target)
                            save_action(room_id, me["nickname"], me["gender"], "解鎖", "情書", 20)
                            st.toast("解鎖成功！", icon="🔓")
                            del st.session_state.unlock_target
                            st.rerun()
                        else: st.error("錯誤")
                    if c2.button("取消"):
                        del st.session_state.unlock_target
                        st.rerun()

        # Tab 4: 回憶
        with tabs[3]:
            st.header("📸 回憶")
            with st.expander("➕ 新增回憶"):
                m_tit = st.text_input("標題")
                m_desc = st.text_area("描述")
                m_mood = st.selectbox("心情", ["😍","😊","😭","😡"])
                m_img = st.file_uploader("照片 (選填)", type=["png", "jpg", "jpeg"], key="mem_img")
                if st.button("記錄"):
                    if m_tit:
                        img_path = save_uploaded_image(m_img)
                        add_memory(room_id, m_tit, m_desc, m_mood, img_path)
                        st.toast("已保存", icon="💾")
                        st.rerun()
                    else: st.warning("請輸入標題")

            mems = get_memories(room_id)
            for _, m in mems.iterrows():
                st.markdown(f"""<div class="glass-card"><h3>{m['mood']} {m['title']}</h3><p class="small-muted">{m['date']}</p><p>{m['desc']}</p></div>""", unsafe_allow_html=True)
                if str(m['image_path']) != "None":
                    if os.path.exists(str(m['image_path'])):
                        st.image(str(m['image_path']), use_container_width=True)
                st.markdown("---")

        # Tab 5: 任務
        with tabs[4]:
            st.header("🎯 每日任務 (互相監督)")
            st.markdown("""<div class="rule-box-orange"><b>📜 規則：</b> 完成後請把手機交給對方，由對方幫你確認打勾！</div>""", unsafe_allow_html=True)

            ensure_today_quests(room_id)
            daily_qs = get_today_quests(room_id)
            
            if p_name == "等待中...":
                st.warning("伴侶尚未加入，無法互評")
            else:
                col_partner, col_me = st.columns(2)
                with col_partner:
                    st.subheader(f"👮 審核 {p_name}")
                    for idx, q in daily_qs.iterrows():
                        p_done = has_today_action(df, p_name, q["quest_key"])
                        with st.container(border=True):
                            st.markdown(f"**{q['emoji']} {q['desc']}**")
                            st.caption(f"獎勵: {q['reward']}pt")
                            if p_done:
                                st.button("✅ 已完成", key=f"p_done_{idx}", disabled=True)
                            else:
                                if st.button("幫打勾", key=f"verify_{idx}"):
                                    save_action(room_id, p_name, p_gender, q["quest_key"], "任務", int(q["reward"]))
                                    st.toast(f"已確認！", icon="⭕")
                                    time.sleep(1)
                                    st.rerun()

                with col_me:
                    st.subheader("📋 我的進度")
                    for idx, q in daily_qs.iterrows():
                        my_done = has_today_action(df, me["nickname"], q["quest_key"])
                        with st.container(border=True):
                            st.markdown(f"**{q['emoji']} {q['desc']}**")
                            if my_done: st.success("✅ 已獲得點數")
                            else: st.caption("⏳ 等待對方確認...")

        # Tab 6: 商城
        with tabs[5]:
            st.header("🎁 商城")
            st.info(f"餘額: {int(my_score)} pt")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💆 按摩券 (100pt)", use_container_width=True):
                    if can_afford(my_score, -100):
                        save_action(room_id, me["nickname"], me["gender"], "兌換", "按摩券", -100)
                        st.toast("兌換成功", icon="💆")
                        st.rerun()
                    else: st.error("點數不足")
            with c2:
                if st.button("🎬 電影券 (300pt)", use_container_width=True):
                    if can_afford(my_score, -300):
                        save_action(room_id, me["nickname"], me["gender"], "兌換", "電影券", -300)
                        st.toast("兌換成功", icon="🎬")
                        st.rerun()
                    else: st.error("點數不足")
            st.divider()
            if st.button("🎲 隨機約會靈感", use_container_width=True):
                idea = random.choice(DATE_IDEAS)
                st.success(f"**{idea['title']}**\n\n{idea['desc']}")

        # Tab 7: 設定
        with tabs[6]:
            st.header("⚙️ 設定")
            if st.button("🚪 離開房間"):
                update_user_room(me["username"], "None")
                st.session_state.user_session["room_id"] = "None"
                st.rerun()
            st.divider()
            if st.button("🚪 登出", key="btn_logout_settings"):
                st.session_state.user_session = None
                st.rerun()
            st.divider()
            if st.button("🧹 重置房間數據"):
                reset_room_data(room_id)
                st.toast("已重置", icon="🧹")
                st.rerun()