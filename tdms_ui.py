import streamlit as st
import pandas as pd


def sidebar_tree(tdms):
    """Render the TDMS structure in the sidebar with collapsible groups and clean tree appearance."""
    st.sidebar.header("🗂️ TDMS Structure")

    if "selected" not in st.session_state:
        st.session_state.selected = {"type": "file"}

    with st.sidebar:
        # Root level
        if st.button("🗄️ File Root", use_container_width=True):
            st.session_state.selected = {"type": "file"}

        # Groups
        for group in tdms.groups():
            with st.expander(f"📂 {group.name}", expanded=False):
                # Group-level button
                if st.button("Properties", key=f"group_{group.name}_select", use_container_width=True):
                    st.session_state.selected = {"type": "group", "group": group.name}

                # Channels
                for channel in group.channels():
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        st.write("")  # Empty space for indentation
                    with col2:
                        icon = "📈" if "ai" in channel.name.lower() else "📊"
                        if st.button(f"{icon} {channel.name}",
                                     key=f"{group.name}_{channel.name}",
                                     use_container_width=True):
                            st.session_state.selected = {
                                "type": "channel",
                                "group": group.name,
                                "channel": channel.name,
                            }

    return st.session_state.selected




def show_properties(props):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Properties")
    if isinstance(props, dict) and props:
        for k, v in props.items():
            st.sidebar.markdown(f"**{k}**: {v}")
    else:
        st.sidebar.write("No properties found.")


def get_axis_data(channel):
    try:
        x_data = channel.time_track()
        x_label = "Time"
    except KeyError:
        x_data = range(len(channel))
        x_label = "Index"
    y_data = channel[:]
    return x_data, y_data, x_label


def render_data_table(df):
    st.subheader("📋 Channel Data")
    st.dataframe(df, use_container_width=True)


def render_plot(df, x_label):
    st.subheader("📈 Channel Plot")
    st.line_chart(df.set_index(x_label))


def show_channel_data(channel):
    x_data, y_data, x_label = get_axis_data(channel)
    df = pd.DataFrame({x_label: x_data, "Value": y_data})

    render_data_table(df)
    render_plot(df, x_label)
