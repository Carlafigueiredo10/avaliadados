"""
Tema visual "Daylight Control Room" — terminal institucional em luz do dia.

Injetado uma vez no início de main() via st.markdown(STYLES, unsafe_allow_html=True).
Profundidade por elevação e sombra, não por escuridão. Tipografia: Fraunces
(display editorial) + Inter (corpo) + IBM Plex Mono (telemetria e rótulos).
"""

# Rótulo de criticidade exibido no topo de cada card de missão na sidebar.
SEVERITY_LABELS = {
    "permitido": "BAIXO",
    "permitido_com_condicoes": "MODERADO",
    "alto_risco_redesenho": "ALTO",
    "nao_recomendado": "ALTO",
    "risco_excessivo": "EXCESSIVO",
}

# Classe CSS que pinta o ponto de criticidade do card.
SEVERITY_CLASS = {
    "permitido": "crit-low",
    "permitido_com_condicoes": "crit-moderate",
    "alto_risco_redesenho": "crit-high",
    "nao_recomendado": "crit-high",
    "risco_excessivo": "crit-severe",
}


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --bg-base: #EEEFF2;
  --bg-panel: #FFFFFF;
  --bg-panel-subtle: #F6F7F9;
  --bg-sidebar: #F4F5F7;
  --text-primary: #1C2024;
  --text-secondary: #565B61;
  --text-tertiary: #8A8F96;
  --accent-steel: #3A5A7A;
  --accent-steel-bright: #4B7299;
  --accent-steel-soft: rgba(58, 90, 122, 0.07);
  --accent-steel-medium: rgba(58, 90, 122, 0.16);
  --border-subtle: rgba(28, 32, 36, 0.07);
  --border-medium: rgba(28, 32, 36, 0.13);
  --risk-low: #4A7A5A;
  --risk-moderate: #B0852E;
  --risk-high: #C0683C;
  --risk-severe: #B14444;
  --shadow-xs: 0 1px 2px rgba(28,32,36,0.05);
  --shadow-sm: 0 1px 2px rgba(28,32,36,0.04), 0 2px 6px rgba(28,32,36,0.06);
  --shadow-md: 0 2px 4px rgba(28,32,36,0.04), 0 8px 20px rgba(28,32,36,0.08);
  --shadow-lg: 0 4px 8px rgba(28,32,36,0.05), 0 18px 44px rgba(28,32,36,0.11);
  --shadow-hover: 0 4px 10px rgba(28,32,36,0.07), 0 14px 32px rgba(58,90,122,0.13);
  --easing: cubic-bezier(0.4, 0, 0.2, 1);
  --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', 'SF Mono', Menlo, monospace;
}

/* ===== BASE ===== */
.stApp {
  background: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-body);
}

/* atmospheric layer — cool gradient + faint grain */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 45% at 50% 0%, rgba(58,90,122,0.05), transparent 70%),
    linear-gradient(180deg, rgba(255,255,255,0.55) 0%, transparent 28%);
  pointer-events: none;
  z-index: 0;
}
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg viewBox='0 0 240 240' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/></svg>");
  opacity: 0.016;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: multiply;
}
[data-testid="stAppViewContainer"] > .main { position: relative; z-index: 2; }
[data-testid="stHeader"] { background: transparent; }

/* hide streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ===== TYPOGRAPHY ===== */
h1 {
  font-family: var(--font-display) !important;
  font-weight: 500 !important;
  letter-spacing: -0.02em !important;
  font-size: 2.6rem !important;
  line-height: 1.08 !important;
  color: var(--text-primary) !important;
  margin-bottom: 0.35rem !important;
}
h2, h3, h4 {
  font-family: var(--font-display) !important;
  font-weight: 500 !important;
  letter-spacing: -0.012em !important;
  color: var(--text-primary) !important;
}
[data-testid="stCaptionContainer"] {
  color: var(--text-secondary) !important;
  font-family: var(--font-body) !important;
  font-weight: 300 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.005em !important;
}
/* version line — the one with bold marker — rendered as telemetry */
[data-testid="stCaptionContainer"]:has(strong) {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: var(--accent-steel) !important;
  margin-top: 0.6rem !important;
  padding-top: 0.55rem !important;
  border-top: 1px solid var(--border-subtle) !important;
  display: inline-block !important;
}
[data-testid="stCaptionContainer"]:has(strong) strong {
  color: var(--accent-steel) !important;
  font-weight: 500 !important;
}

