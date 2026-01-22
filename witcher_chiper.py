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

# Custom CSS dengan ANIMASI
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400&display=swap');

        /* --- 1. Background & Font --- */
        .stApp {
            background-color: #121212;
            background-image: linear-gradient(315deg, #0b0b0b 0%, #1f1f1f 74%);
            color: #dcdcdc;
            font-family: 'Lato', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #c93838;
            text-shadow: 2px 2px 4px #000000;
        }

        /* --- 2. ANIMASI KEYFRAMES --- */
        
        /* Animasi Berdenyut (Breathing) untuk Serigala */
        @keyframes pulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(201, 56, 56, 0.0)); }
            50% { transform: scale(1.1); filter: drop-shadow(0 0 15px rgba(201, 56, 56, 0.6)); }
            100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(201, 56, 56, 0.0)); }
        }

        /* Animasi Muncul dari Bawah (Fade In Up) untuk Hasil */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 20px, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }

        /* --- 3. Applying Animations --- */
        
        /* Terapkan ke Emoji Serigala */
        .wolf-anim {
            font-size: 80px;
            text-align: center;
            animation: pulse 3s infinite ease-in-out;
            cursor: pointer;
        }

        /* Terapkan ke Box Hasil */
        .result-box {
            animation: fadeInUp 0.8s ease-out;
            border: 1px solid #c93838;
            padding: 10px;
            border-radius: 5px;
            background-color: #1a0505;
        }

        /* --- 4. UI Components Styling --- */
        .quote {
            font-family: 'Cinzel', serif;
            color: #d4af37;
            font-style: italic;
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
            transform: scale(1.02);
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
    # MENERAPKAN KELAS ANIMASI 'wolf-anim' PADA EMOJI
    st.markdown('<div class="wolf-anim">🐺</div>', unsafe_allow_html=True)

with col2:
    st.title("The Wolf Cipher")
    st.markdown('<div class="quote">"Medallion\'s humming... magic is near."</div>', unsafe_allow_html=True)

st.write("---")

with st.sidebar:
    st.header("Bestiary & Lore ⚔️")
    st.info("""
    **Signs (Base Force)**
    \nKekuatan dasar sihir Witcher yang menggeser alfabet.
    
    **Mutagens (Modifier)**
    \nRamuan kimiawi yang melipatgandakan atau menambah kekuatan Sign.
    """)
    st.warning("⚠️ Hanya huruf a-z yang diproses. Spasi diabaikan.")
    
tab_encrypt, tab_decrypt = st.tabs(["🔒 CAST SPELL (Encrypt)", "🔓 DISPEL MAGIC (Decrypt)"])

# ===============================
# TAB ENKRIPSI
# ===============================
with tab_encrypt:
    st.subheader("Inscribe Runes")
    
    c1, c2 = st.columns(2)
    with c1:
        sign_in = st.selectbox("Select Witcher Sign", list(SIGN_SHIFT.keys()), key="sign_e")
    with c2:
        mut_in = st.selectbox("Select Mutagen", ["lesser red", "red", "greater red", "lesser blue", "green"], key="mut_e")
        
    plaintext = st.text_area("Enter Message to Hide", height=100, placeholder="Type your secret here...")

    if st.button("🔮 CAST CIPHER"):
        if plaintext:
            # EFEK PARTIKEL SALJU (MAGIC DUST)
            st.snow() 
            
            with st.spinner("Weaving the magic..."):
                time.sleep(1.2) # Sedikit delay untuk menikmati animasi loading
                res, logs = process_cipher(plaintext, sign_in, mut_in, "encrypt")
            
            # MEMBUNGKUS HASIL DALAM DIV YANG DIANIMASIKAN
            st.markdown(f"""
            <div class="result-box">
                <h4 style="color:#d4af37; margin-top:0;">✨ Sealed Message:</h4>
                <code style="background:transparent; color:#e0e0e0; font-size:1.1em;">{res}</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Spell cast successfully.")
            
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
                time.sleep(1.0)
                res, logs = process_cipher(ciphertext, sign_de, mut_de, "decrypt")
            
            # MEMBUNGKUS HASIL DALAM DIV YANG DIANIMASIKAN
            st.markdown(f"""
            <div class="result-box">
                <h4 style="color:#d4af37; margin-top:0;">🔓 Revealed Message:</h4>
                <code style="background:transparent; color:#e0e0e0; font-size:1.1em;">{res}</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Curse Lifted!")
            
            with st.expander("Show Investigation Notes (Debug Log)"):
                for log in logs:
                    st.markdown(log)
        else:
            st.error("No runes detected to decipher.")

# Footer
st.write("---")
st.markdown("<div style='text-align: center; color: #555;'>Created for the School of the Wolf 🐺 | Python & Streamlit</div>", unsafe_allow_html=True)
