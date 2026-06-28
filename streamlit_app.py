# streamlit_app.py
import streamlit as st
from datetime import datetime
from main import agent_loop
from memory import save_memory

st.set_page_config(
    page_title="Book Search Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ──────────────────────────────────────────────────
if "result"         not in st.session_state: st.session_state.result         = None
if "current_query"  not in st.session_state: st.session_state.current_query  = ""
if "search_history" not in st.session_state: st.session_state.search_history = []
if "dark_mode"      not in st.session_state: st.session_state.dark_mode      = True
if "submitted"      not in st.session_state: st.session_state.submitted      = False

dm = st.session_state.dark_mode

# ── Tokens ────────────────────────────────────────────────────────
if dm:
    BG=("#0F0F13"); SB=("#16161D"); CARD=("#1E1E2A"); CARD2=("#252535")
    BORDER=("#2E2E42"); T1=("#F0EEFF"); T2=("#9090B0"); T3=("#3A3A58")
    ACCENT=("#7C6EF5"); ACCENT2=("#5B4FD6"); INPUT=("#1A1A26")
    SHADOW=("rgba(0,0,0,0.5)"); PL=("#2D2850"); GLASS=("rgba(22,22,29,0.92)")
else:
    BG=("#F4F3FF"); SB=("#FFFFFF"); CARD=("#FFFFFF"); CARD2=("#F0EEFF")
    BORDER=("#E2E0F5"); T1=("#1A1830"); T2=("#6860A8"); T3=("#B0A8D8")
    ACCENT=("#6C5CE7"); ACCENT2=("#5048C0"); INPUT=("#FFFFFF")
    SHADOW=("rgba(108,92,231,0.12)"); PL=("#EDE9FF"); GLASS=("rgba(255,255,255,0.95)")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}

html,body,.stApp{{
  background:{BG}!important;
  font-family:'Inter',sans-serif;
  color:{T1};
  -webkit-font-smoothing:antialiased;
}}
#MainMenu,footer,header{{visibility:hidden}}
.block-container{{padding:0!important;max-width:100%!important}}
section[data-testid="stMain"]>div{{padding:0!important}}
[data-testid="stSidebar"]{{display:none!important}}
div[data-testid="column"]{{padding:0 6px!important}}

/* ── TOPBAR ── */
.topbar{{
  background:{GLASS};
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid {BORDER};
  display:flex;align-items:center;
  padding:0 24px;gap:12px;
  height:62px;
  position:sticky;top:0;z-index:200;
}}
.tb-logo{{
  font-size:20px;font-weight:700;
  color:{ACCENT};letter-spacing:-0.5px;
  display:flex;align-items:center;gap:8px;
}}
.tb-sub{{font-size:12px;color:{T3};font-weight:400}}
.tb-space{{flex:1}}
.tb-pill{{
  display:flex;align-items:center;gap:6px;
  padding:6px 14px;border-radius:20px;
  background:{CARD2};border:1px solid {BORDER};
  font-size:12px;color:{T2};font-weight:500;
}}
.avatar{{
  width:34px;height:34px;border-radius:10px;
  background:linear-gradient(135deg,{ACCENT},{ACCENT2});
  display:flex;align-items:center;justify-content:center;
  font-size:13px;font-weight:700;color:#fff;
}}

/* ── LAYOUT ── */
.layout{{display:flex;height:calc(100vh - 62px);overflow:hidden}}

/* ── SIDEBAR ── */
.sidebar{{
  width:270px;flex-shrink:0;
  background:{SB};
  border-right:1px solid {BORDER};
  display:flex;flex-direction:column;
  padding:16px 12px;gap:4px;
  overflow-y:auto;overflow-x:hidden;
}}
.sb-section{{
  font-size:10px;font-weight:600;
  letter-spacing:1.8px;text-transform:uppercase;
  color:{T3};padding:14px 8px 6px;
}}
.sb-item{{
  display:flex;align-items:center;gap:10px;
  padding:9px 12px;border-radius:10px;
  font-size:13px;color:{T2};
  cursor:default;transition:all 0.15s;
  border:1px solid transparent;
  white-space:nowrap;overflow:hidden;
}}
.sb-item:hover{{background:{PL};color:{ACCENT};border-color:{BORDER}}}
.sb-divider{{height:1px;background:{BORDER};margin:8px 0}}
.sb-footer{{margin-top:auto;padding-top:12px;display:flex;flex-direction:column;gap:6px}}

