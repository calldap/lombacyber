import streamlit as st
import string

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Witcher Cipher",
    page_icon="🐺",
    layout="centered"
)

# ===============================
# CUSTOM CSS (THE WITCHER THEME)
# ===============================
st.markdown("""
<style>
body {
    background-color: #0e0e11;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #e5e7eb;
    font-family: 'Trebuchet MS', serif;
}
.stRadio > label, .stSelectbox label, .stTextInput label {
    font-weight: bold;
    color: #d1d5db;
}
.stButton > button {
    background: linear-gradient(135deg, #1f2933, #111827);
    color: #e5e7eb;
    border: 1px solid #4b5563;
    padding: 0.6rem 1.4rem;
    border-radius: 10px;
    font-weight: bold;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #374151, #1f2937);
    border-color: #9ca3af;
}
hr {
    border: 1px solid #374151;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("""
<h1>🐺 Witcher Cipher</h1>
<p style="color:#9ca3af; margin-top:-10px;">
Arcane Encryption & Decryption based on Witcher Signs and Mutagens
</p>
<hr>
""", unsafe_allow_html=True)

# ===============================
# KONFIGURASI CIPHER
# ===============================
ALPHABET = string.ascii_lowercase

SIGN_SHIFT = {
    "aard": 3,
    "igni": 12,
    "yrden": 5,
    "quen": 8,
    "axii": 10
}

MUTAGENS = [
    "lesser red",
    "red",
    "greater red",
    "lesser blue",
    "green"
]

# ===============================
# FUNGSI CIPHER
# ===============================
def apply_mutagen(shift, mutagen):
    if mutagen == "lesser red":
        return shift + 2
    elif mutagen == "red":
        return shift * 2
    elif mutagen == "greater red":
        return shift * 3
    elif mutagen == "lesser blue":
        return shift + 5
    elif mutagen == "green":
        return (shift + 10) // 2

def shift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) + shift) % 26]

def unshift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) - shift) % 26]

def swap_pairs(text):
    chars = list(text)
    log = []
    for i in range(0, len(chars)-1, 2):
        log.append(f"{chars[i]} ↔ {chars[i+1]}")
        chars[i], chars[i+1] = chars[i+1], chars[i]
    return ''.join(chars), ", ".join(log)

def encrypt(plaintext, sign, mutagen):
    logs = []

    base_shift = SIGN_SHIFT[sign]
    final_shift = apply_mutagen(base_shift, mutagen)

    logs.append(f"🜂 Sign '{sign.upper()}' → Base Shift = {base_shift}")
    logs.append(f"🧪 Mutagen '{mutagen}' → Final Shift = {final_shift}")

    text = plaintext.lower().replace(" ", "")
    logs.append(f"✂ Cleaned Text → {text}")

    shifted = ''.join(shift_char(c, final_shift) for c in text)
    logs.append(f"🜁 Arcane Shift → {shifted}")

    result, swap_log = swap_pairs(shifted)
    logs.append(f"🔁 Rune Swap → {swap_log}")

    return result, logs

def decrypt(ciphertext, sign, mutagen):
    logs = []

    final_shift = apply_mutagen(SIGN_SHIFT[sign], mutagen)
    logs.append(f"🜂 Total Shift = {final_shift}")

    unswapped, swap_log = swap_pairs(ciphertext)
    logs.append(f"🔁 Reverse Swap → {swap_log}")

    plaintext = ''.join(unshift_char(c, final_shift) for c in unswapped)
    logs.append(f"✨ Revealed Text → {plaintext}")

    return plaintext, logs

# ===============================
# UI PANEL (RPG STYLE)
# ===============================
mode = st.radio("⚔ Choose Ritual", ["Enkripsi", "Dekripsi"], horizontal=True)

col1, col2 = st.columns(2)

with col1:
    sign = st.selectbox("🜂 Select Witcher Sign", list(SIGN_SHIFT.keys()))

with col2:
    mutagen = st.selectbox("🧪 Select Mutagen", MUTAGENS)

st.divider()

# ===============================
# ACTION
# ===============================
if mode == "Enkripsi":
    plaintext = st.text_input("📜 Enter Plaintext")

    if st.button("🔐 Cast Encryption Spell"):
        if plaintext:
            result, logs = encrypt(plaintext, sign, mutagen)
            st.success(f"🧾 Ciphertext: **{result}**")

            with st.expander("📖 Arcane Process Log"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("⚠ Plaintext tidak boleh kosong")

else:
    ciphertext = st.text_input("📜 Enter Ciphertext")

    if st.button("🔓 Break the Cipher"):
        if ciphertext:
            result, logs = decrypt(ciphertext, sign, mutagen)
            st.success(f"🧾 Plaintext: **{result}**")

            with st.expander("📖 Arcane Process Log"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("⚠ Ciphertext tidak boleh kosong")

# ===============================
# FOOTER
# ===============================
st.markdown("""
<hr>
<p style="text-align:center; color:#9ca3af;">
🏆 Internal Department Competition • Inspired by The Witcher Universe
</p>
""", unsafe_allow_html=True)
