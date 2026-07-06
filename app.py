import streamlit as st
import random
import time
import json
import os

# --- 2000s Retro Minimalist Web Aesthetic Styling ---
st.set_page_config(page_title="Can You Spot The Bot?", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #FBFAFB;
        color: #111111;
        font-family: "Courier New", Courier, monospace;
    }
    .retro-box {
        background-color: #FFFFFF;
        padding: 20px;
        border: 3px solid #111111;
        border-radius: 0px;
        box-shadow: 6px 6px 0px #111111;
        margin-bottom: 25px;
    }
    h1, h2, h3 {
        color: #111111 !important;
        font-family: "Impact", "Arial Black", sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 2px solid #111111 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        box-shadow: 3px 3px 0px #111111 !important;
        transition: all 0.1s ease;
    }
    div.stButton > button:hover {
        transform: translate(-1px, -1px) !important;
        box-shadow: 4px 4px 0px #111111 !important;
    }
    div.stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #111111 !important;
    }
    </style>
    """, unsafe_allow_html=True)

JSON_FILE = "survey_results.json"

try:
    ADMIN_PASSWORD = st.secrets["admin_password"]
except Exception:
    ADMIN_PASSWORD = "s0s0b00m."

def load_scores():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try: return json.load(f)
            except json.JSONDecodeError: return []
    return []

def save_score(name, age, screen_time, final_score, speed, details):
    all_records = load_scores()
    all_records.append({
        "name": name,
        "age_group": age,
        "tiktok_usage": screen_time,
        "score": final_score,
        "avg_speed_seconds": round(speed, 2),
        "timestamp": time.strftime("%H:%M:%S"),
        "raw_responses": details
    })
    with open(JSON_FILE, "w") as f:
        json.dump(all_records, f, indent=4)

# --- Dataset (Now with Carrot Cake Trap) ---
DATASET = [
    {"topic": "Father Boundaries", "human": "why is everyone hating💀 pure rays of sunshine", "ai": "thats not the flex you think it is"},
    {"topic": "Chico & Jordan Barrett", "human": "bro jordan barrett didnt age a bit 💀", "ai": "chico and jordan in the same vid is crazy"},
    {"topic": "Anime Attachment", "human": "me with like 80% of anime’s I’ve seen bc I get attached", "ai": "i still havent found an anime that hits the same 😭"},
    {"topic": "Scooter Breakup", "human": "You can’t look cool on an e scooter it’s js not possible", "ai": "ngl id still be on that scooter"},
    {"topic": "Summer Lazy Routine", "human": "Sleepin at 9 am waking up at 5 pm peak life", "ai": "basically my whole summer 😭"},
    {"topic": "World Cup Match", "human": "bro is playing with newbie", "ai": "this game was actually insane"},
    {"topic": "Blurry Glasses POV", "human": "I js put my glasses on aswell what 😭", "ai": "i be staring until they wave 😭"},
    {"topic": "Elizabeth 59-Year Letter", "human": "I'll be 59 😱", "ai": "imagine opening it and its just one sentence 😭"},
    {"topic": "Carrot Cake Warning", "human": "carrot cake genuinely clears all other cake and I'll die on that hill", "ai": "the little carrot drawing is an absolute power move ngl it’s basically marking its territory 😭"},
    {"topic": "Apple Pay Dog Race", "human": "Its one am and im sharing a hotel room ts frying tf out of me", "ai": "why are they so fast 😭"}
]

# --- Video URLs Order (Update these links when ready) ---
VIDEO_URLS = {
    "Father Boundaries": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/father_boundaries.mp4",
    "Chico & Jordan Barrett": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/chico_jordan.mp4",
    "Anime Attachment": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/anime_attach.mp4",
    "Scooter Breakup": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/scooter.mp4",
    "Summer Lazy Routine": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/summer_lazy.mp4",
    "World Cup Match": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/world_cup.mp4",
    "Blurry Glasses POV": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/glasses_pov.mp4",
    "Elizabeth 59-Year Letter": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/elizabeth_letter.mp4",
    "Carrot Cake Warning": "https://assets.mixkit.co/videos/preview/mixkit-decorating-a-chocolate-cake-with-cream-42232-large.mp4",
    "Apple Pay Dog Race": "https://pub-c5e31b5cdafb419a86d611bfb267ecb2.r2.dev/dog_race.mp4"
}

if "state" not in st.session_state:
    st.session_state.state = "start"
    st.session_state.player_name = ""
    st.session_state.age_group = ""
    st.session_state.screen_time = ""
    st.session_state.q_idx = 0
    st.session_state.points = 0
    st.session_state.total_timer = 0.0
    st.session_state.log = []
    st.session_state.deck = DATASET.copy()
    random.shuffle(st.session_state.deck)
    st.session_state.flips = [random.choice([0, 1]) for _ in range(10)]
    st.session_state.layout = [random.sample(["Real Person", "AI Bot"], 2) for _ in range(10)]
    st.session_state.click_time = None
    st.session_state.name_warning = False

# --- PAGE 1: ENTER NAME & METRICS ---
if st.session_state.state == "start":
    st.title("🤖 CAN YOU SPOT THE BOT?")
    st.write("TikTok comments are rotting. Half of them are written by computers. Can you tell the difference or is your brain completely fried?")
    
    st.markdown('<div class="retro-box">', unsafe_allow_html=True)
    
    name_label = "i need a name to track how badly you do n make a study about it ;)" if st.session_state.name_warning else "ENTER YOUR NAME:"
    name_input = st.text_input(name_label, placeholder="Slayer99...", max_chars=20)
    
    st.write("<br><b>SELECT YOUR AGE COHORT:</b>", unsafe_allow_html=True)
    age_input = st.selectbox("label_hidden_age", ["13–15", "16–18", "19–22", "23+"], label_visibility="collapsed")
    
    st.write("<br><b>THE AMOUNT OF TIME YOU SPEND ON SOCIAL MEDIA:</b>", unsafe_allow_html=True)
    usage_input = st.selectbox("label_hidden_usage", ["<1 hour", "1–3 hours", "3–5 hours", "5+ hours"], label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("START TEST AND HELP MAKE A STUDY ABOUT IT →", use_container_width=True):
        if not name_input.strip():
            st.session_state.name_warning = True
            st.rerun()
        else:
            st.session_state.player_name = name_input.strip()
            st.session_state.age_group = age_input
            st.session_state.screen_time = usage_input
            st.session_state.state = "play"
            st.session_state.click_time = time.time()
            st.rerun()

# --- PAGE 2: THE PLAYGROUND ---
elif st.session_state.state == "play":
    idx = st.session_state.q_idx
    current = st.session_state.deck[idx]
    bot_active = st.session_state.flips[idx]
    
    st.subheader(f"ROUND {idx + 1} / 10")
    st.progress(idx / 10)
    
    st.video(VIDEO_URLS.get(current["topic"], ""), loop=True, autoplay=True)
    shown_text = current["ai"] if bot_active else current["human"]
    
    st.markdown(f"""
    <div class="retro-box" style="text-align: center;">
        <span style="font-size: 0.8rem; font-weight: bold; color: #555;">COMMENT UNDER VIDEO:</span>
        <p style="font-size: 1.4rem; font-weight: bold; margin: 10px 0; color: #000;">"{shown_text}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    btns = st.session_state.layout[idx]
    col1, col2 = st.columns(2)
    
    selection = None
    if col1.button(btns[0].upper(), use_container_width=True, key=f"b1_{idx}"):
        selection = btns[0]
    if col2.button(btns[1].upper(), use_container_width=True, key=f"b2_{idx}"):
        selection = btns[1]
        
    if selection is not None:
        duration = time.time() - st.session_state.click_time
        st.session_state.total_timer += duration
        
        answer_key = "AI Bot" if bot_active else "Real Person"
        win = 1 if selection == answer_key else 0
        if win: st.session_state.points += 1
        
        st.session_state.log.append({
            "topic": current["topic"],
            "picked": selection,
            "was_correct": win,
            "seconds": round(duration, 2)
        })
        
        if idx + 1 < 10:
            st.session_state.q_idx += 1
            st.session_state.click_time = time.time()
        else:
            save_score(
                st.session_state.player_name,
                st.session_state.age_group,
                st.session_state.screen_time,
                st.session_state.points, 
                st.session_state.total_timer / 10, 
                st.session_state.log
            )
            st.session_state.state = "over"
        st.rerun()

