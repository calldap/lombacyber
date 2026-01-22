import streamlit as st
import string
import time

# ===============================
# KONFIGURASI HALAMAN & CSS
# ===============================
st.set_page_config(
    page_title="Witcher Cipher",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS dengan ANIMASI & KABUT
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400&display=swap');

        /* --- 1. Background & Font --- */
        .stApp {
            background-color: #0e0e0e;
            background-image: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
            color: #dcdcdc;
            font-family: 'Lato', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #c93838;
            text-shadow: 2px 2px 4px #000000;
        }

        /* --- 2. ANIMASI KEYFRAMES --- */
        
        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(201, 56, 56, 0.0)); }
            50% { transform: scale(1.1); filter: drop-shadow(0 0 15px rgba(201, 56, 56, 0.6)); }
            100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(201, 56, 56, 0.0)); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 20px, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }

        /* Animasi Kabut Bergerak */
        @keyframes fogFlow {
            0% { background-position: 0% 50%; opacity: 0; }
            20% { opacity: 0.8; }
            80% { opacity: 0.8; }
            100% { background-position: 100% 50%; opacity: 0; }
        }

        /* --- 3. CLASS UNTUK EFEK KABUT (MIASMA) --- */
        .miasma-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 9999;
            background: linear-gradient(
                120deg, 
                rgba(20, 40, 20, 0.0) 0%, 
                rgba(50, 80, 50, 0.4) 30%, 
                rgba(100, 100, 100, 0.2) 50%, 
                rgba(50, 80, 50, 0.4) 70%, 
                rgba(20, 40, 20, 0.0) 100%
            );
            background-size: 200% 200%;
            animation: fogFlow 2.5s ease-in-out forwards;
        }

        /* --- 4. UI Components Styling --- */
        .wolf-anim {
            font-size: 80px;
            text-align: center;
            animation: pulse 3s infinite ease-in-out;
            cursor: pointer;
        }

        .result-box {
            animation: fadeInUp 0.8s ease-out;
            border: 1px solid #c93838;
            padding: 15px;
            border-radius: 5px;
            background-color: #1a0505;
            margin-top: 20px;
        }

        .quote {
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-style: italic;
            font-size: 1.1em;
        }

        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #555;
            font-family: 'Courier New', monospace;
        }
        
        .stSelectbox > div > div > div {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }

        .stButton > button {
            background-color: #380c0c;
            color: #e0e0e0;
            border: 1px solid #c93838;
            font-family: 'Cinzel', serif;
            width: 100%;
            transition: 0.3s;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .stButton > button:hover {
            background-color: #c93838;
            color: #ffffff;
            box-shadow: 0 0 20px #c93838;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# LOGIKA KRIPTOGRAFI
# ===============================
ALPHABET = string.ascii_lowercase

SIGN_SHIFT = {
    "aard": 3,
    "igni": 12,
    "yrden": 5,
    "quen": 8,
    "axii": 10
}

def apply_mutagen(shift, mutagen):
    if mutagen == "lesser red": return shift + 2
    elif mutagen == "red": return shift * 2
    elif mutagen == "greater red": return shift * 3
    elif mutagen == "lesser blue": return shift + 5
    elif mutagen == "green": return (shift + 10) // 2
    else: return shift

def shift_char(c, shift):
    if c not in ALPHABET: return c
    return ALPHABET[(ALPHABET.index(c) + shift) % 26]

def unshift_char(c, shift):
    if c not in ALPHABET: return c
    return ALPHABET[(ALPHABET.index(c) - shift) % 26]

def swap_pairs(text):
    chars = list(text)
    log = []
    for i in range(0, len(chars)-1, 2):
        if chars[i] in ALPHABET and chars[i+1] in ALPHABET:
            log.append(f"[{chars[i]} ⇄ {chars[i+1]}]")
            chars[i], chars[i+1] = chars[i+1], chars[i]
    return ''.join(chars), "  ".join(log)

def process_cipher(text, sign, mutagen, mode="encrypt"):
    logs = []
    base_shift = SIGN_SHIFT[sign]
    final_shift = apply_mutagen(base_shift, mutagen)
    
    logs.append(f"🛡️ **Sign Used:** {sign.capitalize()} (Base: {base_shift})")
    logs.append(f"🧪 **Mutagen:** {mutagen} (Final Shift: {final_shift})")

    clean_text = text.lower().replace(" ", "") if mode == "encrypt" else text
    
    if mode == "encrypt":
        logs.append(f"📜 **Raw Input:** `{clean_text}`")
        shifted = "".join([shift_char(c, final_shift) for c in clean_text])
        logs.append(f"✨ **Shifted:** `{shifted}`")
        result, swap_log = swap_pairs(shifted)
        logs.append(f"⚔️ **Swapped Pairs:**\n{swap_log}")
    else:
        unswapped, swap_log = swap_pairs(clean_text)
        logs.append(f"⚔️ **Un-swapped:** `{unswapped}`")
        result = "".join([unshift_char(c, final_shift) for c in unswapped])
        
    return result, logs

# ===============================
# UI COMPONENTS
# ===============================

col1, col2 = st.columns([1, 4])
with col1:
    st.markdown('<div class="wolf-anim">🐺</div>', unsafe_allow_html=True)
with col2:
    # --- JUDUL & QUOTE YANG DIMINTA ---
    st.title("Witcher Cipher")
    st.markdown('<div class="quote">"Medallion\'s humming... a hidden message, it\'s gotta be."</div>', unsafe_allow_html=True)

st.write("---")

with st.sidebar:
    st.header("Bestiary & Lore ⚔️")
    st.info("Kombinasikan **Sign** dan **Mutagen** untuk menyandikan pesan rahasia.")
    st.markdown("---")
    st.caption("School of the Wolf © 1272")

tab_encrypt, tab_decrypt = st.tabs(["🔒 CAST SPELL", "🔓 DISPEL MAGIC"])

# Placeholder untuk efek kabut
fog_placeholder = st.empty()

# ===============================
# TAB ENKRIPSI
# ===============================
with tab_encrypt:
    st.subheader("Inscribe Runes")
    
    c1, c2 = st.columns(2)
    with c1:
        sign_in = st.selectbox("Select Sign", list(SIGN_SHIFT.keys()), key="s_e")
    with c2:
        mut_in = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="m_e")
        
    plaintext = st.text_area("Plaintext Message", height=100, placeholder="Secret message...")

    if st.button("🔮 CAST CIPHER"):
        if plaintext:
            # 1. TRIGGER EFEK KABUT (MIASMA)
            fog_placeholder.markdown('<div class="miasma-overlay"></div>', unsafe_allow_html=True)
            
            # 2. PROSES
            with st.spinner("Channeling Chaos..."):
                time.sleep(2.0) # Waktu untuk melihat animasi kabut
                res, logs = process_cipher(plaintext, sign_in, mut_in, "encrypt")
            
            # 3. BERSIHKAN KABUT
            fog_placeholder.empty()

            # 4. TAMPILKAN HASIL
            st.markdown(f"""
            <div class="result-box">
                <h4 style="color:#d4af37; margin-top:0;">✨ Sealed Message:</h4>
                <code style="background:transparent; color:#e0e0e0; font-size:1.1em;">{res}</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Message sealed in the mists.")
            
            with st.expander("Show Spell Trace"):
                for log in logs:
                    st.markdown(log)
        else:
            st.warning("Cannot cast on emptiness.")

# ===============================
# TAB DEKRIPSI
# ===============================
with tab_decrypt:
    st.subheader("Analyze Runes")
    
    c1, c2 = st.columns(2)
    with c1:
        sign_de = st.selectbox("Select Sign", list(SIGN_SHIFT.keys()), key="s_d")
    with c2:
        mut_de = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="m_d")
        
    ciphertext = st.text_input("Ciphertext String")

    if st.button("🗡️ BREAK CURSE"):
        if ciphertext:
            # 1. TRIGGER EFEK KABUT
            fog_placeholder.markdown('<div class="miasma-overlay"></div>', unsafe_allow_html=True)
            
            with st.spinner("Examining traces..."):
                time.sleep(2.0)
                res, logs = process_cipher(ciphertext, sign_de, mut_de, "decrypt")
            
            fog_placeholder.empty()

            st.markdown(f"""
            <div class="result-box">
                <h4 style="color:#d4af37; margin-top:0;">🔓 Revealed Message:</h4>
                <code style="background:transparent; color:#e0e0e0; font-size:1.1em;">{res}</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Curse Lifted.")
            
            with st.expander("Show Investigation"):
                for log in logs:
                    st.markdown(log)
        else:
            st.warning("No runes detected.")

st.write("---")
st.markdown("<div style='text-align: center; color: #555;'>Created for the School of the Wolf 🐺</div>", unsafe_allow_html=True)
