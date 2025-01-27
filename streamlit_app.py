import streamlit as st
from data_loader import load_data
from solution_finder import find_solutions, cap_and_balance_solutions
from PIL import Image
import io

st.set_page_config(page_title="Mounting Solutions Finder", layout="wide")

def main():
    st.title("Mounting Solutions Finder")

    st.warning("Please note: The following solutions are based solely on the provided information. Varying individual circumstances may mean the selected solution won't always be suitable.")

    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    wheelchairs, aac_devices, products = st.session_state.data

    if 'mount_type' not in st.session_state:
        st.session_state.mount_type = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Wheelchair", use_container_width=True):
            if st.session_state.mount_type != "wheelchair":
                st.session_state.mount_type = "wheelchair"
                st.experimental_rerun()
    with col2:
        if st.button("Floorstand", use_container_width=True):
            if st.session_state.mount_type != "floorstand":
                st.session_state.mount_type = "floorstand"
                st.experimental_rerun()

    if st.session_state.mount_type == "wheelchair":
        display_wheelchair_options(wheelchairs, aac_devices, products)
    elif st.session_state.mount_type == "floorstand":
        display_floorstand_options(aac_devices, products)

if __name__ == "__main__":
    main()

def display_wheelchair_options(wheelchairs, aac_devices, products):
    col1, col2 = st.columns([1, 1])

    with col1:
        wheelchair_options = ["Please select your wheelchair"] + [wc.model for wc in wheelchairs]
        selected_wheelchair_index = st.selectbox("Select Wheelchair Model:", range(len(wheelchair_options)), format_func=lambda x: wheelchair_options[x])
        selected_wheelchair = wheelchair_options[selected_wheelchair_index] if selected_wheelchair_index > 0 else None

        device_options = ["Please select your device"] + [f"{device.make} {device.model}" for device in aac_devices]
        selected_device_index = st.selectbox("Select AAC Device:", range(len(device_options)), format_func=lambda x: device_options[x])
        selected_device = device_options[selected_device_index] if selected_device_index > 0 else None
        
        selected_device_obj = next((device for device in aac_devices if f"{device.make} {device.model}" == selected_device), None)
        
        if selected_device_obj and selected_device_obj.eyegaze:
            using_eyegaze = st.checkbox("Using Eyegaze?")
        else:
            using_eyegaze = st.checkbox("Using Eyegaze?", value=False, disabled=True)

        # Display wheelchair and AAC device images
        image_col1, image_col2 = st.columns(2)

        if selected_wheelchair:
            wheelchair_obj = next((wc for wc in wheelchairs if wc.model == selected_wheelchair), None)
            if wheelchair_obj and wheelchair_obj.wheelchair_image:
                with image_col1:
                    image = Image.open(io.BytesIO(wheelchair_obj.wheelchair_image))
                    image.thumbnail((250, 250))
                    st.image(image, caption=selected_wheelchair, use_column_width=False)

        if selected_device:
            if selected_device_obj and selected_device_obj.device_image:
                with image_col2:
                    image = Image.open(io.BytesIO(selected_device_obj.device_image))
                    image.thumbnail((250, 250))
                    st.image(image, caption=selected_device, use_column_width=False)

    with col2:
        if selected_wheelchair and selected_device:
            recommended_solution, alternative_solutions = find_solutions(
                st.session_state.data,
                selected_wheelchair,
                selected_device,
                using_eyegaze
            )

            if recommended_solution:
                st.subheader("Recommended Solution:")
                if st.button("View Recommended Solution"):
                    display_solution_details(recommended_solution, products)

                st.subheader("Alternative Solutions:")
                capped_alternatives = cap_and_balance_solutions(alternative_solutions, 5)
                for i, solution in enumerate(capped_alternatives):
                    if st.button(f"View Alternative Solution {i+1}"):
                        display_solution_details(solution, products)
            else:
                st.info("No recommended solution found.")
        else:
            st.info("Please select both a wheelchair and an AAC device to view solutions.")

def display_floorstand_options(aac_devices, products):
    col1, col2 = st.columns([1, 1])

    with col1:
        device_options = ["Please select your device"] + [f"{device.make} {device.model}" for device in aac_devices]
        selected_device_index = st.selectbox("Select AAC Device:", range(len(device_options)), format_func=lambda x: device_options[x])
        selected_device = device_options[selected_device_index] if selected_device_index > 0 else None

        if selected_device:
            selected_device_obj = next((device for device in aac_devices if f"{device.make} {device.model}" == selected_device), None)
            if selected_device_obj and selected_device_obj.device_image:
                image = Image.open(io.BytesIO(selected_device_obj.device_image))
                image.thumbnail((250, 250))
                st.image(image, caption=selected_device, use_column_width=False)

    with col2:
        if selected_device:
            selected_device_obj = next((device for device in aac_devices if f"{device.make} {device.model}" == selected_device), None)
            if selected_device_obj:
                compatible_floorstands = [p for p in products.values() if p.type == 'floorstand' and selected_device_obj.weight <= p.weight_capacity]
                
                if compatible_floorstands:
                    st.subheader("Compatible Floorstands:")
                    for floorstand in compatible_floorstands:
                        if st.button(f"View {floorstand.name}"):
                            display_floorstand_details(floorstand)
                else:
                    st.info("No compatible floorstands found for this device.")
            else:
                st.info("Please select an AAC device to view compatible floorstands.")

def display_solution_details(solution, products):
    solution_string, frame_clamp, mount, adaptor = solution
    parts = solution_string.split('|')
    location = parts[-1].split(':')[1].strip()

    st.markdown(f"**Frame Clamp: [{frame_clamp.name}]({frame_clamp.url})**")
    st.write(f"Manufacturer: {frame_clamp.manufacturer}")
    st.write(f"Description: {frame_clamp.description}")
    st.write(f"Location: {location}")

    st.write("")  # Add a blank line for spacing

    st.markdown(f"**Mount: [{mount.name}]({mount.url})**")
    st.write(f"Manufacturer: {mount.manufacturer}")
    st.write(f"Description: {mount.description}")

    if adaptor:
        st.write("")  # Add a blank line for spacing
        st.write("You will need the following adaptor to interface the above two parts:")
        st.markdown(f"**Adaptor: [{adaptor.name}]({adaptor.url})**")
        st.write(f"Manufacturer: {adaptor.manufacturer}")
        st.write(f"Description: {adaptor.description}")

def display_floorstand_details(floorstand):
    st.markdown(f"**Floorstand: [{floorstand.name}]({floorstand.url})**")
    st.write(f"Manufacturer: {floorstand.manufacturer}")
    st.write(f"Description: {floorstand.description}")
    st.write(f"Weight Capacity: {floorstand.weight_capacity} kg")

if __name__ == "__main__":
    main()