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
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk Tema The Witcher (Tanpa Gambar)
st.markdown("""
    <style>
        /* Import Font Cinzel untuk nuansa Medieval */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400&display=swap');

        /* Background Gelap Total */
        .stApp {
            background-color: #0e0e0e;
            color: #dcdcdc;
            font-family: 'Lato', sans-serif;
        }

        /* Judul & Header dengan Font Cinzel */
        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #c93838; /* Merah Darah/Witcher */
            text-shadow: 0px 0px 10px rgba(201, 56, 56, 0.5);
            text-align: center;
        }
        
        /* Subtitle Styling */
        .subtitle {
            font-family: 'Cinzel', serif;
            color: #8c8c8c;
            text-align: center;
            margin-top: -15px;
            margin-bottom: 30px;
            font-size: 1.2rem;
        }

        /* Input Fields Styling */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #1a1a1a;
            color: #e0e0e0;
            border: 1px solid #444;
            font-family: 'Courier New', monospace;
        }
        .stSelectbox > div > div > div {
             background-color: #1a1a1a;
             color: #e0e0e0;
        }

        /* Tombol Utama - Merah Gelap */
        .stButton > button {
            background-color: #380c0c;
            color: #e0e0e0;
            border: 1px solid #c93838;
            font-family: 'Cinzel', serif;
            font-weight: bold;
            width: 100%;
            transition: 0.3s;
            text-transform: uppercase;
        }
        .stButton > button:hover {
            background-color: #c93838;
            color: #ffffff;
            border-color: #ff5555;
            box-shadow: 0 0 15px #c93838;
        }

        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1a1a1a;
            border-radius: 4px;
            color: #888;
            border: 1px solid #333;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #2d2d2d;
            color: #c93838;
            border-color: #c93838;
        }

        /* Code Block Result */
        code {
            color: #d4af37; /* Warna Emas */
            background-color: #111;
            font-weight: bold;
        }
        
        /* Divider Custom */
        hr {
            border-color: #333;
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
    
    logs.append(f"🌀 **Sign:** {sign.capitalize()} (Base: {base_shift})")
    logs.append(f"🧪 **Mutagen:** {mutagen} (Final Shift: {final_shift})")

    clean_text = text.lower().replace(" ", "") if mode == "encrypt" else text
    
    if mode == "encrypt":
        logs.append(f"📜 **Raw:** `{clean_text}`")
        shifted = "".join([shift_char(c, final_shift) for c in clean_text])
        logs.append(f"✨ **Shifted:** `{shifted}`")
        result, swap_log = swap_pairs(shifted)
        logs.append(f"⚔️ **Swapped:**\n{swap_log}")
    else:
        unswapped, swap_log = swap_pairs(clean_text)
        logs.append(f"⚔️ **Un-swapped:** `{unswapped}`")
        result = "".join([unshift_char(c, final_shift) for c in unswapped])
        
    return result, logs

# ===============================
# UI UTAMA
# ===============================

# Header Title dengan Emoji Besar
st.markdown("<h1>🐺 THE WITCHER CIPHER ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>School of the Wolf Cryptography</div>", unsafe_allow_html=True)

# Layout Tabs
tab_encrypt, tab_decrypt = st.tabs(["🔒 ENCRYPT (MANTRA)", "🔓 DECRYPT (DISPEL)"])

# --- TAB ENKRIPSI ---
with tab_encrypt:
    st.markdown("### 📝 Inscribe Runes")
    
    col1, col2 = st.columns(2)
    with col1:
        sign_e = st.selectbox("Select Sign (Base Force)", list(SIGN_SHIFT.keys()), key="s_e")
    with col2:
        mut_e = st.selectbox("Select Mutagen (Modifier)", ["lesser red", "red", "greater red", "lesser blue", "green"], key="m_e")
        
    plaintext = st.text_area("Plaintext Message", height=100, placeholder="write your secret here...")

    if st.button("🔥 Cast Encryption Spell"):
        if plaintext:
            with st.spinner("Channeling Chaos..."):
                time.sleep(0.8)
                res, logs = process_cipher(plaintext, sign_e, mut_e, "encrypt")
            
            st.success("Message Sealed!")
            st.markdown("#### 📜 Ciphertext Result")
            st.code(res, language=None)
            
            with st.expander("👁️ View Spell Trace"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("Needs text to cast spell.")

# --- TAB DEKRIPSI ---
with tab_decrypt:
    st.markdown("### 🧩 Analyze Runes")
    
    col1, col2 = st.columns(2)
    with col1:
        sign_d = st.selectbox("Select Sign", list(SIGN_SHIFT.keys()), key="s_d")
    with col2:
        mut_d = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="m_d")
        
    ciphertext = st.text_input("Ciphertext String")

    if st.button("🗡️ Break Curse (Decrypt)"):
        if ciphertext:
            with st.spinner("Deciphering Runes..."):
                time.sleep(0.8)
                res, logs = process_cipher(ciphertext, sign_d, mut_d, "decrypt")
            
            st.success("Message Revealed!")
            st.markdown("#### 📜 Plaintext Result")
            st.code(res, language=None)
            
            with st.expander("👁️ View Investigation"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("Needs runes to decrypt.")

# Footer Minimalis
st.write("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
    "⚔️ White Wolf Tools | Python Streamlit 🐍"
    "</div>", 
    unsafe_allow_html=True
)