/* ===== MAIN CONTAINER ===== */
.main .block-container {
  padding-top: 3rem !important;
  padding-bottom: 4rem !important;
  max-width: 1080px !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
  background: var(--bg-sidebar) !important;
  border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.75rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.5rem; }

/* terminal header */
.terminal-header {
  padding: 0 0.25rem 1.1rem 0.25rem;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 0.5rem;
}
.th-title {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.15em;
  color: var(--text-primary);
}
.th-sub {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.13em;
  color: var(--text-tertiary);
  margin-top: 0.3rem;
}

/* section label */
.section-label {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin: 1.1rem 0.25rem 0.3rem 0.25rem;
}
.section-caption {
  font-family: var(--font-body);
  font-size: 0.72rem;
  font-weight: 300;
  color: var(--text-secondary);
  margin: 0 0.25rem 0.5rem 0.25rem;
  line-height: 1.4;
}

/* selectbox (ambiente) */
[data-testid="stSidebar"] [data-testid="stSelectbox"] label {
  font-family: var(--font-mono) !important;
  font-size: 0.62rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.13em !important;
  text-transform: uppercase !important;
  color: var(--text-tertiary) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: 3px !important;
  box-shadow: var(--shadow-xs) !important;
  font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  color: var(--text-primary) !important;
}

/* mission card — label row above each case button */
.case-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 0.7rem 0.3rem 0 0.3rem;
}
.case-id { color: var(--text-tertiary); }
.case-crit { display: flex; align-items: center; gap: 0.35rem; font-weight: 500; }
.crit-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 5px currentColor;
}
.crit-low { color: var(--risk-low); }
.crit-moderate { color: var(--risk-moderate); }
.crit-high { color: var(--risk-high); }
.crit-severe { color: var(--risk-severe); }

/* mission card body — the button */
[data-testid="stSidebar"] .stButton button {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 4px !important;
  box-shadow: var(--shadow-sm) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-weight: 400 !important;
  font-size: 0.86rem !important;
  line-height: 1.4 !important;
  text-align: left !important;
  padding: 0.7rem 0.85rem !important;
  height: auto !important;
  min-height: auto !important;
  white-space: normal !important;
  transition: transform 320ms var(--easing), box-shadow 320ms var(--easing), border-color 320ms var(--easing) !important;
}
[data-testid="stSidebar"] .stButton button:hover {
  border-color: var(--accent-steel-medium) !important;
  box-shadow: var(--shadow-hover) !important;
  transform: translateY(-1px) !important;
  color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stButton button:active {
  transform: translateY(0) !important;
  box-shadow: var(--shadow-sm) !important;
}
[data-testid="stSidebar"] .stButton button:focus:not(:active) {
  border-color: var(--accent-steel) !important;
  box-shadow: var(--shadow-sm), 0 0 0 3px var(--accent-steel-soft) !important;
}

/* sidebar divider + meta */
[data-testid="stSidebar"] hr {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 1.25rem 0 0.9rem 0;
}
.sidebar-meta {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  letter-spacing: 0.06em;
  padding: 0 0.3rem;
}
.sidebar-meta .meta-row {
  display: flex;
  justify-content: space-between;
  padding: 0.22rem 0;
  border-bottom: 1px solid var(--border-subtle);
}
.sidebar-meta .meta-row:last-child { border-bottom: none; }
.sidebar-meta .meta-row span:first-child { color: var(--text-tertiary); }
.sidebar-meta .meta-row span:last-child { color: var(--text-secondary); }

/* ===== CHAT INPUT ===== */
[data-testid="stChatInput"] {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-medium) !important;
  border-radius: 4px !important;
  box-shadow: var(--shadow-md) !important;
}
[data-testid="stChatInput"] textarea {
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-weight: 300 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: var(--text-tertiary) !important;
}
[data-testid="stChatInput"] button {
  color: var(--accent-steel) !important;
}

