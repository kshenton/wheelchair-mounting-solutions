import streamlit as st
from data_loader import load_data
from solution_finder import find_solutions

st.set_page_config(page_title="Mounting Solutions Finder", layout="wide")

def display_wheelchair_options(wheelchairs, aac_devices, products):
    st.header("Wheelchair Options")
    st.write("Select a wheelchair:")
    wheelchair_options = [wc.model for wc in wheelchairs]
    selected_wheelchair_index = st.selectbox("Wheelchair Options", range(len(wheelchair_options)), format_func=lambda x: wheelchair_options[x])
    selected_wheelchair = wheelchair_options[selected_wheelchair_index]

    st.write("Select an AAC device:")
    aac_device_options = [f"{device.make} {device.model}" for device in aac_devices]
    selected_aac_device_index = st.selectbox("AAC Device Options", range(len(aac_device_options)), format_func=lambda x: aac_device_options[x])
    selected_aac_device = aac_device_options[selected_aac_device_index]

    solutions = find_solutions(wheelchairs, aac_devices, products, selected_wheelchair, selected_aac_device)
    st.write("Recommended mounting solution:")
    st.write(solutions[0])

def main():
    st.title("Mounting Solutions Finder")

    st.warning("Please note: The following solutions are based solely on the provided information. Varying individual circumstances may mean the selected solution won't always be suitable.")

    data = load_data()
    wheelchairs, aac_devices, products = data

    if 'mount_type' not in st.session_state:
        st.session_state.mount_type = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Wheelchair", key="wheelchair_button", use_container_width=True):
            if st.session_state.mount_type != "wheelchair":
                st.session_state.mount_type = "wheelchair"
                st.experimental_rerun()
    with col2:
        if st.button("Floorstand", key="floorstand_button", use_container_width=True):
            if st.session_state.mount_type != "floorstand":
                st.session_state.mount_type = "floorstand"
                st.experimental_rerun()

    if st.session_state.mount_type == "wheelchair":
        display_wheelchair_options(wheelchairs, aac_devices, products)

if __name__ == "__main__":
    main()