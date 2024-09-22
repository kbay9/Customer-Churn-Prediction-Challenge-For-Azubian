import streamlit as st
from home import show as show_home
from data import show as show_data
from dashboard import show as show_dashboard
from predict import show as show_prediction
from history import show as show_history
from database import authenticate, create_customer_data_table

# Setting Streamlit page configuration
st.set_page_config(
    page_title="Churn App",
    page_icon="images/churn01.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app logic
def main():

    create_customer_data_table()

    if 'login_status' not in st.session_state:
        st.session_state['login_status'] = False

    if st.session_state['login_status']:
        if st.sidebar.button("Logout"):
            st.session_state['login_status'] = False
            st.sidebar.success("You have been logged out.")
            st.rerun()

        # User is logged in, show sidebar menu
        st.sidebar.header(f"Logged in as {st.session_state['username']}")
        page = st.sidebar.radio(
            "Go to", ('Home', 'Data', 'Dashboard', 'Prediction', 'History'))
        if page == 'Home':
            show_home()
        elif page == 'Data':
            show_data()
        elif page == 'Dashboard':
            show_dashboard()
        elif page == 'Prediction':
            show_prediction()
        elif page == 'History':
            show_history()

    else:
        # User is not logged in, show login form
        with st.sidebar:
            st.title("Login")
            with st.form(key='login_form'):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button(label='Login')

                if submit_button:
                    if authenticate(username, password):
                        st.session_state['login_status'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("Incorrect Username/Password")

        # Showing login prompt in the main are
        st.markdown("""
                <h2 style='text-align: center;'>CHURN MANAGEMENT APPLICATION</h2>
                """, unsafe_allow_html=True)
        container = st.container()
        col1, col2, col3 = container.columns([1, 5, 1])

        with col2:
            st.image("images/churn05.png", use_column_width="always")

if __name__ == "__main__":
    main()
