import streamlit as st
from database import init_db, seed_data, get_categories, get_all_functionalities
from agent import create_agent

st.set_page_config(page_title="Hospital Support Agent", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #D4AF37, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .sub-header { text-align: center; color: #999; margin-bottom: 1.5rem; }
    .stApp { background: #0d0d0d; }
    .stMarkdown, p, h2, h3 { color: #ddd; }
    .stButton button { background: #D4AF37 !important; color: #1a1a1a !important; font-weight: 600 !important; }
    .stat-box { background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .stat-number { font-size: 2rem; font-weight: bold; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

init_db()
seed_data()

@st.cache_resource
def get_agent():
    return create_agent()

agent = get_agent()

with st.sidebar:
    st.title(" Hospital Agent")
    st.caption("AI-Powered Hospital Support")
    st.divider()
    
    funcs = get_all_functionalities()
    cats = get_categories()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(funcs)}</div><div>Services</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(cats)}</div><div>Categories</div></div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("###  Tools")
    st.markdown("- `search_functionalities`")
    st.markdown("- `get_steps`")
    st.markdown("- `list_categories`")
    st.markdown("- `search_by_keyword`")
    
    st.divider()
    st.markdown("###  Try These")
    st.markdown("- I need to see a doctor")
    st.markdown("- show all services")
    st.markdown("- my test results")
    st.markdown("- how much do I owe")
    st.markdown("- need ambulance")
    st.markdown("- refill my prescription")
    st.markdown("- I'm being discharged")
    st.markdown("- need specialist referral")

st.markdown('<p class="main-header"> Hospital Support Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI Agent + 4 Tools → SQLite (24 Hospital Services)</p>', unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("How can we help you today?")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner("Checking hospital services..."):
            try:
                result = agent.invoke({"input": query})
                response = result["output"]
            except Exception as e:
                response = f" Error: {e}"
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

elif not st.session_state.messages:
    st.markdown("""
    ###  Hospital Support Agent
    
    This AI agent helps patients find the right hospital service.
    
    **7 Categories, 22 Services:**
    -  Appointments (schedule, cancel, reschedule, walk-in)
    -  Medical Records (test results, prescriptions, history)
    -  Billing & Insurance (payment, claims, coverage)
    -  Emergency (ER guide, ambulance)
    -  Pharmacy (refills, drug info, OTC)
    -  Inpatient (admission, discharge, room service)
    -  Referrals (specialist, second opinion)
    
    **Try asking:**
    - `I need to see a doctor`
    - `show all services`
    - `my test results`
    - `how much do I need to pay`
    """)

st.markdown("---")
