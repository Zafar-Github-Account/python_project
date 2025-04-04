import streamlit as st
import string
import math
import time
import requests
import hashlib

# Common passwords
common_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123', '111111', 'iloveyou']

# Hash-based Pwned Passwords check
def is_password_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url)
        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
    except Exception as e:
        print("API error:", e)
    return 0

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in string.punctuation for c in password): charset += len(string.punctuation)
    return len(password) * math.log2(charset) if charset > 0 else 0

def estimate_crack_time(entropy):
    guesses = 2 ** entropy
    guesses_per_second = 1e9
    seconds = guesses / guesses_per_second
    return seconds

def human_time(seconds):
    units = [("centuries", 60*60*24*365*100), ("years", 60*60*24*365),
             ("months", 60*60*24*30), ("days", 60*60*24),
             ("hours", 3600), ("minutes", 60), ("seconds", 1)]
    for name, unit_seconds in units:
        if seconds >= unit_seconds:
            return f"{seconds // unit_seconds:.0f} {name}"
    return "less than 1 second"

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("❌ Too short — use at least 12 characters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("❌ Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("❌ Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("❌ Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("❌ Add special characters.")

    if password.lower() in common_passwords:
        feedback.append("❌ This is a common password — extremely risky!")
        score = 0

    entropy = calculate_entropy(password)
    crack_time = human_time(estimate_crack_time(entropy))
    pwned_count = is_password_pwned(password)

    if pwned_count > 0:
        feedback.append(f"❌ This password has appeared in {pwned_count} breaches!")

    return score, feedback, entropy, crack_time, pwned_count

# --- UI ---
st.set_page_config(page_title="🚨 Secure Password Analyzer", layout="centered")
st.title("🔐 Extra Secure Password Strength Checker")

password = st.text_input("🔑 Enter your password", type="password")

if password:
    with st.spinner("Running deep password analysis..."):
        time.sleep(1)
        score, feedback, entropy, crack_time, pwned_count = check_password_strength(password)

    st.subheader("📊 Password Report")

    if score == 5:
        st.success("✅ Your password is **extremely strong**! 🟢")
    elif 3 <= score < 5:
        st.warning("🟡 Your password is decent — but could be better.")
    else:
        st.error("❌ Your password is weak or compromised.")

    st.markdown(f"🧠 **Entropy**: `{entropy:.2f}` bits")
    st.markdown(f"⏳ **Estimated crack time**: `{crack_time}`")

    if pwned_count > 0:
        st.error(f"🚨 Your password was found in **{pwned_count:,}** data breaches!")

    st.markdown("### 🧠 Suggestions")
    for tip in feedback:
        st.write("• " + tip)

    st.markdown("### 🔋 Strength Meter")
    st.progress(int((score / 5) * 100))