/* ── MAIN ── */
.main{{
  flex:1;
  display:flex;flex-direction:column;
  overflow:hidden;
  background:{BG};
}}

/* ── SEARCH BAR (top of main) ── */
.searchbar-wrap{{
  padding:20px 32px 16px;
  border-bottom:1px solid {BORDER};
  background:{GLASS};
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
}}
.searchbar-inner{{
  max-width:760px;
  margin:0 auto;
}}
.searchbar-label{{
  font-size:11px;font-weight:600;
  letter-spacing:1.5px;text-transform:uppercase;
  color:{T3};margin-bottom:10px;
}}

/* ── RESULTS AREA ── */
.results-scroll{{
  flex:1;overflow-y:auto;
  padding:32px;
}}
.results-scroll::-webkit-scrollbar{{width:4px}}
.results-scroll::-webkit-scrollbar-thumb{{background:{BORDER};border-radius:4px}}
.results-inner{{max-width:760px;margin:0 auto}}

/* ── RESULT HEADER ── */
.result-header{{
  display:flex;align-items:center;gap:12px;
  margin-bottom:24px;
  padding-bottom:16px;
  border-bottom:1px solid {BORDER};
}}
.result-query{{
  font-size:22px;font-weight:700;
  color:{T1};letter-spacing:-0.5px;line-height:1.2;
}}
.result-sub{{
  font-size:13px;color:{T2};font-weight:400;
  margin-top:4px;
}}
.result-badge{{
  margin-left:auto;flex-shrink:0;
  background:linear-gradient(135deg,{ACCENT},{ACCENT2});
  color:#fff;
  font-size:10px;font-weight:600;
  letter-spacing:1.5px;text-transform:uppercase;
  padding:5px 12px;border-radius:20px;
}}

/* ── RESULT CONTENT ── */
.result-content p{{
  font-size:14px;line-height:1.85;
  color:{T2};font-weight:400;
  margin-bottom:12px;
}}
.result-content strong{{color:{T1};font-weight:600}}
.result-content em{{color:{ACCENT};font-style:italic}}
.result-content h3{{
  font-size:17px;font-weight:600;color:{T1};
  margin:24px 0 12px;padding-bottom:8px;
  border-bottom:1px solid {BORDER};
  letter-spacing:-0.3px;
}}
.result-content h4{{
  font-size:11px;font-weight:600;color:{T3};
  text-transform:uppercase;letter-spacing:1.5px;
  margin:18px 0 8px;
}}
.result-content ol{{
  list-style:none;padding:0;margin:0 0 20px;
  counter-reset:item;
}}
.result-content ol li{{
  counter-increment:item;
  display:flex;gap:14px;
  padding:13px 0;
  border-bottom:1px solid {BORDER};
  font-size:14px;line-height:1.7;color:{T2};
  align-items:start;
}}
.result-content ol li::before{{
  content:counter(item,decimal-leading-zero);
  font-size:11px;font-weight:600;
  color:{ACCENT};opacity:0.7;
  padding-top:3px;min-width:24px;flex-shrink:0;
  font-family:monospace;
}}
.result-content ol li:last-child{{border-bottom:none}}
.result-content ol li strong{{color:{T1};font-weight:600}}
.result-content ul{{
  list-style:none;padding:0;margin:0 0 20px;
}}
.result-content ul li{{
  padding:10px 0 10px 20px;
  border-bottom:1px solid {BORDER};
  font-size:14px;color:{T2};
  line-height:1.7;position:relative;
}}
.result-content ul li::before{{
  content:'›';position:absolute;left:0;
  color:{ACCENT};font-size:16px;font-weight:600;
}}
.result-content ul li:last-child{{border-bottom:none}}
.result-content ul li strong{{color:{T1}}}
.result-content hr{{border:none;border-top:1px solid {BORDER};margin:20px 0}}
.result-content code{{
  font-family:monospace;font-size:12px;
  color:{ACCENT};background:{CARD2};
  padding:2px 7px;border-radius:5px;
  border:1px solid {BORDER};
}}

