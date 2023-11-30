# src/client/app/home.py

import streamlit as st
import requests

from config import settings, logger, get_user, set_user, clear_user
from schema.auth import NewUser, User
from components import nav_page


# --------------------------------- Definitions ------------------------------ #


# --------------------------------- Setup ----------------------------------- #

# configure page
st.set_page_config(
    page_title="OmicsCopilot",
    page_icon="🧬",
    layout="wide",
)

# initialize session state
for key in ["dataset"]:
    if key not in st.session_state:
        st.session_state[key] = None


# -------------------------------- Sidebar ---------------------------------- #

logout = st.sidebar.button("Logout")


# --------------------------------- Page ------------------------------------ #

if "error" in st.session_state and st.session_state.error is not None:
    if st.session_state.error["type"] == "auth":
        st.error(st.session_state.error["detail"])
        logger.error(f"Authentication error: {st.session_state.error['detail']}")

    st.session_state.error = None

if get_user() is not None:
    st.write("# Welcome to OmicsCopilot! 👋")

    st.markdown(
        """\
    Streamlit is an open-source app built to help research scientists and
    computational biologists analyze multi-omics data.

    To get started, go to the **Sidebar** and select the **Data** tab to upload
    your data or select from one of our curated datasets.
    """
    )

else:
    tabs = st.tabs(["Login", "Register"])

    with tabs[0]:
        with st.form(key="login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            yes = st.checkbox("Remember me", disabled=True)  # TODO: implement
            submit = st.form_submit_button("Login")

            if submit:
                r = requests.post(
                    settings.get_endpoint("auth/login"),
                    json=User(email=email, password=password).model_dump(),
                )

                if r.status_code == 200:
                    set_user(r.json()["user_id"], r.json()["jwt"])

                    st.success(r.json()["message"])
                    logger.info("User logged in successfully.")

                    nav_page("")
                elif r.status_code == 400:
                    st.error(r.json()["detail"])
                else:
                    st.error(r.text)

    with tabs[1]:
        with st.form(key="register"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            cols = st.columns(2)
            full_name = cols[0].text_input("Full name")
            institution = cols[1].text_input("Institution")

            submit = st.form_submit_button("Register")

            if submit:
                r = requests.post(
                    settings.get_endpoint("auth/register"),
                    json=NewUser(
                        email=email, password=password, full_name=full_name
                    ).model_dump(),
                )

                if r.status_code == 200:
                    set_user(r.json()["user_id"], r.json()["jwt"])

                    st.success(r.json()["message"])
                    logger.info("User registered successfully.")

                    nav_page("")
                elif r.status_code == 400:
                    st.error(r.json()["detail"])
                else:
                    st.error(r.text)

if logout:
    r = requests.get(settings.get_endpoint("auth/logout"))

    if r.status_code == 200:
        clear_user()

        st.success(r.json()["message"])
        logger.info("User logged out successfully.")
    else:
        st.error(r.text)
