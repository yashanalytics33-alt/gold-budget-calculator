import streamlit as st
import hashlib
import requests
from PIL import Image

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Gold Budget Calculator", layout="centered")

# -----------------------------
# LOGIN SETUP
# -----------------------------
valid_credentials = {
    "yash": hashlib.sha256("12345".encode()).hexdigest()
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# IMAGE / LOGO
# -----------------------------
img = Image.open('bx.png')
st.image(img)



# -----------------------------
# LOGIN UI
# -----------------------------
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")


if st.button("Login"):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in valid_credentials and hashed_password == valid_credentials[username]:
        st.success("Welcome! Login successful 🎉")
        st.session_state.logged_in = True
    else:
        st.error("Invalid credentials")




# -----------------------------
# LIVE GOLD PRICE FUNCTION
# -----------------------------
def get_live_gold_price_inr(purity):
    try:
        API_KEY = "goldapi-pqpeo19mjjooqr8-io"  # GoldAPI.io
        url = "https://www.goldapi.io/api/XAU/INR"
        headers = {
            "x-access-token": API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        price_per_gram_24k = data["price"] / 31.1035

        purity_map = {
            "24K": 1.0,
            "22K": 0.916,
            "20K": 0.833,
            "18K": 0.75
        }

        return price_per_gram_24k * purity_map[purity], True

    except Exception:
        fallback = {
            "18K": 4500,
            "20K": 5200,
            "22K": 5600,
            "24K": 6000
        }
        return fallback[purity], False

st.info("Enter gold details to estimate your final jewellery cost.")

# -----------------------------
# MAIN APP
# -----------------------------
if st.session_state.logged_in:

    st.markdown("---")
    st.header("💰 Gold Budget Calculator")

    purity = st.selectbox("Select Purity", ["18K", "20K", "22K", "24K"])
    gold_type = st.selectbox(
        "Gold Type",
        ["Chain", "Ring", "Locket", "Bracelet", "Coin", "Bar", "Religious Statue"]
    )

    decoration = st.selectbox(
        "Decoration",
        [
            "None",
            "Diamond (0.25 Carat)",
            "Pink Gemstone (0.1 Carat)",
            "Blue Sapphire (1 Carat)",
            "Swiss Blue Topaz (0.5 Carat)",
            "Natural Emerald (1 Carat)"
        ]
    )

    quantity = st.number_input("Gold Quantity (grams)",  min_value=0.1,
    step=0.1,
    value=10.0)

    # -----------------------------
    # PRICE LOGIC
    # -----------------------------
    type_prices = {
        "Chain": 170,
        "Ring": 150,
        "Locket": 190,
        "Bracelet": 160,
        "Coin": 25,
        "Bar": 70,
        "Religious Statue": 210
    }

    decoration_prices = {
        "None": 0,
        "Diamond (0.25 Carat)": 6500,
        "Pink Gemstone (0.1 Carat)": 22000,
        "Blue Sapphire (1 Carat)": 90000,
        "Swiss Blue Topaz (0.5 Carat)": 11000,
        "Natural Emerald (1 Carat)": 14500
    }

    if st.button("Calculate"):

        gold_price, live = get_live_gold_price_inr(purity)

        base_gold_cost = gold_price * quantity
        making_charges = type_prices[gold_type] * quantity
        decoration_cost = decoration_prices[decoration]

        subtotal = base_gold_cost + making_charges + decoration_cost

        # GST
        cgst = subtotal * 0.03
        sgst = subtotal * 0.03
        total_tax = cgst + sgst
        total_cost = subtotal + total_tax

        # -----------------------------
        # OUTPUT
        # -----------------------------
        st.markdown("---")

        if live:
            st.success(f"Live Gold Price ({purity}): ₹{gold_price:.2f} per gram")
        else:
            st.warning("Live price unavailable. Using fallback price.")

        st.subheader("📊 Cost Breakdown")

        st.write(f"**Base Gold Cost:** ₹{base_gold_cost:.2f}")
        st.write(f"**Making Charges ({gold_type}):** ₹{making_charges:.2f}")
        st.write(f"**Decoration Charges:** ₹{decoration_cost:.2f}")

        st.markdown("---")

        st.subheader("🧾 GST Breakdown")
        st.write(f"CGST (3%): ₹{cgst:.2f}")
        st.write(f"SGST (3%): ₹{sgst:.2f}")

        st.markdown("---")

        st.subheader("💵 Final Amount")
        st.write(f"**Amount before tax:** ₹{subtotal:.2f}")
        st.success(f"**Total Amount (Including GST): ₹{total_cost:.2f}**")

        st.caption("✔️ This amount includes applicable GST (6%).")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit | Gold Budget Calculator")





