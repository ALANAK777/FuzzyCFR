import streamlit as st

# Set page layout to wide
st.set_page_config(layout="wide")

# Initializing session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None  # Track if the user is 'admin' or 'user'

# Hardcoded login credentials
credentials = {
    "user@gmail.com": {"password": "123", "role": "user"},
    "admin@gmail.com": {"password": "123", "role": "admin"}
}

# Define login function
def login(email, password):
    if email in credentials and credentials[email]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user_role = credentials[email]["role"]
        return True
    else:
        return False

# Logout function
def logout():
    st.session_state.clear()  # Clear session state to force logout and reset app

# Main content area
if not st.session_state.logged_in:
    # Login page
    st.markdown("# Login Page")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")
    login_button = st.button("Login")
    
    if login_button:
        if login(email, password):
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password.")
else:
    # Navigation after login
    if st.session_state.user_role == "admin":
        st.sidebar.title("Admin Page")
        if st.sidebar.button("Logout"):
            logout()

        # Admin-specific content
        st.markdown("# Welcome, Admin")
        st.write("This is the admin dashboard.")

        # You can add more admin functionalities here
        if st.sidebar.button("Manage Users"):
            st.write("Admin can manage users here.")

        if st.sidebar.button("View Reports"):
            st.write("Admin can view reports here.")

    elif st.session_state.user_role == "user":
        st.sidebar.title("User Page")
        if st.sidebar.button("Logout"):
            logout()

        # User-specific content
        st.markdown("# Welcome, User")
        st.write("This is the user dashboard.")

        # User dashboard functionality
        if st.sidebar.button("Settings"):
            st.write("User can adjust their settings here.")

        if st.sidebar.button("Search Products"):
            st.write("User can search for products here.")

        if st.sidebar.button("Search Suppliers"):
            st.write("User can search for suppliers here.")

# Customize the page appearance (Optional CSS)
st.markdown(
    """
    <style>
    .css-18e3th9 {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        font-size: 18px;
    }

    .stSidebar {
        background-color: grey;
    }
    
    .stSidebar .stButton > button {
        color: black;
        background-color: white;
        border: 2px solid black;
        border-radius: 5px;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        width: 100%;
    }

    .stSidebar .stButton > button:focus {
        background-color: white !important;
        color: black !important;
        border-color: black !important;
    }
    </style>
    """, unsafe_allow_html=True
)
