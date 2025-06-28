import streamlit as st
#streamlit run "d:\Bootcamp june 2025\stocks_app\Stock_app\src\homepage\homepagefrontend.py"
st.set_page_config(page_title="Stock Market Landing", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: white;
            padding: 1rem 2rem;
            font-family: Arial, sans-serif;
        }
        .nav-links {
            display: flex;
            gap: 2rem;
            font-size: 16px;
            color: #333;
        }
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
        }
        .signup-button {
            background-color: #ff4081;
            color: white;
            border-radius: 20px;
            padding: 8px 16px;
            font-weight: bold;
            text-decoration: none;
        }
        .left-col h1 {
            font-size: 40px;
            color: #2c2c6c;
            margin-bottom: 0.5rem;
        }
        .left-col h3 {
            color: #1ca1f1;
            margin-top: 0;
        }
        .left-col p {
            font-size: 16px;
            color: #555;
        }
        .register-btn {
            background-color: #ff4081;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown("""
    <div class="navbar">
        <div><img src="https://via.placeholder.com/40/ff4081/ffffff?text=L" style="border-radius: 10px;" alt="Logo"/></div>
        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Services</a>
            <a href="#">Contact</a>
        </div>
        <a class="signup-button" href="#">Sign Up</a>
    </div>
""", unsafe_allow_html=True)

# --- Main Content ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)
    st.markdown("<h1>STOCK MARKET</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Landing Page</h3>", unsafe_allow_html=True)
    st.markdown("<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna.</p>", unsafe_allow_html=True)
    if st.button("REGISTER", key="register_btn"):
        st.success("You clicked Register!")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    # st.image("home1image.jpg", use_container_width=True)
    st.markdown(
    "<img src='https://i.postimg.cc/rsDNCy1V/home1image.jpg' style='width: 100%; height: auto; border-radius: 10px;' alt='Stock Market Image'/>",
    unsafe_allow_html=True
)
