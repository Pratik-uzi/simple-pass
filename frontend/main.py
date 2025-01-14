import streamlit as st
import requests
import time
from requests.exceptions import RequestException

BASE_URL = "http://127.0.0.1:5000"

def check_server():
    try:
        response = requests.get(BASE_URL)
        return response.status_code == 200
    except:
        return False

def load_passwords():
    try:
        response = requests.get(f"{BASE_URL}/view")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def main():
    st.set_page_config(
        page_title="Simple Pass",
        page_icon="🔐",
        layout="wide"
    )
    
    st.title("🔐 Simple Pass")
    st.caption("A simple and secure password manager")
    
    tab1, tab2 = st.tabs(["Add Password", "View Passwords"])
    
    # Add Password Tab
    with tab1:
        with st.form("password_form"):
            app_name = st.text_input("Application/Platform")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Save Password")

            if submitted:
                if not all([app_name, username, password]):
                    st.error("Please fill in all required fields!")
                else:
                    try:
                        payload = {
                            "application": app_name,
                            "username": username,
                            "password": password
                        }
                        with st.spinner('Saving password...'):
                            response = requests.post(f"{BASE_URL}/add", json=payload)
                        
                        if response.status_code == 201:
                            st.success("✅ Password saved successfully!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to save password: {response.json().get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred: {str(e)}")

    # View Passwords Tab
    with tab2:
        passwords = load_passwords()
        
        if st.button("🔄 Refresh"):
            st.rerun()

        if not passwords:
            st.info("No passwords stored yet!")
        else:
            for pwd in passwords:
                with st.expander(f"📁 {pwd['application']} - {pwd['username']}", expanded=False):
                    col1, col2, col3 = st.columns([3, 0.5, 0.5])
                    
                    with col1:
                        master_password = st.text_input("Master Password", type="password", 
                                                      key=f"master_{pwd['id']}")
                        if st.button("👁️ Show", key=f"show_{pwd['id']}"):
                            try:
                                view_response = requests.get(
                                    f"{BASE_URL}/view/{pwd['id']}", 
                                    json={"master_password": master_password}
                                )
                                if view_response.status_code == 200:
                                    password_data = view_response.json()
                                    st.success("✅ Password decrypted successfully!")
                                    st.code(password_data['password'], language=None)
                                else:
                                    st.error("❌ Invalid master password!")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
                    with col2:
                        # Edit button
                        if st.button("✏️", key=f"edit_btn_{pwd['id']}"):
                            if not master_password:
                                st.error("❌ Please enter master password first")
                            else:
                                st.session_state[f'editing_{pwd["id"]}'] = True
                    
                    with col3:
                        # Delete button
                        if st.button("🗑️", key=f"delete_btn_{pwd['id']}"):
                            if not master_password:
                                st.error("❌ Please enter master password first")
                            else:
                                st.session_state[f'deleting_{pwd["id"]}'] = True

                    # Show delete confirmation
                    if st.session_state.get(f'deleting_{pwd["id"]}', False):
                        st.warning("⚠️ Are you sure you want to delete this password?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("❌ Cancel", key=f"cancel_delete_btn_{pwd['id']}"):
                                del st.session_state[f'deleting_{pwd["id"]}']
                                st.rerun()
                        with col2:
                            if st.button("🗑️ Confirm Delete", key=f"confirm_delete_btn_{pwd['id']}", type="primary"):
                                try:
                                    response = requests.delete(
                                        f"{BASE_URL}/delete/{pwd['id']}", 
                                        json={"master_password": master_password}
                                    )
                                    if response.status_code == 200:
                                        st.success("✅ Password deleted successfully!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Invalid master password!")
                                except Exception as e:
                                    st.error(f"❌ Failed to delete password: {str(e)}")

                    # Edit form
                    if st.session_state.get(f'editing_{pwd["id"]}', False):
                        new_password = st.text_input("New Password", type="password",
                                                   key=f"new_password_{pwd['id']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("❌ Cancel", key=f"cancel_edit_btn_{pwd['id']}"):
                                del st.session_state[f'editing_{pwd["id"]}']
                                st.rerun()
                        with col2:
                            if st.button("💾 Save Changes", key=f"save_edit_btn_{pwd['id']}", type="primary"):
                                try:
                                    response = requests.put(
                                        f"{BASE_URL}/update/{pwd['id']}", 
                                        json={
                                            "master_password": master_password,
                                            "new_password": new_password
                                        }
                                    )
                                    if response.status_code == 200:
                                        st.success("✅ Password updated successfully!")
                                        del st.session_state[f'editing_{pwd["id"]}']
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to update password!")
                                except Exception as e:
                                    st.error(f"❌ Error updating password: {str(e)}")

if __name__ == "__main__":
    main()
