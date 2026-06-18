import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Data Engineer RPG", page_icon="⚔️", layout="centered")

# 2. Initialize Game State (Simulating an in-memory database)
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "quests" not in st.session_state:
    # Starting default quests
    st.session_state.quests = [
        {"id": 1, "task": "Write 1 complex SQL query", "type": "Daily Quest", "xp_reward": 20, "completed": False},
        {"id": 2, "task": "Debug a Python script for 20 mins", "type": "Daily Quest", "xp_reward": 25, "completed": False},
        {"id": 3, "task": "Finish Portfolio Project ReadMe File", "type": "Boss Fight", "xp_reward": 100, "completed": False},
    ]

# 3. Game Logic Functions
XP_PER_LEVEL = 100

def add_quest(task_name, quest_type):
    new_id = len(st.session_state.quests) + 1
    xp_amount = 100 if quest_type == "Boss Fight" else 25
    st.session_state.quests.append({
        "id": new_id,
        "task": task_name,
        "type": quest_type,
        "xp_reward": xp_amount,
        "completed": False
    })

def complete_quest(quest_id, xp_reward):
    for quest in st.session_state.quests:
        if quest["id"] == quest_id and not quest["completed"]:
            quest["completed"] = True
            st.session_state.xp += xp_reward
            
            # Level Up Logic
            if st.session_state.xp >= XP_PER_LEVEL:
                st.session_state.level += 1
                st.session_state.xp = st.session_state.xp - XP_PER_LEVEL
                st.balloons()
                st.success(f"🎉 LEVEL UP! You reached Level {st.session_state.level}! 🎉")

# 4. App UI Layout
st.title("⚔️ Data Engineer Career RPG")
st.subheader("Turn your daily grinds into career levels.")

# Sidebar: Character Status Panel
with st.sidebar:
    st.header("👤 Character Status")
    st.markdown(f"### **Level {st.session_state.level}**")
    
    # XP Progress Bar
    xp_progress = min(st.session_state.xp / XP_PER_LEVEL, 1.0)
    st.progress(xp_progress)
    st.write(f"XP: {st.session_state.xp} / {XP_PER_LEVEL}")
    
    st.markdown("---")
    st.markdown("✨ *Tip: Complete tasks to earn XP. Keep your streak alive!*")

# Main Section: Add New Quests
st.markdown("### ➕ Forge a New Quest")
with st.form("quest_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        task_input = st.text_input("What is your next career objective?", placeholder="e.g., Learn AWS S3 basics...")
    with col2:
        type_input = st.selectbox("Quest Type", ["Daily Quest", "Boss Fight"])
    
    submit_button = st.form_submit_submit_button = st.form_submit_button("Add to Quest Log")
    if submit_button and task_input:
        add_quest(task_input, type_input)
        st.toast("Quest successfully added to log!", icon="📜")

# Main Section: Active Quest Log
st.markdown("### 📜 Active Quest Log")
active_quests = [q for q in st.session_state.quests if not q["completed"]]

if not active_quests:
    st.info("All quests cleared! Your schedule is clear. Go enjoy your RPG gaming reward! 🎮")
else:
    for quest in active_quests:
        # Style different quest types visually
        if quest["type"] == "Boss Fight":
            bg_color = "🔴 **[BOSS FIGHT]**"
        else:
            bg_color = "🔹 **[DAILY]**"
            
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.markdown(f"{bg_color} {quest['task']} *(Reward: +{quest['xp_reward']} XP)*")
        with col_btn:
            if st.button("Claim XP", key=f"btn_{quest['id']}", type="primary"):
                complete_quest(quest["id"], quest["xp_reward"])
                st.rerun()

# Bottom Section: Completed Quests (History Logs)
st.markdown("---")
with st.expander("📚 View Completed Quest Archives"):
    completed_quests = [q for q in st.session_state.quests if q["completed"]]
    if completed_quests:
        df = pd.DataFrame(completed_quests)[["type", "task", "xp_reward"]]
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No completed archives found for today.")