# --- PAGE 3: THE ROAST & SCOREBOARD ---
elif st.session_state.state == "over":
    st.title("🚨 TEST COMPLETE")
    st.write("*stares awkwardly in binary code*... calculated metrics below:")
    
    score = st.session_state.points
    name = st.session_state.player_name
    
    st.markdown('<div class="retro-box" style="text-align:center;">', unsafe_allow_html=True)
    st.write(f"### {name}'s Score: {score} / 10")
    st.write(f"Average speed: {st.session_state.total_timer / 10:.2f} seconds")
    
    if score <= 4:
        st.error("🧠 YOU ABSOLUTELY SUCK. A basic chat-bot completely fooled you. Thx for participating <3")
    elif 5 <= score <= 7:
        st.warning("😐 IDK WHAT TO TELL YA UR A LITTLE SHIT BUT A LITTLE GOOD. Thx for participating <3")
    else:
        st.success("👑 LEGEND. You can actually smell the code. Your brain isn't entirely mush yet. Thx for participating <3")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### 🏆 SCOREBOARD")
    history = load_scores()
    if history:
        sorted_history = sorted(history, key=lambda x: (-x["score"], x["avg_speed_seconds"]))
        
        table_html = "<table style='width:100%; border:3px solid #111; border-collapse:collapse; background:#fff; color:#111; font-family:monospace;'>"
        table_html += "<tr style='background:#111; color:#fff; text-align:center;'><th style='padding:10px; border:1px solid #111;'>RANK</th><th style='padding:10px; border:1px solid #111;'>NAME</th><th style='padding:10px; border:1px solid #111;'>SCORE</th><th style='padding:10px; border:1px solid #111;'>SPEED</th></tr>"
        
        for rank, entry in enumerate(sorted_history[:10], 1):
            table_html += "<tr style='text-align:center; background:#fff; color:#111;'>"
            table_html += f"<td style='padding:10px; border:1px solid #111; font-weight:bold;'>#{rank}</td>"
            table_html += f"<td style='padding:10px; border:1px solid #111;'>{entry['name']}</td>"
            table_html += f"<td style='padding:10px; border:1px solid #111; font-weight:bold;'>{entry['score']}/10</td>"
            table_html += f"<td style='padding:10px; border:1px solid #111;'>{entry['avg_speed_seconds']}s</td>"
            table_html += "</tr>"
            
        table_html += "</table><br>"
        st.markdown(table_html, unsafe_allow_html=True)

# --- 🔒 HIDDEN ADMIN PANEL ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🛠️ Admin Panel"):
    with st.form(key="admin_form"):
        token = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label="Unlock Panel", use_container_width=True)
    
    if token == ADMIN_PASSWORD:
        records = load_scores()
        st.success(f"🔓 Access Granted. Total active rows: {len(records)}")
        
        st.download_button(
            label="Download Master Data (JSON)",
            data=json.dumps(records, indent=4),
            file_name="all_player_scores.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("<hr style='border:1px dashed #111;'>", unsafe_allow_html=True)
        st.write("⚠️ **DANGER ZONE**")
        
        if st.button("🔴 WIPE ALL SCOREBOARD RECORDS", use_container_width=True):
            if os.path.exists(JSON_FILE):
                with open(JSON_FILE, "w") as f:
                    json.dump([], f)
                st.success("Database wiped clean! Refreshing...")
                time.sleep(1)
                st.rerun()
    elif token and token != ADMIN_PASSWORD:
        st.error("❌ Incorrect Password")