/* ── TABLE ── */
.result-content table,
div[data-testid="stMarkdownContainer"] table{{
  width:100%!important;border-collapse:collapse!important;
  margin:16px 0 24px!important;
  border:1px solid {BORDER}!important;
  border-radius:14px!important;overflow:hidden!important;
}}
.result-content th,
div[data-testid="stMarkdownContainer"] th{{
  background:{CARD2}!important;color:{ACCENT}!important;
  font-size:10px!important;font-weight:600!important;
  letter-spacing:2px!important;text-transform:uppercase!important;
  padding:12px 16px!important;text-align:left!important;
  border:none!important;border-bottom:1px solid {BORDER}!important;
}}
.result-content td,
div[data-testid="stMarkdownContainer"] td{{
  padding:12px 16px!important;border:none!important;
  border-bottom:1px solid {BORDER}!important;
  color:{T2}!important;font-size:13px!important;
  font-weight:400!important;vertical-align:top!important;
  line-height:1.65!important;background:transparent!important;
}}
div[data-testid="stMarkdownContainer"] tbody tr:last-child td{{border-bottom:none!important}}
div[data-testid="stMarkdownContainer"] td strong{{color:{T1}!important;font-weight:600!important}}
div[data-testid="stMarkdownContainer"] tr:nth-child(even) td{{background:rgba(124,110,245,0.03)!important}}

