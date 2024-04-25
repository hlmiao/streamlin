import streamlit as st
import msal
import webbrowser
import requests



client_id = "aaaaa-bbbbbb-eeee-cccc-ddddddd"
tenant_id = "bbbbbb-aaaa-ccccc-dddd-eeeeeee"
redirect_uri = "http://localhost:8501/"
scopes = ["https://graph.microsoft.com/.default"]
authority = f"https://login.microsoftonline.com/{tenant_id}"
endpoint = "https://graph.microsoft.com/v1.0/me"

app = msal.PublicClientApplication(
    client_id, authority=authority, verify=False
)

def get_token_from_cache():
    accounts = app.get_accounts()
    if not accounts:
        return None

    result = app.acquire_token_silent(scopes, account=accounts[0])
    if "access_token" in result:
        return result["access_token"]
    else:
        return None

def login():
    flow = app.initiate_auth_code_flow(scopes=scopes, state=['somestupidstate'])

    if "auth_uri" not in flow:
        return st.write("Failed with token")

    auth_uri = flow['auth_uri']
    webbrowser.open(auth_uri, new=0)
    auth_code = st.experimental_get_query_params()

    if 'code' not in auth_code:
        return st.write("Failed with token")

    result = app.acquire_token_by_authorization_code(auth_code, scopes=scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        return st.write("No token found")


if st.button("Login"):
    get_token_from_cache()
    token = login()

    st.write(st.experimental_get_query_params())
    if token:
        st.write("Logged in successfully!")
        st.write(token)
    else:
        st.write("Failed to login")