/* ===== CHAT MESSAGES ===== */
[data-testid="stChatMessage"] {
  animation: riseIn 520ms var(--easing);
  margin: 0.85rem 0 !important;
}
/* assistant — regulatory panel */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 5px !important;
  box-shadow: var(--shadow-md) !important;
  padding: 1.6rem 1.9rem !important;
}
/* user — minimal annotation */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: transparent !important;
  border: none !important;
  border-left: 2px solid var(--accent-steel-medium) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0.3rem 0 0.3rem 1.25rem !important;
}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
  background: var(--bg-panel-subtle) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--accent-steel) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
  font-weight: 300 !important;
  line-height: 1.72 !important;
  font-size: 0.95rem !important;
}
[data-testid="stChatMessage"] strong {
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
  font-family: var(--font-display) !important;
  font-weight: 500 !important;
  letter-spacing: -0.01em !important;
  margin-top: 1.4rem !important;
  margin-bottom: 0.6rem !important;
  font-size: 1.15rem !important;
}
[data-testid="stChatMessage"] code {
  font-family: var(--font-mono) !important;
  background: var(--bg-panel-subtle) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 2px !important;
  font-size: 0.82rem !important;
  color: var(--accent-steel) !important;
}

@keyframes riseIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== EXPANDER — telemetry panel (rastro decisório) ===== */
[data-testid="stExpander"] {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 4px !important;
  box-shadow: var(--shadow-sm) !important;
  margin-top: 1.4rem !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.11em !important;
  text-transform: uppercase !important;
  color: var(--accent-steel) !important;
  padding: 0.95rem 1.2rem !important;
}
[data-testid="stExpander"] summary:hover { color: var(--accent-steel-bright) !important; }
[data-testid="stExpanderDetails"] {
  background: var(--bg-panel-subtle) !important;
  border-top: 1px solid var(--border-subtle) !important;
  padding: 1.2rem 1.3rem !important;
}
[data-testid="stExpanderDetails"] p,
[data-testid="stExpanderDetails"] li {
  font-family: var(--font-mono) !important;
  font-size: 0.76rem !important;
  line-height: 1.75 !important;
  color: var(--text-secondary) !important;
}
[data-testid="stExpanderDetails"] strong { color: var(--text-primary) !important; font-weight: 500 !important; }
[data-testid="stExpanderDetails"] h1,
[data-testid="stExpanderDetails"] h2,
[data-testid="stExpanderDetails"] h3,
[data-testid="stExpanderDetails"] h4 {
  font-family: var(--font-mono) !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
}

/* ===== DOWNLOAD BUTTON ===== */
[data-testid="stDownloadButton"] button {
  background: transparent !important;
  border: 1px solid var(--border-medium) !important;
  color: var(--text-secondary) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.66rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 0.5rem 1rem !important;
  border-radius: 3px !important;
  box-shadow: none !important;
  transition: all 240ms var(--easing) !important;
}
[data-testid="stDownloadButton"] button:hover {
  border-color: var(--accent-steel) !important;
  color: var(--accent-steel) !important;
  background: var(--accent-steel-soft) !important;
}

/* ===== METRICS ===== */
[data-testid="stMetric"] {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 3px !important;
  box-shadow: var(--shadow-xs) !important;
  padding: 0.7rem 0.95rem !important;
}
[data-testid="stMetricLabel"] {
  font-family: var(--font-mono) !important;
  font-size: 0.6rem !important;
  letter-spacing: 0.09em !important;
  text-transform: uppercase !important;
  color: var(--text-tertiary) !important;
}
[data-testid="stMetricValue"] {
  font-family: var(--font-mono) !important;
  color: var(--accent-steel) !important;
  font-weight: 500 !important;
  font-size: 1.4rem !important;
}

/* ===== STATUS WIDGET (running indicator) ===== */
[data-testid="stStatusWidget"] {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 3px !important;
  box-shadow: var(--shadow-sm) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.06em !important;
  color: var(--accent-steel) !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--border-medium);
  border-radius: 5px;
  border: 2px solid var(--bg-base);
}
::-webkit-scrollbar-thumb:hover { background: var(--text-tertiary); }

/* ===== SELECTION ===== */
::selection { background: var(--accent-steel-medium); color: var(--text-primary); }
</style>
"""