/* ── WELCOME ── */
.welcome{{
  flex:1;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  padding:40px 32px;text-align:center;
}}
.welcome-icon{{font-size:60px;margin-bottom:20px;animation:float 3s ease-in-out infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
.welcome-title{{
  font-size:26px;font-weight:700;color:{T1};
  letter-spacing:-0.5px;margin-bottom:10px;
}}
.welcome-sub{{
  font-size:14px;color:{T2};font-weight:400;
  max-width:420px;line-height:1.7;margin-bottom:36px;
}}
.prompt-grid{{
  display:grid;grid-template-columns:repeat(2,1fr);
  gap:12px;max-width:540px;width:100%;
}}
.prompt-card{{
  background:{CARD};border:1px solid {BORDER};
  border-radius:16px;padding:16px;
  text-align:left;display:flex;
  align-items:flex-start;gap:10px;
  transition:all 0.2s;cursor:default;
}}
.prompt-card:hover{{
  border-color:{ACCENT};background:{PL};
  transform:translateY(-2px);
  box-shadow:0 8px 24px {SHADOW};
}}
.pc-icon{{font-size:20px;flex-shrink:0}}
.pc-title{{font-size:13px;font-weight:500;color:{T1};line-height:1.3}}
.pc-sub{{font-size:11px;color:{T2};margin-top:3px}}

/* ── INPUT ── */
.stTextInput>div>div>input{{
  background:{INPUT}!important;
  border:1.5px solid {BORDER}!important;
  border-radius:14px!important;
  color:{T1}!important;
  font-family:'Inter',sans-serif!important;
  font-size:15px!important;
  font-weight:400!important;
  padding:14px 20px!important;
  height:52px!important;
  caret-color:{ACCENT};
  transition:border-color 0.2s,box-shadow 0.2s;
  box-shadow:0 2px 8px {SHADOW};
}}
.stTextInput>div>div>input:focus{{
  border-color:{ACCENT}!important;
  box-shadow:0 0 0 4px rgba(124,110,245,0.1)!important;
  outline:none!important;
}}
.stTextInput>div>div>input::placeholder{{color:{T3}!important;font-style:italic}}
.stTextInput label{{display:none!important}}
.stTextInput>div{{border:none!important;background:transparent!important}}
.stTextInput>div>div{{border:none!important;background:transparent!important}}

/* ── BUTTONS ── */
div[data-testid="stButton"]>button{{
  background:linear-gradient(135deg,{ACCENT},{ACCENT2})!important;
  color:#fff!important;border:none!important;
  border-radius:12px!important;
  font-family:'Inter',sans-serif!important;
  font-size:13px!important;font-weight:600!important;
  padding:0 20px!important;height:52px!important;
  width:100%!important;
  box-shadow:0 4px 16px {SHADOW}!important;
  transition:all 0.18s!important;
  letter-spacing:0.2px!important;
}}
div[data-testid="stButton"]>button:hover{{
  opacity:0.9!important;transform:translateY(-1px)!important;
}}

.sb-new-btn div[data-testid="stButton"]>button{{
  height:42px!important;border-radius:12px!important;
  font-size:13px!important;
}}
.sb-toggle div[data-testid="stButton"]>button{{
  background:{CARD2}!important;color:{T2}!important;
  border:1px solid {BORDER}!important;
  box-shadow:none!important;
  height:38px!important;border-radius:10px!important;
  font-size:12px!important;
}}
.sb-toggle div[data-testid="stButton"]>button:hover{{
  background:{PL}!important;color:{ACCENT}!important;
  border-color:{ACCENT}!important;transform:none!important;
}}
.sb-clear div[data-testid="stButton"]>button{{
  background:rgba(224,80,80,0.08)!important;
  color:#E05050!important;
  border:1px solid rgba(224,80,80,0.2)!important;
  box-shadow:none!important;
  height:38px!important;border-radius:10px!important;
  font-size:12px!important;
}}
.sb-clear div[data-testid="stButton"]>button:hover{{
  background:rgba(224,80,80,0.15)!important;
  transform:none!important;
}}

/* ── FOOTER ── */
.footer{{
  border-top:1px solid {BORDER};
  padding:10px 32px;
  display:flex;align-items:center;gap:14px;
  flex-wrap:wrap;
  background:{GLASS};
}}
.f-badge{{
  display:inline-flex;align-items:center;gap:5px;
  background:{CARD2};border:1px solid {BORDER};
  border-radius:8px;padding:3px 10px;
  font-size:10px;color:{T2};font-weight:500;
}}
.f-heart{{font-size:11px;color:{T3};margin-left:auto}}

/* ── SPINNER ── */
.stSpinner>div{{border-top-color:{ACCENT}!important}}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# SIDEBAR COLUMN
# ════════════════════════════════════════════════════
sb_col, main_col = st.columns([27, 100], gap="small")

with sb_col:
    st.markdown(f'<div class="sidebar">', unsafe_allow_html=True)
    st.markdown('<div class="sb-section">Menu</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-new-btn">', unsafe_allow_html=True)
    if st.button("✦  New Search", key="new_search", use_container_width=True):
        st.session_state.result = None
        st.session_state.current_query = ""
        save_memory([])
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    for icon, label in [("🏠","Home"), ("⭐","Favorites"), ("🔖","Bookmarks"), ("ℹ️","About")]:
        st.markdown(f'<div class="sb-item"><span>{icon}</span><span>{label}</span></div>', unsafe_allow_html=True)

    if st.session_state.search_history:
        st.markdown('<div class="sb-section">Recent</div>', unsafe_allow_html=True)
        for q in reversed(st.session_state.search_history[-6:]):
            short = q[:22] + "…" if len(q) > 22 else q
            st.markdown(f'<div class="sb-item"><span>🔍</span><span title="{q}">{short}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-footer">', unsafe_allow_html=True)
    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    mode_lbl = "☀️  Light mode" if dm else "🌙  Dark mode"
    st.markdown('<div class="sb-toggle">', unsafe_allow_html=True)
    if st.button(mode_lbl, key="toggle_mode", use_container_width=True):
        st.session_state.dark_mode = not dm
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.search_history:
        st.markdown('<div class="sb-clear" style="margin-top:6px">', unsafe_allow_html=True)
        if st.button("🗑  Clear history", key="clear_all", use_container_width=True):
            st.session_state.result = None
            st.session_state.current_query = ""
            st.session_state.search_history = []
            save_memory([])
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # sb-footer
    st.markdown('</div>', unsafe_allow_html=True)  # sidebar

# ════════════════════════════════════════════════════
# MAIN COLUMN
# ════════════════════════════════════════════════════
with main_col:
    # Topbar
    st.markdown(f"""
    <div class="topbar">
      <div class="tb-logo">📚<span>Book Search Agent</span></div>
      <div class="tb-sub">Discover books instantly with AI</div>
      <div class="tb-space"></div>
      <div class="tb-pill">🤖 AI Powered</div>
      <div class="avatar">U</div>
    </div>
    """, unsafe_allow_html=True)

    # ── SEARCH BAR (always visible at top) ──────────────────
    st.markdown('<div class="searchbar-wrap"><div class="searchbar-inner">', unsafe_allow_html=True)
    st.markdown('<div class="searchbar-label">📖 Search books</div>', unsafe_allow_html=True)

    q_col, btn_col = st.columns([7, 1], gap="small")
    with q_col:
        query = st.text_input(
            "q",
            value="",
            placeholder="Search any book, author, topic, or genre…",
            label_visibility="collapsed",
            key="search_box"
        )
    with btn_col:
        search_clicked = st.button("Search →", key="search_btn", use_container_width=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── TRIGGER LOGIC — single-execution guard ───────────────
    # Only run agent if button clicked AND query is non-empty
    # and we haven't already run it for this exact query
    if search_clicked and query.strip():
        q_clean = query.strip()
        if q_clean != st.session_state.get("_last_executed", ""):
            st.session_state._last_executed = q_clean
            st.session_state.current_query  = q_clean
            if q_clean not in st.session_state.search_history:
                st.session_state.search_history.append(q_clean)
            with st.spinner("🤖 Searching the library…"):
                try:
                    answer = agent_loop(q_clean)
                    st.session_state.result = {"ok": answer}
                except Exception as e:
                    st.session_state.result = {"err": str(e)}
            st.rerun()

    # ── RESULTS / WELCOME ────────────────────────────────────
    st.markdown('<div class="results-scroll"><div class="results-inner">', unsafe_allow_html=True)

    if st.session_state.result is None:
        # Welcome
        st.markdown(f"""
        <div class="welcome">
          <div class="welcome-icon">📚</div>
          <h1 class="welcome-title">Welcome to Book Search Agent</h1>
          <p class="welcome-sub">Ask me anything about books, authors, publishers, or discover your next favorite read.</p>
          <div class="prompt-grid">
            <div class="prompt-card"><span class="pc-icon">📖</span><div><div class="pc-title">Find Atomic Habits</div><div class="pc-sub">by James Clear</div></div></div>
            <div class="prompt-card"><span class="pc-icon">🧙</span><div><div class="pc-title">Search Harry Potter</div><div class="pc-sub">Complete series</div></div></div>
            <div class="prompt-card"><span class="pc-icon">✍️</span><div><div class="pc-title">Books by James Clear</div><div class="pc-sub">All titles</div></div></div>
            <div class="prompt-card"><span class="pc-icon">🌟</span><div><div class="pc-title">Recommend self-help</div><div class="pc-sub">Top picks</div></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        r = st.session_state.result
        if "err" in r:
            st.markdown(f"""
            <div style="background:rgba(224,80,80,0.06);border:1px solid rgba(224,80,80,0.2);
                        border-left:3px solid #E05050;border-radius:14px;
                        padding:18px 22px;font-size:13px;color:#E07070;">
              ⚠️ &nbsp;{r['err']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Result header
            st.markdown(f"""
            <div class="result-header">
              <div>
                <div class="result-query">"{st.session_state.current_query}"</div>
                <div class="result-sub">AI-generated results · {datetime.now().strftime("%b %d, %Y · %H:%M")}</div>
              </div>
              <div class="result-badge">✦ Results</div>
            </div>
            """, unsafe_allow_html=True)

            # Content wrapper so our CSS applies
            st.markdown('<div class="result-content">', unsafe_allow_html=True)
            st.markdown(r["ok"])
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)  # results-inner, results-scroll

    # Footer
    st.markdown(f"""
    <div class="footer">
      <span class="f-badge">📗 Google Books API</span>
      <span class="f-badge">🤖 OpenRouter AI</span>
    </div>
    """, unsafe_allow_html=True)