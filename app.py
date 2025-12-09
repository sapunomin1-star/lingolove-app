import streamlit as st
import pandas as pd
import os
import random
import hashlib
from datetime import datetime, date, timedelta
import time
import uuid

# =====================================================
# 🎨 0. UI 設定 & CSS
# =====================================================

st.set_page_config(
    page_title="LingoLove - 兩人專屬英語小屋",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Quicksand:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans TC', 'Quicksand', sans-serif;
        background-color: #FAFAFA;
        color: #2c3e50;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div.block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
        color: #2c3e50;
    }

    .pet-stage {
        text-align: center;
        padding: 40px;
        border-radius: 30px;
        margin-bottom: 20px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.05);
        border: 4px solid rgba(255,255,255,0.8);
        position: relative;
        overflow: hidden;
        transition: all 0.5s ease;
    }
    
    .pet-emoji {
        font-size: 80px;
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
        animation: bounce 2s infinite ease-in-out;
    }

    @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

    .hero-card {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        border-radius: 24px;
        padding: 32px;
        color: #5d5d5d;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-card h1 { margin: 0; font-size: 2.2rem; color: #4a4a4a; font-weight: 700; }

    .stat-number { font-size: 28px; font-weight: 800; color: #ff6b81; font-family: 'Quicksand', sans-serif; }
    .small-muted { font-size: 13px; color: #a4b0be; }
    
    .rule-box-blue { background-color: #e3f2fd; padding: 15px; border-radius: 12px; border-left: 6px solid #2196f3; margin-bottom: 20px; color: #0d47a1; }
    .rule-box-pink { background-color: #fce4ec; padding: 15px; border-radius: 12px; border-left: 6px solid #e91e63; margin-bottom: 20px; color: #880e4f; }
    .rule-box-orange { background-color: #fff3e0; padding: 15px; border-radius: 12px; border-left: 6px solid #ff9800; margin-bottom: 20px; color: #e65100; }
    
    .vocab-tag { display: inline-block; background-color: #e0e0e0; padding: 5px 10px; border-radius: 15px; margin: 3px; font-size: 0.9em; font-weight: bold; color: #333; }
    .secret-msg-locked { background: #f1f3f5; border-left: 6px solid #adb5bd; padding: 16px; border-radius: 12px; color: #868e96; font-style: italic; margin-bottom: 12px; }
    .secret-msg-unlocked { background: #e3fafc; border-left: 6px solid #66d9e8; padding: 16px; border-radius: 12px; color: #0c8599; margin-bottom: 12px; }
</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)

# =====================================================
# 🛍️ 商城物品
# =====================================================
STORE_ITEMS = {
    "skin_default":  {"type": "skin", "name": "✨ 自然進化", "icon": "🥚", "price": 0, "desc": "隨積分自動進化"},
    "skin_cat":      {"type": "skin", "name": "🐱 貪吃橘貓", "icon": "🐱", "price": 500, "desc": "永遠吃不飽"},
    "skin_dog":      {"type": "skin", "name": "🐕 忠誠柴犬", "icon": "🐕", "price": 500, "desc": "在門口等你"},
    "skin_robot":    {"type": "skin", "name": "🤖 戀愛機器人","icon": "🤖", "price": 800, "desc": "速配率 100%"},
    "skin_alien":    {"type": "skin", "name": "👽 外星寶寶", "icon": "👽", "price": 1000, "desc": "來自愛的星球"},
    "skin_king":     {"type": "skin", "name": "🤴 國王",     "icon": "🤴", "price": 1500, "desc": "尊爵不凡"},
    "skin_queen":    {"type": "skin", "name": "👸 女王",     "icon": "👸", "price": 1500, "desc": "氣場全開"},
    
    "bg_default":    {"type": "bg", "name": "🏠 溫馨暖白", "icon": "⬜", "price": 0,    "css": "background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);"},
    "bg_sakura":     {"type": "bg", "name": "🌸 櫻花季",   "icon": "🌸", "price": 300,  "css": "background: linear-gradient(120deg, #ff9a9e 0%, #fecfef 100%);"},
    "bg_ocean":      {"type": "bg", "name": "🌊 海洋之心", "icon": "🌊", "price": 300,  "css": "background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);"},
    "bg_night":      {"type": "bg", "name": "🌌 星空夜語", "icon": "🌌", "price": 600,  "css": "background: linear-gradient(to top, #30cfd0 0%, #330867 100%); color: white !important; text-shadow: 1px 1px 2px black;"},
    "bg_sunset":     {"type": "bg", "name": "🌇 落日餘暉", "icon": "🌇", "price": 400,  "css": "background: linear-gradient(to right, #fa709a 0%, #fee140 100%); color: white !important; text-shadow: 1px 1px 2px black;"},
    "bg_forest":     {"type": "bg", "name": "🌲 迷霧森林", "icon": "🌲", "price": 400,  "css": "background: linear-gradient(to top, #0ba360 0%, #3cba92 100%); color: white !important; text-shadow: 1px 1px 2px black;"},
}

# =====================================================
# 💾 1. 資料庫管理
# =====================================================

USER_DB_FILE    = "users_v7.csv"
ROOM_DB_FILE    = "rooms_v7.csv"
INVENTORY_DB_FILE = "inventory.csv"
MESSAGE_DB_FILE = "messages_v7.csv"
MEMORY_DB_FILE  = "memories_v7.csv"
QUEST_DB_FILE   = "quests_v7.csv"
GAME_DATA_FILE_PREFIX = "lingo_data_"
IMAGES_DIR      = "images"

if not os.path.exists(IMAGES_DIR): os.makedirs(IMAGES_DIR)

# 🟢 修正：統一函式名稱為 hash_password
def hash_password(pwd: str) -> str: 
    return hashlib.sha256(pwd.encode()).hexdigest()

def load_csv(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df
    
    df = pd.read_csv(file_path)
    # 自動修復缺少的欄位
    for col in columns:
        if col not in df.columns:
            if col == "story_level":
                df[col] = 0
            else:
                df[col] = "None"
    df.to_csv(file_path, index=False)
    return df

def save_csv(df, file_path): df.to_csv(file_path, index=False)

def save_uploaded_image(u_file):
    if u_file is None: return None
    ext = os.path.splitext(u_file.name)[1]
    fname = f"{uuid.uuid4()}{ext}"
    path = os.path.join(IMAGES_DIR, fname)
    with open(path, "wb") as f: f.write(u_file.getbuffer())
    return path

AVATARS = ["🧸","🐻","🐼","🐨","🐯","🦊","🐱","🐶","🦁","🐰","🦋","🌸","🌙","⭐","🍑","🍓","🍒","🧁","☕","🎧"]

# --- 使用者 ---
def get_user(username):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"]).astype(str)
    user = df[df["username"] == str(username)]
    return user.iloc[0].to_dict() if not user.empty else None

def create_user(username, password, nickname, gender, avatar):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"])
    if str(username) in df["username"].astype(str).values: return False, "帳號已存在"
    new_u = pd.DataFrame([{"username": username, "password": hash_password(password), "nickname": nickname, "gender": gender, "room_id": "None", "avatar": avatar, "join_date": date.today().isoformat()}])
    save_csv(pd.concat([df, new_u], ignore_index=True), USER_DB_FILE)
    return True, "註冊成功"

def update_user_room(username, room_id):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"])
    df.loc[df["username"].astype(str) == str(username), "room_id"] = str(room_id)
    save_csv(df, USER_DB_FILE)

def update_user_profile(username, new_nick, new_avatar):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"])
    idx = df["username"].astype(str) == str(username)
    df.loc[idx, "nickname"] = new_nick
    df.loc[idx, "avatar"] = new_avatar
    save_csv(df, USER_DB_FILE)

def get_room_users(room_id):
    df = load_csv(USER_DB_FILE, ["username","password","nickname","gender","room_id","avatar","join_date"])
    return df[df["room_id"].astype(str) == str(room_id)]

# --- 房間 & 庫存 ---
def init_inventory(room_id):
    df = load_csv(INVENTORY_DB_FILE, ["room_id", "item_key"])
    defaults = [{"room_id": str(room_id), "item_key": "skin_default"}, {"room_id": str(room_id), "item_key": "bg_default"}]
    save_csv(pd.concat([df, pd.DataFrame(defaults)], ignore_index=True), INVENTORY_DB_FILE)

def create_room(room_id, password, room_name, anniversary):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary","active_skin","active_bg", "story_level"])
    if str(room_id) in df["room_id"].astype(str).values: return False, "房號已存在"
    new_r = pd.DataFrame([{
        "room_id": str(room_id), "room_name": room_name, "password": hash_password(password),
        "created_at": datetime.now().isoformat(), "anniversary": anniversary,
        "active_skin": "skin_default", "active_bg": "bg_default",
        "story_level": 0
    }])
    save_csv(pd.concat([df, new_r], ignore_index=True), ROOM_DB_FILE)
    init_inventory(room_id)
    return True, "成功"

def update_room_info(room_id, new_name=None, new_pass=None):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary","active_skin","active_bg", "story_level"])
    idx = df["room_id"].astype(str) == str(room_id)
    if new_name: df.loc[idx, "room_name"] = new_name
    if new_pass: df.loc[idx, "password"] = hash_password(new_pass)
    save_csv(df, ROOM_DB_FILE)

# 🟢 強制更新等級函式
def update_room_story_level(room_id, new_level):
    try:
        df = pd.read_csv(ROOM_DB_FILE)
        df['room_id'] = df['room_id'].astype(str)
        room_id = str(room_id)
        
        # 確保有欄位
        if 'story_level' not in df.columns:
            df['story_level'] = 0
            
        # 寫入
        mask = df['room_id'] == room_id
        if mask.any():
            df.loc[mask, 'story_level'] = int(new_level)
            df.to_csv(ROOM_DB_FILE, index=False)
            return True
    except Exception as e:
        print(f"Error updating level: {e}")
    return False

def check_room_exists(room_id):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary","active_skin","active_bg", "story_level"])
    return str(room_id) in df["room_id"].astype(str).values

def verify_room_password(room_id, password):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary","active_skin","active_bg", "story_level"])
    r = df[df["room_id"].astype(str) == str(room_id)]
    if r.empty: return False
    return r.iloc[0]["password"] == hash_password(password)

def get_room_info(room_id):
    # 每次讀取都強制重新載入 CSV
    if os.path.exists(ROOM_DB_FILE):
        df = pd.read_csv(ROOM_DB_FILE)
        df['room_id'] = df['room_id'].astype(str)
        r = df[df["room_id"] == str(room_id)]
        if not r.empty:
            return r.iloc[0].to_dict()
    return {}

def update_room_look(room_id, item_key, item_type):
    df = load_csv(ROOM_DB_FILE, ["room_id","room_name","password","created_at","anniversary","active_skin","active_bg", "story_level"])
    col = "active_skin" if item_type == "skin" else "active_bg"
    idx = df[df["room_id"].astype(str) == str(room_id)].index
    if not idx.empty:
        df.loc[idx, col] = item_key
        save_csv(df, ROOM_DB_FILE)

def get_inventory(room_id):
    df = load_csv(INVENTORY_DB_FILE, ["room_id", "item_key"])
    return df[df["room_id"].astype(str) == str(room_id)]["item_key"].tolist()

def add_to_inventory(room_id, item_key):
    df = load_csv(INVENTORY_DB_FILE, ["room_id", "item_key"])
    if not ((df["room_id"].astype(str) == str(room_id)) & (df["item_key"] == item_key)).any():
        new_item = pd.DataFrame([{"room_id": str(room_id), "item_key": item_key}])
        save_csv(pd.concat([df, new_item], ignore_index=True), INVENTORY_DB_FILE)

# --- 遊戲數據 ---
def get_game_df(room_id):
    return load_csv(f"{GAME_DATA_FILE_PREFIX}{room_id}.csv", ["時間","使用者名稱","性別","動作","項目","點數"])

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

def can_afford(current_score, cost): return current_score + cost >= 0

# --- 情書/回憶 ---
def send_secret_message(room_id, sender, content, image_path=None):
    df = load_csv(MESSAGE_DB_FILE, ["room_id","sender","content","status","timestamp","likes", "image_path"])
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
    df = load_csv(MEMORY_DB_FILE, ["room_id","date","title","desc","mood", "image_path"])
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

def ensure_today_quests(room_id, pool):
    init_quest_db()
    df = load_csv(QUEST_DB_FILE, ["room_id","date","quest_key","desc","reward","emoji"])
    today = date.today().isoformat()
    if not ((df["room_id"] == str(room_id)) & (df["date"] == today)).any():
        selected = random.sample(pool, min(3, len(pool)))
        new_rows = []
        for q in selected:
            new_rows.append({"room_id": str(room_id), "date": today, "quest_key": q["type"], "desc": q["desc"], "reward": q["reward"], "emoji": q["emoji"]})
        save_csv(pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True), QUEST_DB_FILE)

def get_today_quests(room_id):
    df = load_csv(QUEST_DB_FILE, ["room_id","date","quest_key","desc","reward","emoji"])
    today = date.today().isoformat()
    return df[(df["room_id"].astype(str) == str(room_id)) & (df["date"] == today)]

# =====================================================
# 🧠 2. 遊戲內容 (Stories & Quests)
# =====================================================

def get_pet_evolution(score):
    if score < 500:   return "🥚", "神秘的蛋", "孵化中..."
    if score < 1500:  return "🐣", "呆萌小雞", "世界好大！"
    if score < 3000:  return "🦉", "博學貓頭鷹", "Hoo-Hoo!"
    if score < 5000:  return "🦄", "夢幻獨角獸", "充滿魔力！"
    return "🐲", "傳奇神龍", "世界最強！"

# 📚 故事庫 (Story Bank)
# =====================================================


STORY_BANK = [
    # Level 1 - 5: 初識與日常
    {
        "id": "s1", "title": "Rainy Day Coffee (雨天咖啡)", 
        "image": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=600",
        "content_en": "It was a rainy afternoon. Alice ran into a small coffee shop to hide from the rain. She ordered a hot latte. Suddenly, a man walked in, shaking his wet umbrella. Their eyes met, and time seemed to stop.",
        "content_ch": "這是一個下雨的下午。Alice 跑進一家小咖啡廳躲雨。她點了一杯熱拿鐵。突然，一個男人走了進來，甩著他濕淋淋的雨傘。他們的眼神交會，時間彷彿靜止了。",
        "vocab": [{"word": "Shelter", "ch": "庇護所"}, {"word": "Latte", "ch": "拿鐵"}, {"word": "Suddenly", "ch": "突然地"}, {"word": "Umbrella", "ch": "雨傘"}]
    },
    {
        "id": "s2", "title": "The Lost Puppy (迷路小狗)", 
        "image": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600",
        "content_en": "Ben found a small puppy shivering under a bench in the park. It looked hungry and scared. Ben gently picked it up and decided to take it home. He named it 'Lucky'.",
        "content_ch": "Ben 在公園的長椅下發現了一隻發抖的小狗。它看起來又餓又害怕。Ben 溫柔地抱起它，決定帶它回家。他給它取名叫「Lucky」。",
        "vocab": [{"word": "Shiver", "ch": "發抖"}, {"word": "Bench", "ch": "長椅"}, {"word": "Scared", "ch": "害怕的"}, {"word": "Gently", "ch": "溫柔地"}]
    },
    {
        "id": "s3", "title": "Starry Night (星空之夜)", 
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=600",
        "content_en": "They drove up the mountain to see the stars. The sky was clear and full of sparkling lights. He held her hand and whispered, 'You are brighter than any star.'",
        "content_ch": "他們開車上山去看星星。天空很晴朗，滿是閃爍的光點。他握住她的手，輕聲說：「你比任何星星都耀眼。」",
        "vocab": [{"word": "Mountain", "ch": "山"}, {"word": "Sparkling", "ch": "閃爍的"}, {"word": "Whisper", "ch": "低語"}, {"word": "Bright", "ch": "明亮的"}]
    },
    {
        "id": "s4", "title": "Cooking Together (一起做飯)", 
        "image": "https://images.unsplash.com/photo-1556910103-1c02745a30bf?w=600",
        "content_en": "They decided to make pasta for dinner. The kitchen was messy but full of laughter. She chopped the onions while he boiled the water. It tasted perfect because they made it together.",
        "content_ch": "他們決定晚餐煮義大利麵。廚房雖然亂七八糟，但充滿了笑聲。她切洋蔥，他煮水。這頓飯嚐起來很完美，因為是他們一起做的。",
        "vocab": [{"word": "Messy", "ch": "雜亂的"}, {"word": "Chop", "ch": "切/剁"}, {"word": "Boil", "ch": "煮沸"}, {"word": "Perfect", "ch": "完美的"}]
    },
    {
        "id": "s5", "title": "Movie Night (電影之夜)", 
        "image": "https://images.unsplash.com/photo-1517604931442-71053e683e12?w=600",
        "content_en": "They chose a horror movie. She was scared, so she hid behind a pillow. He laughed and hugged her tight. It became their favorite date night activity.",
        "content_ch": "他們選了一部恐怖片。她很害怕，所以躲在枕頭後面。他笑了笑，緊緊抱住她。這成了他們最喜歡的約會活動。",
        "vocab": [{"word": "Horror", "ch": "恐怖"}, {"word": "Hide", "ch": "躲藏"}, {"word": "Pillow", "ch": "枕頭"}, {"word": "Activity", "ch": "活動"}]
    },

    # Level 6 - 10: 驚喜與挑戰
    {
        "id": "s6", "title": "The Surprise (驚喜)", 
        "image": "https://images.unsplash.com/photo-1513201099705-a9746e1e201f?w=600",
        "content_en": "It was just a normal Tuesday. He came home with a bouquet of red roses. 'Just because,' he said. She felt like the luckiest girl in the world.",
        "content_ch": "這只是一個普通的週二。他帶著一束紅玫瑰回家。「不為什麼，」他說。她覺得自己是世界上最幸運的女孩。",
        "vocab": [{"word": "Normal", "ch": "普通的"}, {"word": "Bouquet", "ch": "花束"}, {"word": "Luckiest", "ch": "最幸運的"}]
    },
    {
        "id": "s7", "title": "Beach Day (海灘日)", 
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
        "content_en": "The sun was shining bright. They built a huge sandcastle near the water. The ocean breeze was refreshing. They took many photos to remember this day.",
        "content_ch": "陽光燦爛。他們在水邊堆了一個巨大的沙堡。海風令人心曠神怡。他們拍了很多照片來紀念這一天。",
        "vocab": [{"word": "Shine", "ch": "照耀"}, {"word": "Sandcastle", "ch": "沙堡"}, {"word": "Breeze", "c": "微風"}, {"word": "Refreshing", "ch": "清爽的"}]
    },
    {
        "id": "s8", "title": "Grocery Shopping (買菜)", 
        "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600",
        "content_en": "They went to the supermarket. They argued playfully about which snacks to buy. In the end, they bought both chocolate and chips. Compromise is key.",
        "content_ch": "他們去了超市。他們開玩笑地爭論要買哪種零食。最後，巧克力和洋芋片都買了。妥協是關鍵。",
        "vocab": [{"word": "Argue", "ch": "爭論"}, {"word": "Snack", "ch": "零食"}, {"word": "Compromise", "ch": "妥協"}]
    },
    {
        "id": "s9", "title": "Sick Day (生病)", 
        "image": "https://images.unsplash.com/photo-1584634731339-252c581abfc5?w=600",
        "content_en": "She woke up with a fever. He cancelled his plans to take care of her. He made soup and read her stories. His presence was the best medicine.",
        "content_ch": "她醒來發燒了。他取消了計畫來照顧她。他煮湯並讀故事給她聽。他的陪伴是最好的良藥。",
        "vocab": [{"word": "Fever", "ch": "發燒"}, {"word": "Cancel", "ch": "取消"}, {"word": "Presence", "ch": "陪伴/存在"}, {"word": "Medicine", "ch": "藥"}]
    },
    {
        "id": "s10", "title": "Lost Keys (鑰匙不見了)", 
        "image": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600",
        "content_en": "He couldn't find his keys. They searched everywhere in the house. Finally, they found them in the fridge! They laughed so hard their stomachs hurt.",
        "content_ch": "他找不到鑰匙。他們在家裡到處找。最後，竟然在冰箱裡找到了！他們笑到肚子痛。",
        "vocab": [{"word": "Search", "ch": "搜尋"}, {"word": "Fridge", "ch": "冰箱"}, {"word": "Stomach", "ch": "肚子"}]
    },

    # Level 11 - 15: 深入與磨合
    {
        "id": "s11", "title": "Rainy Drive (雨中駕駛)", 
        "image": "https://images.unsplash.com/photo-1490555022872-9844f24fba9d?w=600",
        "content_en": "The storm was heavy. He drove very carefully while she checked the map. They worked as a team to get home safely.",
        "content_ch": "暴風雨很大。他非常小心地開車，而她負責看地圖。他們團隊合作安全回到了家。",
        "vocab": [{"word": "Storm", "ch": "暴風雨"}, {"word": "Carefully", "ch": "小心地"}, {"word": "Safely", "ch": "安全地"}]
    },
    {
        "id": "s12", "title": "Broken Phone (手機壞了)", 
        "image": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600",
        "content_en": "She accidentally dropped her phone. The screen cracked. She was upset, but he told her it was just a thing. 'You are what matters,' he said.",
        "content_ch": "她不小心摔了手機。螢幕裂開了。她很難過，但他告訴她那只是個物品。「你才是最重要的，」他說。",
        "vocab": [{"word": "Accidentally", "ch": "意外地"}, {"word": "Crack", "ch": "裂開"}, {"word": "Matter", "ch": "重要"}]
    },
    {
        "id": "s13", "title": "Cleaning Day (大掃除)", 
        "image": "https://images.unsplash.com/photo-1581578731117-10d52143b0e8?w=600",
        "content_en": "They spent Sunday cleaning the entire house. They played loud music and danced while sweeping. Chores became fun when done together.",
        "content_ch": "他們週日打掃了整間房子。他們放很大聲的音樂，邊掃地邊跳舞。一起做家事變成了樂趣。",
        "vocab": [{"word": "Entire", "ch": "整個"}, {"word": "Sweep", "ch": "掃地"}, {"word": "Chore", "ch": "家務/雜事"}]
    },
    {
        "id": "s14", "title": "Late Night Talk (深夜談心)", 
        "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600",
        "content_en": "They couldn't sleep. They stayed up late talking about their childhoods. Sharing secrets made their bond even stronger.",
        "content_ch": "他們睡不著。他們熬夜聊著彼此的童年。分享秘密讓他們的連結更緊密了。",
        "vocab": [{"word": "Childhood", "ch": "童年"}, {"word": "Secret", "ch": "秘密"}, {"word": "Bond", "ch": "連結/羈絆"}]
    },
    {
        "id": "s15", "title": "Road Trip (公路旅行)", 
        "image": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600",
        "content_en": "They packed the car with snacks. They sang along to the radio. The destination didn't matter, only the journey together.",
        "content_ch": "他們在車上塞滿了零食。他們跟著收音機唱歌。目的地不重要，重要的是一起的旅程。",
        "vocab": [{"word": "Pack", "ch": "打包"}, {"word": "Destination", "ch": "目的地"}, {"word": "Journey", "ch": "旅程"}]
    },

    # Level 16 - 20: 冒險與回憶
    {
        "id": "s16", "title": "Camping (露營)", 
        "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600",
        "en": "They set up a tent by the lake. They roasted marshmallows over the fire. The nature sounds were peaceful.",
        "content_ch": "他們在湖邊搭了帳篷。他們在火上烤棉花糖。大自然的聲音很平靜。",
        "vocab": [{"word": "Tent", "ch": "帳篷"}, {"word": "Roast", "ch": "烤"}, {"word": "Peaceful", "ch": "平靜的"}]
    },
    {
        "id": "s17", "title": "Hiking (健行)", 
        "image": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=600",
        "en": "The trail was steep and difficult. He held her hand to help her up. The view from the top was breathtaking.",
        "content_ch": "步道很陡峭且困難。他牽著她的手拉她上去。山頂的景色美得令人屏息。",
        "vocab": [{"word": "Steep", "ch": "陡峭的"}, {"word": "View", "ch": "景色"}, {"word": "Breathtaking", "ch": "驚人的美"}]
    },
    {
        "id": "s18", "title": "Lost in City (迷失城市)", 
        "image": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600",
        "en": "They got lost in a strange city. Instead of panicking, they explored. They found a delicious bakery and had the best cake ever.",
        "content_ch": "他們在陌生的城市迷路了。他們沒有驚慌，反而去探索。他們發現一家好吃的麵包店，吃了最棒的蛋糕。",
        "vocab": [{"word": "Strange", "ch": "陌生的"}, {"word": "Panic", "ch": "驚慌"}, {"word": "Explore", "ch": "探索"}]
    },
    {
        "id": "s19", "title": "Museum Visit (參觀博物館)", 
        "image": "https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?w=600",
        "en": "They walked quietly through the museum. He pretended to understand modern art. She laughed at his funny interpretations.",
        "content_ch": "他們安靜地走過博物館。他假裝懂現代藝術。她被他好笑的解讀逗樂了。",
        "vocab": [{"word": "Pretend", "ch": "假裝"}, {"word": "Modern", "ch": "現代的"}, {"word": "Interpretation", "ch": "解讀/詮釋"}]
    },
    {
        "id": "s20", "title": "Flight Delay (班機延誤)", 
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600",
        "en": "Their flight was delayed for 5 hours. They played cards on the floor. Even boring waiting time was fun with him.",
        "content_ch": "他們的班機延誤了5小時。他們在地上打牌。有他在，連無聊的等待時間都有趣。",
        "vocab": [{"word": "Delay", "ch": "延誤"}, {"word": "Boring", "ch": "無聊的"}, {"word": "Wait", "ch": "等待"}]
    },

    # Level 21 - 30: 承諾與未來
    {
        "id": "s21", "title": "Souvenirs (紀念品)", 
        "image": "https://images.unsplash.com/photo-1555447019-f5424564c749?w=600",
        "en": "She bought a cute magnet for her mom. He bought a funny hat. They promised to travel more in the future.",
        "content_ch": "她買了一個可愛的磁鐵給媽媽。他買了一頂好笑的帽子。他們承諾未來要更常旅行。",
        "vocab": [{"word": "Magnet", "ch": "磁鐵"}, {"word": "Promise", "ch": "承諾"}, {"word": "Future", "ch": "未來"}]
    },
    {
        "id": "s22", "title": "Meeting Parents (見家長)", 
        "image": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600",
        "en": "He was very nervous to meet her parents. He wore his best shirt. Luckily, her dad loved his jokes.",
        "content_ch": "他很緊張要去見她的父母。他穿上了最好的襯衫。幸運的是，她爸爸很愛他的笑話。",
        "vocab": [{"word": "Nervous", "ch": "緊張"}, {"word": "Shirt", "ch": "襯衫"}, {"word": "Luckily", "ch": "幸運地"}]
    },
    {
        "id": "s23", "title": "The Proposal (求婚)", 
        "image": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=600",
        "en": "He kneeled down on one knee. He held out a ring. She cried tears of joy and said 'Yes'.",
        "content_ch": "他單膝下跪。他拿出一枚戒指。她喜極而泣並答應了。",
        "vocab": [{"word": "Kneel", "ch": "跪下"}, {"word": "Ring", "ch": "戒指"}, {"word": "Joy", "ch": "喜悅"}]
    },
    {
        "id": "s24", "title": "New Apartment (新公寓)", 
        "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600",
        "en": "They moved into a new apartment. It was small but cozy. They painted the walls blue together.",
        "content_ch": "他們搬進了新公寓。雖然小但很溫馨。他們一起把牆壁漆成藍色。",
        "vocab": [{"word": "Apartment", "ch": "公寓"}, {"word": "Cozy", "ch": "溫馨"}, {"word": "Paint", "ch": "油漆"}]
    },
    {
        "id": "s25", "title": "Ikea Trip (逛家具)", 
        "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=600",
        "en": "Buying furniture is stressful. They couldn't agree on a sofa. But they solved it with a hug and ice cream.",
        "content_ch": "買傢俱很有壓力。他們對沙發意見不合。但他們用擁抱和冰淇淋解決了問題。",
        "vocab": [{"word": "Furniture", "ch": "傢俱"}, {"word": "Stressful", "ch": "有壓力的"}, {"word": "Solve", "ch": "解決"}]
    },
    {
        "id": "s26", "title": "Adopt a Pet (領養寵物)", 
        "image": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600",
        "en": "They went to a shelter. A kitten looked at them with big eyes. They named him 'Mochi' and took him home.",
        "content_ch": "他們去了收容所。一隻小貓用大眼睛看著他們。他們叫他 Mochi 並帶他回家。",
        "vocab": [{"word": "Shelter", "ch": "收容所"}, {"word": "Kitten", "ch": "小貓"}, {"word": "Name", "ch": "命名"}]
    },
    {
        "id": "s27", "title": "Anniversary (紀念日)", 
        "image": "https://images.unsplash.com/photo-1530103862676-de3c9da59af7?w=600",
        "en": "They celebrated their anniversary. They looked at old photos. They realized how much they had grown together.",
        "content_ch": "他們慶祝紀念日。他們看了舊照片。他們意識到彼此一起成長了多少。",
        "vocab": [{"word": "Celebrate", "ch": "慶祝"}, {"word": "Realize", "ch": "意識到"}, {"word": "Grow", "ch": "成長"}]
    },
    {
        "id": "s28", "title": "Apology (道歉)", 
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600",
        "en": "He forgot an important date. He apologized sincerely. Forgiveness is part of love.",
        "content_ch": "他忘記了一個重要的日子。他真誠地道歉。原諒是愛的一部分。",
        "vocab": [{"word": "Forget", "ch": "忘記"}, {"word": "Apologize", "ch": "道歉"}, {"word": "Forgiveness", "ch": "原諒"}]
    },
    {
        "id": "s29", "title": "Growing Old (變老)", 
        "image": "https://images.unsplash.com/photo-1481819613568-3701cbc70156?w=600",
        "en": "They saw an old couple holding hands. 'That will be us,' she whispered. He squeezed her hand in agreement.",
        "content_ch": "他們看到一對老夫妻牽著手。「那會是我們，」她低語。他緊握她的手表示同意。",
        "vocab": [{"word": "Couple", "ch": "夫妻/情侶"}, {"word": "Whisper", "ch": "低語"}, {"word": "Agreement", "ch": "同意"}]
    },
    {
        "id": "s30", "title": "The Journey (旅程)", 
        "image": "https://images.unsplash.com/photo-1469474938227-add8492a4778?w=600",
        "en": "Life is a long journey. There will be ups and downs. But as long as they are together, everything is fine.",
        "content_ch": "人生是一段長途旅程。會有起起伏伏。但只要他們在一起，一切都會很好。",
        "vocab": [{"word": "Journey", "ch": "旅程"}, {"word": "Ups and downs", "ch": "起伏"}, {"word": "Together", "ch": "在一起"}]
    }
]

# 🗂️ 獨立單字庫
CONTENT_BANK = [
    {"word": "Cherish", "ch": "珍惜", "sentence": "I cherish every moment with you.", "context": "深情告白"},
    {"word": "Cuddle", "ch": "擁抱", "sentence": "Let's cuddle and watch a movie.", "context": "想討抱抱"},
    {"word": "Support", "ch": "支持", "sentence": "I support you no matter what.", "context": "互相打氣"},
    {"word": "Trust", "ch": "信任", "sentence": "I trust you completely.", "context": "內心話"},
    {"word": "Destiny", "ch": "命運", "sentence": "Meeting you was my destiny.", "context": "浪漫時刻"},
]

DATE_IDEAS = [
    {"title": "🎬 電影馬拉松", "desc": "準備爆米花和飲料，在家連看三部電影！"},
    {"title": "🍳 廚神大賽", "desc": "用冰箱現有食材，一人做一道創意料理。"},
]

QUEST_POOL = [
    {"type": "q_gratitude", "desc": "用英文說出 3 件感謝對方的事", "reward": 35, "emoji": "💝"},
    {"type": "q_compliment", "desc": "用英文誇對方 5 句 (形容詞不重複)", "reward": 35, "emoji": "🌟"},
    {"type": "q_feeling", "desc": "用 'I feel...' 表達感受 (不說 You always)", "reward": 40, "emoji": "🧠"},
    {"type": "q_hug", "desc": "給對方一個 30 秒的擁抱", "reward": 30, "emoji": "🫂"},
]

def get_weekly_story():
    # 這裡只回傳一個預設值，真正邏輯在 UI 層
    return STORY_BANK[0]

def get_today_word():
    random.seed(date.today().toordinal())
    res = random.choice(CONTENT_BANK)
    random.seed()
    return res

# =====================================================
# 📱 3. 介面呈現
# =====================================================

if "user_session" not in st.session_state: st.session_state.user_session = None
if "current_task" not in st.session_state: st.session_state.current_task = None
if "quiz_phase" not in st.session_state: st.session_state.quiz_phase = "reading"
if "quiz_q_index" not in st.session_state: st.session_state.quiz_q_index = 0
if "quiz_score_sheet" not in st.session_state: st.session_state.quiz_score_sheet = []
if "quiz_start_time" not in st.session_state: st.session_state.quiz_start_time = None

# A. 登入
if st.session_state.user_session is None:
    st.markdown("<h1 style='text-align:center;'>💖 LingoLove</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 登入", "✨ 註冊"])
    with t1:
        u = st.text_input("帳號", key="l_u")
        p = st.text_input("密碼", type="password", key="l_p")
        if st.button("登入", use_container_width=True, type="primary"):
            user = get_user(u)
            if user and user["password"] == hash_password(p):
                st.session_state.user_session = user
                st.rerun()
            else: st.error("錯誤")
    with t2:
        ru = st.text_input("設定帳號", key="r_u")
        rp = st.text_input("設定密碼", type="password", key="r_p")
        rn = st.text_input("暱稱", key="r_n")
        rg = st.radio("角色", ["👦", "👧"], horizontal=True)
        ra = st.selectbox("頭像", AVATARS)
        if st.button("註冊", use_container_width=True):
            if ru and rp and rn:
                ok, msg = create_user(ru, rp, rn, rg, ra)
                if ok: st.success(msg)
                else: st.error(msg)

# B. 主程式
else:
    me = st.session_state.user_session
    room_id = str(me["room_id"])
    
    # 大廳
    if room_id == "None" or room_id == "nan":
        st.info("🏠 請建立或加入小屋")
        c1, c2 = st.columns(2)
        with c1:
            n_rid = st.text_input("房號")
            n_pass = st.text_input("密碼")
            if st.button("創建"):
                ok, msg = create_room(n_rid, n_pass, "愛的小屋", "")
                if ok:
                    update_user_room(me["username"], n_rid)
                    st.session_state.user_session["room_id"] = n_rid
                    st.rerun()
                else: st.error(msg)
        with c2:
            j_rid = st.text_input("輸入房號")
            j_pass = st.text_input("輸入密碼", type="password")
            if st.button("加入"):
                if verify_room_password(j_rid, j_pass):
                    update_user_room(me["username"], j_rid)
                    st.session_state.user_session["room_id"] = j_rid
                    st.rerun()
                else: st.error("錯誤")
        if st.button("登出"): st.session_state.user_session = None; st.rerun()

    # 小屋
    else:
        # 強制重新讀取房間資訊
        r_info = get_room_info(room_id)
        room_name = r_info.get("room_name", "愛的小屋")
        active_skin_key = r_info.get("active_skin", "skin_default")
        active_bg_key = r_info.get("active_bg", "bg_default")
        
        # 🟢 安全讀取故事等級
        try:
            current_story_level = int(float(r_info.get("story_level", 0)))
        except:
            current_story_level = 0
        
        active_bg_css = STORE_ITEMS.get(active_bg_key, STORE_ITEMS["bg_default"])["css"]
        st.markdown(f"""<style>.pet-stage {{ {active_bg_css} }}</style>""", unsafe_allow_html=True)

        r_users = get_room_users(room_id)
        partner = r_users[r_users["username"] != str(me["username"])]
        if not partner.empty:
            partner = partner.iloc[0].to_dict()
            p_name, p_avatar = partner["nickname"], partner["avatar"]
        else:
            p_name, p_avatar = "等待中...", "⏳"

        df = get_game_df(room_id)
        my_score = df[df["使用者名稱"]==me["nickname"]]["點數"].sum() if not df.empty else 0
        p_score = df[df["使用者名稱"]==p_name]["點數"].sum() if not df.empty else 0
        joint_score = int(my_score + p_score)
        
        if active_skin_key == "skin_default":
            pet_icon, pet_title, pet_desc = get_pet_evolution(joint_score)
        else:
            skin_data = STORE_ITEMS.get(active_skin_key, STORE_ITEMS["skin_default"])
            pet_icon = skin_data["icon"]
            pet_title = skin_data["name"]
            pet_desc = skin_data["desc"]
        
        st.markdown(f"""<div class="hero-card"><h1>{room_name}</h1><p>{me['avatar']} {me['nickname']} × {p_avatar} {p_name}</p></div>""", unsafe_allow_html=True)

        tabs = st.tabs(["🏡 首頁", "📖 故事", "🛍️ 商城", "💌 情書", "📸 回憶", "🎯 任務", "⚙️ 設定"])

        # Tab 1: 首頁
        with tabs[0]:
            st.markdown(f"""
            <div class="pet-stage">
                <div class="pet-emoji">{pet_icon}</div>
                <h2 style="margin-top:color: #000000;">{pet_title}</h2>
                <p style="opacity:0.8;">{pet_desc}</p>
                <div style="margin-top:25px; background:rgba(255,255,255,0.5); padding:10px; border-radius:15px;">
                    <small>共同積分: {joint_score}</small>
                    <progress value="{min(joint_score, 5000)}" max="5000" style="width:100%; height:10px; border-radius:5px;"></progress>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px;"><h4>{me['avatar']} 我</h4><div class="stat-number">{int(my_score)}</div></div>""", unsafe_allow_html=True)
            with c2: st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px;"><h4>{p_avatar} 伴侶</h4><div class="stat-number">{int(p_score)}</div></div>""", unsafe_allow_html=True)
            
            today_w = get_today_word()
            today_date = date.today().strftime("%Y-%m-%d")
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="margin-bottom:10px;"> {today_date} 今日情話</h4>
                <h2 style="color:#6c5ce7; margin:0;">{today_w['word']}</h2>
                <p style="font-size:1.1em;"><b>{today_w['ch']}</b></p>
                <p style="color:#666; font-style:italic;">"{today_w['sentence']}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            if has_today_action(df, me["nickname"], "口說"):
                st.button("✅ 今日已打卡", disabled=True, use_container_width=True, key="btn_checkin_done")
            else:
                if st.button("🗣️ 每日口說打卡 (+30pt)", type="primary", use_container_width=True, key="btn_checkin"):
                    save_action(room_id, me["nickname"], me["gender"], "口說", today_w["word"], 30)
                    st.toast("打卡成功！寵物獲得能量 ✨", icon="🍖")
                    time.sleep(1)
                    st.rerun()

        # Tab 2: 故事挑戰 (闖關版)
        with tabs[1]:
            st.header(f"📖 故事閱讀 (Level {current_story_level + 1})")
            
            # 依據等級選故事 (循環)
            story_idx = current_story_level % len(STORY_BANK)
            story = STORY_BANK[story_idx]
            
            # 階段 1: 閱讀模式
            if st.session_state.quiz_phase == "reading":
                st.markdown("""
                <div class="rule-box-blue">
                    <b>📜 故事挑戰規則：</b><br>
                    1. 閱讀雙語短篇故事。<br>
                    2. 按下「開始挑戰」進入隨堂考。<br>
                    3. 每題限時 <b>40秒</b>，<b>全對</b> 即可解鎖下一關並獲得 <b>100分</b>！
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"### {story['title']}")
                st.image(story['image'], use_container_width=True)
                
                with st.expander("📖 閱讀故事 (中英對照)", expanded=True):
                    st.markdown(f"**{story['content_en']}**")
                    st.divider()
                    st.markdown(f"{story['content_ch']}")
                
                st.subheader("🔑 重點單字")
                for v in story['vocab']: st.markdown(f"<span class='vocab-tag'>{v['word']}</span> : {v['ch']}", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔥 我準備好了！開始挑戰", type="primary", use_container_width=True, key="start_qz"):
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
                    st.warning("⏱️ 限時 40 秒")
                    st.info(f"翻譯：**{q_data['ch']}**")
                    user_ans = st.text_input("答案", key=f"q_in_{q_idx}")
                    if st.button("送出", key="sub_qz"):
                        time_used = time.time() - st.session_state.quiz_start_time
                        is_correct = (time_used <= 40) and (user_ans.strip().lower() == q_data['word'].lower())
                        st.session_state.quiz_score_sheet.append(is_correct)
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
                st.markdown(f"### 結果: {'🎉 全對' if is_perfect else '😢 加油'}")
                if is_perfect:
                    # 🟢 強制升級按鈕
                    if st.button("領獎並前往下一關 (+100)", key="claim_qz_next"):
                        save_action(room_id, me["nickname"], me["gender"], "挑戰", f"完美通關: {story['title']}", 100)
                        # 強制寫入新等級
                        success = update_room_story_level(room_id, current_story_level + 1)
                        if success:
                            st.toast("升級成功！正在載入下一關...", icon="🚀")
                            time.sleep(1) # 強制等待存檔
                            st.session_state.quiz_phase = "reading"
                            st.rerun()
                        else:
                            st.error("存檔失敗，請再試一次")
                else:
                    if st.button("重來", key="retry_qz"):
                        st.session_state.quiz_phase = "reading"
                        st.rerun()

        # Tab 3: 商城
        with tabs[2]:
            st.header("🛍️ 寵物精品店")
            st.info(f"💰 你的可用餘額：{int(my_score)} pt")
            inventory = get_inventory(room_id)
            tab_skin, tab_bg = st.tabs(["👗 造型", "🖼️ 背景"])
            
            with tab_skin:
                cols = st.columns(2)
                for idx, (key, item) in enumerate(STORE_ITEMS.items()):
                    if item["type"] == "skin":
                        with cols[idx % 2]:
                            with st.container(border=True):
                                st.markdown(f"<div style='font-size:40px; text-align:center;'>{item['icon']}</div>", unsafe_allow_html=True)
                                st.markdown(f"**{item['name']}**")
                                is_owned = (key in inventory) or (key == "skin_default")
                                if key == active_skin_key:
                                    st.button("使用中", key=f"sk_act_{key}", disabled=True, use_container_width=True)
                                elif is_owned:
                                    if st.button("裝備", key=f"sk_eq_{key}", use_container_width=True):
                                        update_room_look(room_id, key, "skin")
                                        st.rerun()
                                else:
                                    if st.button(f"💰 {item['price']}", key=f"sk_buy_{key}", use_container_width=True):
                                        if can_afford(my_score, -item['price']):
                                            save_action(room_id, me["nickname"], me["gender"], "購買", item['name'], -item['price'])
                                            add_to_inventory(room_id, key)
                                            st.rerun()
                                        else: st.error("錢不夠")

            with tab_bg:
                cols = st.columns(2)
                for idx, (key, item) in enumerate(STORE_ITEMS.items()):
                    if item["type"] == "bg":
                        with cols[idx % 2]:
                            with st.container(border=True):
                                st.markdown(f"<div style='width:100%; height:50px; border-radius:8px; {item['css']}'></div>", unsafe_allow_html=True)
                                st.markdown(f"**{item['name']}**")
                                is_owned = (key in inventory) or (key == "bg_default")
                                if key == active_bg_key:
                                    st.button("使用中", key=f"bg_act_{key}", disabled=True, use_container_width=True)
                                elif is_owned:
                                    if st.button("套用", key=f"bg_eq_{key}", use_container_width=True):
                                        update_room_look(room_id, key, "bg")
                                        st.rerun()
                                else:
                                    if st.button(f"💰 {item['price']}", key=f"bg_buy_{key}", use_container_width=True):
                                        if can_afford(my_score, -item['price']):
                                            save_action(room_id, me["nickname"], me["gender"], "購買", item['name'], -item['price'])
                                            add_to_inventory(room_id, key)
                                            st.rerun()
                                        else: st.error("錢不夠")

        # Tab 4: 情書
        with tabs[3]:
            st.header("💌 情書")
            st.markdown("""<div class="rule-box-pink"><b>📜 規則：</b> 寫下悄悄話並上鎖（可附照片），對方解鎖成功可得 <b>+20 分</b>。</div>""", unsafe_allow_html=True)
            with st.expander("寫信 (可附圖)"):
                txt = st.text_area("內容")
                img = st.file_uploader("附圖", type=["png", "jpg", "jpeg"])
                if st.button("🔒 送出", key="snd_ltr"):
                    if txt:
                        p = save_uploaded_image(img)
                        send_secret_message(room_id, me["nickname"], txt, p)
                        st.success("已送出")
            msgs = get_room_messages(room_id)
            for idx, msg in msgs.iterrows():
                st.markdown(f"**{msg['sender']}**: {msg['status']}")
                if msg['status'] == 'LOCKED' and msg['sender'] != me['nickname']:
                    if st.button("解鎖", key=f"ul_{idx}"):
                        st.session_state.unlock_target = msg['timestamp']
                        st.session_state.unlock_quiz = random.choice(CONTENT_BANK)
                        st.rerun()
            if "unlock_target" in st.session_state:
                st.warning("解鎖中...")
                ans = st.text_input(f"翻譯: {st.session_state.unlock_quiz['ch']}", key="ul_ans")
                if st.button("確認", key="ul_conf"):
                    if ans.lower() == st.session_state.unlock_quiz['word'].lower():
                        unlock_message(room_id, st.session_state.unlock_target)
                        del st.session_state.unlock_target
                        st.rerun()

       # Tab 5: 回憶 (含照片上傳功能)
        with tabs[4]:
            st.header("📸 回憶牆")
            
            # --- 新增區塊 ---
            with st.expander("➕ 新增美好回憶", expanded=False):
                m_title = st.text_input("標題 (例如: 第一次去海邊)")
                m_desc = st.text_area("內容 (例如: 風很大，但很開心)")
                m_mood = st.selectbox("心情", ["😍 開心", "😊 平靜", "😭 感動", "🥳 慶祝", "😡 生氣"])
                
                # 👇 這裡是關鍵：上傳照片的按鈕
                m_img = st.file_uploader("上傳照片 (選填)", type=["png", "jpg", "jpeg"], key="uploader_mem")
                
                if st.button("💾 儲存回憶", key="btn_save_mem"):
                    if m_title:
                        # 1. 先把圖片存到 images 資料夾，並取得路徑
                        img_path = save_uploaded_image(m_img)
                        
                        # 2. 把路徑存進資料庫
                        add_memory(room_id, m_title, m_desc, m_mood, img_path)
                        
                        st.toast("回憶已保存！", icon="📸")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("請至少輸入標題喔！")

            st.divider()

            # --- 顯示區塊 ---
            mems = get_memories(room_id)
            if mems.empty:
                st.info("目前還沒有回憶，快去新增第一筆吧！")
            else:
                for idx, row in mems.iterrows():
                    with st.container(border=True):
                        # 標題區
                        c1, c2 = st.columns([1, 5])
                        with c1: st.write(f"## {row['mood'][0]}") # 取心情的第一個字(emoji)
                        with c2:
                            st.subheader(row['title'])
                            st.caption(f"📅 {row['date']}")
                        
                        # 內容文字
                        if row['desc']:
                            st.write(row['desc'])
                        
                        # 👇 這裡是關鍵：如果有照片路徑，就顯示出來
                        if str(row['image_path']) != "None" and os.path.exists(str(row['image_path'])):
                            st.image(str(row['image_path']), use_container_width=True)
        # Tab 6: 任務
        with tabs[5]:
            st.header("🎯 任務 (互評)")
            st.markdown("""<div class="rule-box-orange"><b>📜 規則：</b> 完成後請對方幫你確認打勾！</div>""", unsafe_allow_html=True)
            ensure_today_quests(room_id, QUEST_POOL)
            qs = get_today_quests(room_id)
            if p_name == "等待中...": st.warning("伴侶未加入")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader(f"審核 {p_name}")
                    for idx, q in qs.iterrows():
                        if not has_today_action(df, p_name, q["quest_key"]):
                            if st.button(f"確認 {q['desc']}", key=f"v_{idx}"):
                                save_action(room_id, p_name, partner['gender'], q["quest_key"], "任務", int(q["reward"]))
                                st.rerun()
                with c2:
                    st.subheader("我的進度")
                    for idx, q in qs.iterrows():
                        done = has_today_action(df, me["nickname"], q["quest_key"])
                        st.write(f"{q['emoji']} {q['desc']} - {'✅' if done else '⏳'}")

       # Tab 7: 設定
        with tabs[6]:
            st.header("⚙️ 設定與管理")
            
            # --- 1. 個人資料修改 ---
            with st.expander("👤 修改個人資料"):
                new_nick = st.text_input("新暱稱", value=me['nickname'])
                new_avatar = st.selectbox("新頭像", AVATARS, index=AVATARS.index(me['avatar']) if me['avatar'] in AVATARS else 0)
                if st.button("儲存個人資料"):
                    update_user_profile(me['username'], new_nick, new_avatar)
                    # 即時更新 session，不用重登就能看到變化
                    st.session_state.user_session['nickname'] = new_nick
                    st.session_state.user_session['avatar'] = new_avatar
                    st.success("個人資料已更新！")
                    time.sleep(1)
                    st.rerun()

            # --- 2. 房間名稱修改 ---
            with st.expander("🏠 修改小屋名稱"):
                new_room_name_input = st.text_input("新小屋名稱", value=room_name)
                if st.button("儲存小屋名稱"):
                    update_room_info(room_id, new_name=new_room_name_input)
                    st.success("小屋名稱已更新！")
                    time.sleep(1)
                    st.rerun()

            # --- 3. 房間密碼修改 ---
            with st.expander("🔐 重設房間密碼"):
                st.warning("⚠️ 注意：這是你們共用的房間密碼。修改後請務必告訴另一半，否則他會進不來喔！")
                new_room_pass = st.text_input("設定新密碼", type="password")
                if st.button("確認重設密碼"):
                    if new_room_pass:
                        update_room_info(room_id, new_pass=new_room_pass)
                        st.success("密碼已重設！請牢記新密碼。")
                    else:
                        st.error("密碼不能為空")

            st.divider()
            
            # --- 離開與登出 ---
            col_set1, col_set2 = st.columns(2)
            with col_set1:
                if st.button("🚪 離開房間", key="leave_room_btn"):
                    update_user_room(me["username"], "None")
                    st.session_state.user_session["room_id"] = "None"
                    st.rerun()
            with col_set2:
                if st.button("👋 登出帳號", key="logout_btn_settings"):
                    st.session_state.user_session = None
                    st.rerun()
            
            # --- 危險區域 ---
            with st.expander("⚠️ 危險區域 (重置資料)"):
                st.warning("這將會清空本房間所有的積分、購買紀錄和任務進度！(回憶和情書會保留)")
                if st.button("🧹 確定重置房間數據", key="reset_data_btn"):
                    reset_room_data(room_id)
                    # 如果有做庫存系統，也要考慮是否重置 inventory
                    st.toast("已重置所有積分與數據", icon="🧹")
                    st.rerun()