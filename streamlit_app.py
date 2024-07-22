import streamlit as st
from data_loader import load_data
from solution_finder import find_solutions
from PIL import Image
import io

def main():
    st.set_page_config(page_title="Mounting Solutions Finder", layout="wide")
    st.title("Mounting Solutions Finder")

    st.warning("Please note: The following solutions are based solely on the provided information. Varying individual circumstances may mean the selected solution won't always be suitable.")

    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    wheelchairs, aac_devices, products = st.session_state.data

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
            st.checkbox("Using Eyegaze?", value=False, disabled=True)
            using_eyegaze = False

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
            solutions = find_solutions(
                st.session_state.data,
                selected_wheelchair,
                selected_device,
                using_eyegaze
            )

            recommended_solution, alternative_solutions = solutions

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

def cap_and_balance_solutions(solutions, cap):
    re_solutions = [s for s in solutions if "Rehadapt" in s]
    da_solutions = [s for s in solutions if "Daessy" in s]
    
    if len(re_solutions) + len(da_solutions) <= cap:
        return solutions
    
    balanced_solutions = []
    while len(balanced_solutions) < cap and (re_solutions or da_solutions):
        if re_solutions:
            balanced_solutions.append(re_solutions.pop(0))
        if len(balanced_solutions) < cap and da_solutions:
            balanced_solutions.append(da_solutions.pop(0))
    
    return balanced_solutions

def display_solution_details(solution, products):
    parts = solution.split('|')
    location = parts[2].split(':')[1].strip()
    st.write(f"Location: {location}")
    
    frame_clamp_name = parts[0].split(':')[1].strip()
    mount_name = parts[1].split(':')[1].strip()

    frame_clamp = next((p for p in products.values() if p.type == 'frame_clamp' and p.name == frame_clamp_name), None)
    mount = next((p for p in products.values() if p.type == 'mount' and p.name == mount_name), None)

    if frame_clamp:
        st.markdown(f"Frame Clamp: [{frame_clamp.name}]({frame_clamp.url})")
        st.write(f"Description: {frame_clamp.description}")
    
    if mount:
        st.markdown(f"Mount: [{mount.name}]({mount.url})")
        st.write(f"Description: {mount.description}")

    # Check if we need to display the M3D Adapter Ring
    if frame_clamp and mount and frame_clamp.manufacturer == "Daessy" and mount.manufacturer == "Rehadapt":
        adapter_ring = next((p for p in products.values() if p.name == "Rehadapt M3D Adapter Ring"), None)
        if adapter_ring:
            st.markdown(f"Adapter Ring: [{adapter_ring.name}]({adapter_ring.url})")
            st.write(f"Description: {adapter_ring.description}")

if __name__ == "__main__":
    main()