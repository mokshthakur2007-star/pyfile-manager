import os
from pathlib import Path
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PyFile Manager", page_icon="📁", layout="centered"
)

st.title("📁 PyFile Manager")
st.caption(
    "A sleek, web-based local file management utility built with Python and Streamlit."
)
st.write("---")

# --- CORE FUNCTIONS ---


def create_file(name, data):
    try:
        path = Path(name)
        if path.exists():
            st.error(f"❌ Error: File '{name}' already exists.")
        else:
            with open(path, "w") as file:
                file.write(data)
            st.success(f"✅ File '{name}' created successfully!")
    except Exception as err:
        st.error(f"⚠️ Error encountered: {err}")


def read_file(name):
    try:
        path = Path(name)
        if not path.exists():
            st.error(f"❌ Error: File '{name}' does not exist.")
            return None
        else:
            with open(path, "r") as file:
                return file.read()
    except Exception as err:
        st.error(f"⚠️ Error encountered: {err}")
        return None


def modify_file(name, operation, new_data="", new_name=""):
    try:
        path = Path(name)
        if not path.exists():
            st.error(f"❌ Error: File '{name}' does not exist.")
            return

        if operation == "Rename":
            new_path = Path(new_name)
            if not new_path.exists():
                path.rename(new_path)
                st.success(f"✅ File renamed to '{new_name}' successfully!")
            else:
                st.error(f"❌ Error: A file named '{new_name}' already exists.")

        elif operation == "Append":
            with open(path, "a") as file:
                file.write(new_data)
            st.success("✅ Data appended successfully!")

        elif operation == "Append with New Line":
            with open(path, "a") as file:
                file.write("\n" + new_data)
            st.success("✅ Data appended with a new line successfully!")

        elif operation == "Overwrite":
            with open(path, "w") as file:
                file.write(new_data)
            st.success("✅ File overwritten successfully!")

    except Exception as err:
        st.error(f"⚠️ Error encountered: {err}")


def delete_file(name):
    try:
        path = Path(name)
        if not path.exists():
            st.error(f"❌ Error: File '{name}' does not exist.")
        else:
            path.unlink()
            st.success(f"🗑️ File '{name}' deleted successfully!")
    except Exception as err:
        st.error(f"⚠️ Error encountered: {err}")


# --- FRONTEND TABS ---
tab1, tab2, tab3, tab4 = st.tabs(
    ["Create File", "Read File", "Modify File", "Delete File"]
)

# 1. CREATE FILE
with tab1:
    st.subheader("Create a New File")
    c_name = st.text_input(
        "File Name (e.g., notes.txt)", key="c_name", placeholder="notes.txt"
    )
    c_data = st.text_area(
        "Initial File Content",
        key="c_data",
        placeholder="Type the content here...",
    )

    if st.button("Create File", type="primary"):
        if c_name:
            create_file(c_name, c_data)
        else:
            st.warning("Please provide a file name.")

# 2. READ FILE
with tab2:
    st.subheader("Read File Content")
    r_name = st.text_input(
        "Enter file name to read", key="r_name", placeholder="notes.txt"
    )

    if st.button("Read File"):
        if r_name:
            content = read_file(r_name)
            if content is not None:
                st.info(f"📄 **Showing content for {r_name}:**")
                st.code(content, language="text")
        else:
            st.warning("Please provide a file name.")

# 3. MODIFY FILE
with tab3:
    st.subheader("Modify an Existing File")
    m_name = st.text_input(
        "Enter file name to modify", key="m_name", placeholder="notes.txt"
    )

    op_choice = st.selectbox(
        "Select an operation:",
        ["Select...", "Rename", "Append", "Append with New Line", "Overwrite"],
    )

    if op_choice == "Rename":
        new_filename = st.text_input("Enter new file name:")
        if st.button("Execute Rename", type="primary"):
            if m_name and new_filename:
                modify_file(m_name, "Rename", new_name=new_filename)
            else:
                st.warning("Please fill in both fields.")

    elif op_choice in ["Append", "Append with New Line", "Overwrite"]:
        mod_data = st.text_area("Enter data:")
        if st.button(f"Execute {op_choice}", type="primary"):
            if m_name:
                modify_file(m_name, op_choice, new_data=mod_data)
            else:
                st.warning("Please provide a file name.")

# 4. DELETE FILE
with tab4:
    st.subheader("Delete a File")
    d_name = st.text_input(
        "Enter file name to delete", key="d_name", placeholder="notes.txt"
    )

    st.warning("⚠️ Warning: This action is permanent and cannot be undone.")
    if st.button("Delete File", type="secondary"):
        if d_name:
            delete_file(d_name)
        else:
            st.warning("Please provide a file name.")