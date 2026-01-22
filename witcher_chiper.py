import streamlit as st
import string

# ===============================
# KONFIGURASI DASAR
# ===============================
ALPHABET = string.ascii_lowercase

SIGN_SHIFT = {
    "aard": 3,
    "igni": 12,
    "yrden": 5,
    "quen": 8,
    "axii": 10
}

# ===============================
# FUNGSI KRIPTOGRAFI
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
    else:
        raise ValueError("Mutagen tidak dikenal")

def shift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) + shift) % 26]

def unshift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) - shift) % 26]

def swap_pairs(text):
    chars = list(text)
    log = []
    for i in range(0, len(chars)-1, 2):
        log.append(f"({chars[i]} <-> {chars[i+1]})")
        chars[i], chars[i+1] = chars[i+1], chars[i]
    return ''.join(chars), ", ".join(log)

def encrypt(plaintext, sign, mutagen):
    logs = []

    base_shift = SIGN_SHIFT[sign]
    logs.append(f"Base shift ({sign}) = {base_shift}")

    final_shift = apply_mutagen(base_shift, mutagen)
    logs.append(f"Mutagen '{mutagen}' → Shift akhir = {final_shift}")

    text = plaintext.lower().replace(" ", "")
    logs.append(f"Cleaning text → {text}")

    shifted = ""
    for c in text:
        shifted += shift_char(c, final_shift)

    logs.append(f"Hasil shifting → {shifted}")

    result, swap_log = swap_pairs(shifted)
    logs.append(f"Swap pasangan → {swap_log}")
    logs.append(f"Ciphertext akhir → {result}")

    return result, logs

def decrypt(ciphertext, sign, mutagen):
    logs = []

    base_shift = SIGN_SHIFT[sign]
    final_shift = apply_mutagen(base_shift, mutagen)
    logs.append(f"Total shift = {final_shift}")

    unswapped, swap_log = swap_pairs(ciphertext)
    logs.append(f"Un-swap → {swap_log}")
    logs.append(f"Hasil un-swap → {unswapped}")

    plaintext = ""
    for c in unswapped:
        plaintext += unshift_char(c, final_shift)

    logs.append(f"Plaintext akhir → {plaintext}")

    return plaintext, logs

# ===============================
# STREAMLIT UI
# ===============================
st.set_page_config(page_title="Witcher Cipher", page_icon="🐺")

st.title("🐺 Witcher Cipher")
st.caption("Enkripsi & Dekripsi berbasis Sign dan Mutagen")

mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

sign = st.selectbox("Pilih Sign", list(SIGN_SHIFT.keys()))
mutagen = st.selectbox(
    "Pilih Mutagen",
    ["lesser red", "red", "greater red", "lesser blue", "green"]
)

st.divider()

if mode == "Enkripsi":
    plaintext = st.text_input("Masukkan Plaintext")

    if st.button("🔐 Enkripsi"):
        if plaintext:
            result, logs = encrypt(plaintext, sign, mutagen)
            st.success(f"Ciphertext: **{result}**")

            with st.expander("📜 Lihat Proses (Debug)"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("Plaintext tidak boleh kosong")

else:
    ciphertext = st.text_input("Masukkan Ciphertext")

    if st.button("🔓 Dekripsi"):
        if ciphertext:
            result, logs = decrypt(ciphertext, sign, mutagen)
            st.success(f"Plaintext: **{result}**")

            with st.expander("📜 Lihat Proses (Debug)"):
                for log in logs:
                    st.write(log)
        else:
            st.warning("Ciphertext tidak boleh kosong")

st.divider()
st.caption("Dibuat dengan Streamlit & Python 🐍")
