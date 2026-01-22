import streamlit as st
import string
import time

# ===============================
# KONFIGURASI HALAMAN & CSS
# ===============================
st.set_page_config(
    page_title="Wolf School Cipher",
    page_icon="🐺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Tema The Witcher
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400&display=swap');

        /* Background Gelap Textur */
        .stApp {
            background-color: #121212;
            background-image: linear-gradient(315deg, #121212 0%, #2d2d2d 74%);
            color: #dcdcdc;
            font-family: 'Lato', sans-serif;
        }

        /* Judul Utama */
        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #c93838; /* Warna Merah Witcher */
            text-shadow: 2px 2px 4px #000000;
        }
        
        /* Highlight text */
        .highlight {
            color: #d4af37;
            font-weight: bold;
        }

        /* Custom Input Fields */
        .stTextInput > div > div > input {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #555;
            font-family: 'Courier New', monospace;
        }

        /* Custom Buttons */
        .stButton > button {
            background-color: #380c0c;
            color: #e0e0e0;
            border: 1px solid #c93838;
            font-family: 'Cinzel', serif;
            width: 100%;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #c93838;
            color: #ffffff;
            border-color: #ff5555;
            box-shadow: 0 0 10px #c93838;
        }

        /* Expander Styling (Quest Log) */
        .streamlit-expanderHeader {
            background-color: #1e1e1e;
            color: #d4af37; /* Gold */
            font-family: 'Cinzel', serif;
        }
        
        /* Success/Info Message Customization */
        .stSuccess {
            background-color: #1e1e1e;
            border-left: 5px solid #4caf50;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# LOGIKA KRIPTOGRAFI (CORE)
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
    if c not in ALPHABET: return c # Handle non-alphabet
    return ALPHABET[(ALPHABET.index(c) + shift) % 26]

def unshift_char(c, shift):
    if c not in ALPHABET: return c
    return ALPHABET[(ALPHABET.index(c) - shift) % 26]

def swap_pairs(text):
    chars = list(text)
    log = []
    for i in range(0, len(chars)-1, 2):
        if chars[i] in ALPHABET and chars[i+1] in ALPHABET: # Only swap letters
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

# Header dengan Nuansa RPG
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/87/The_Witcher_3_Wild_Hunt_Music_Cover_Art.jpg/220px-The_Witcher_3_Wild_Hunt_Music_Cover_Art.jpg", caption="School of the Wolf")
with col2:
    st.title("The Wolf Cipher")
    st.markdown("*\"Medallion's humming... a hidden message, it's gotta be.\"*")

st.write("---")

# Sidebar untuk Lore/Info
with st.sidebar:
    st.header("Bestiary & Lore")
    st.info("""
    **Signs** mempengaruhi pergeseran dasar huruf (Shift).
    \n**Mutagens** memodifikasi kekuatan Sign (Multiplier/Adder).
    \n**Mekanisme:** 1. Shift Huruf
    2. Tukar Pasangan (Swap)
    """)
    st.warning("Hanya huruf a-z yang akan diproses. Spasi dihapus saat enkripsi.")

# Layout Tab yang lebih bersih
tab_encrypt, tab_decrypt = st.tabs(["🔒 CAST SPELL (Encrypt)", "🔓 DISPEL MAGIC (Decrypt)"])

# ===============================
# TAB ENKRIPSI
# ===============================
with tab_encrypt:
    st.subheader("Inscribe Runes")
    
    # Input menggunakan kolom agar tidak memanjang ke bawah
    c1, c2 = st.columns(2)
    with c1:
        sign_in = st.selectbox("Select Witcher Sign", list(SIGN_SHIFT.keys()), key="sign_e")
    with c2:
        mut_in = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="mut_e")
        
    plaintext = st.text_area("Enter Message to Hide", height=100, placeholder="Type your secret here...")

    if st.button("🔮 CAST CIPHER"):
        if plaintext:
            with st.spinner("Channeling Chaos..."):
                time.sleep(0.8) # Efek dramatis
                res, logs = process_cipher(plaintext, sign_in, mut_in, "encrypt")
            
            st.success("Message Sealed Successfully!")
            st.markdown("### 📜 Sealed Scroll (Result)")
            # Menggunakan st.code agar user mudah meng-copy hasil
            st.code(res, language=None)
            
            with st.expander("Show Spell Trace (Debug Log)"):
                for log in logs:
                    st.markdown(log)
        else:
            st.error("You cannot cast a spell on nothingness.")

# ===============================
# TAB DEKRIPSI
# ===============================
with tab_decrypt:
    st.subheader("Analyze Runes")
    
    c1, c2 = st.columns(2)
    with c1:
        sign_de = st.selectbox("Select Witcher Sign", list(SIGN_SHIFT.keys()), key="sign_d")
    with c2:
        mut_de = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="mut_d")
        
    ciphertext = st.text_input("Enter Encrypted Runes")

    if st.button("🗡️ BREAK CURSE"):
        if ciphertext:
            with st.spinner("Examining traces..."):
                time.sleep(0.8)
                res, logs = process_cipher(ciphertext, sign_de, mut_de, "decrypt")
            
            st.success("Curse Lifted! Message Revealed.")
            st.markdown("### 📜 Revealed Message")
            st.code(res, language=None)
            
            with st.expander("Show Investigation Notes (Debug Log)"):
                for log in logs:
                    st.markdown(log)
        else:
            st.error("No runes detected to decipher.")

# Footer
st.write("---")
st.markdown("<div style='text-align: center; color: #555;'>Created for the School of the Wolf 🐺 | Python & Streamlit</div>", unsafe_allow_html=True)
