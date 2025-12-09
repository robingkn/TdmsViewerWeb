import streamlit as st
import tdms_backend
import tdms_ui

# Configure the Streamlit page
st.set_page_config(page_title="TDMS Viewer", layout="wide")
st.title("📈 TDMS File Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload a TDMS file", type=["tdms"])

if uploaded_file:
    # Load the TDMS file
    tdms = tdms_backend.load_tdms(uploaded_file)

    # Render the tree in the sidebar and get the current selection
    selection = tdms_ui.sidebar_tree(tdms)

    # Fetch and display properties in the sidebar
    props = tdms_backend.get_properties(
        tdms,
        selection["type"],
        group=selection.get("group"),
        channel=selection.get("channel")
    )
    tdms_ui.show_properties(props)

    # If a channel is selected, also show its data
    if selection["type"] == "channel":
        channel_obj = tdms[selection["group"]][selection["channel"]]
        tdms_ui.show_channel_data(channel_obj)
