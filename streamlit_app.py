import streamlit as st
from data_loader import load_data
from solution_finder import find_solutions

def main():
    st.set_page_config(page_title="Mounting Solutions Finder", layout="wide")
    st.title("Mounting Solutions Finder")

    # Warning message at the top of the page
    st.warning("Please note: The following solutions are based solely on the provided information. Varying individual circumstances may mean the selected solution won't always suitable.")

    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    wheelchairs, aac_devices, mounts, product_urls = st.session_state.data

    col1, col2 = st.columns(2)

    with col1:
        wheelchair_options = ["Please select your wheelchair"] + [wc.model for wc in wheelchairs]
        selected_wheelchair_index = st.selectbox("Select Wheelchair Model:", range(len(wheelchair_options)), format_func=lambda x: wheelchair_options[x])
        selected_wheelchair = wheelchair_options[selected_wheelchair_index] if selected_wheelchair_index > 0 else None

        device_options = ["Please select your device"] + [device.name for device in aac_devices]
        selected_device_index = st.selectbox("Select AAC Device:", range(len(device_options)), format_func=lambda x: device_options[x])
        selected_device = device_options[selected_device_index] if selected_device_index > 0 else None
        
        # Find the selected device
        selected_device_obj = next((device for device in aac_devices if device.name == selected_device), None)
        
        # Only enable the eyegaze checkbox if the device supports it
        if selected_device_obj and selected_device_obj.eyegaze:
            using_eyegaze = st.checkbox("Using Eyegaze?")
        else:
            st.checkbox("Using Eyegaze?", value=False, disabled=True)
            using_eyegaze = False

    # Update solutions whenever a selection changes
    if selected_wheelchair and selected_device:
        solutions = find_solutions(
            st.session_state.data,
            selected_wheelchair,
            selected_device,
            using_eyegaze
        )

        recommended_solution, alternative_solutions = solutions

        # Cap alternative solutions at 5, ensuring solutions from both RE and DA if available
        capped_alternatives = cap_and_balance_solutions(alternative_solutions, 5)

        with col2:
            st.subheader("Recommended Solution:")
            if recommended_solution:
                if st.button("View Recommended Solution"):
                    display_solution_details(recommended_solution, product_urls)

            st.subheader("Alternative Solutions:")
            for i, solution in enumerate(capped_alternatives):
                if st.button(f"View Alternative Solution {i+1}"):
                    display_solution_details(solution, product_urls)
    else:
        with col2:
            st.info("Please select both a wheelchair and an AAC device to view solutions.")

def cap_and_balance_solutions(solutions, cap):
    re_solutions = [s for s in solutions if "(RE)" in s]
    da_solutions = [s for s in solutions if "(DA)" in s]
    
    if len(re_solutions) + len(da_solutions) <= cap:
        return solutions
    
    balanced_solutions = []
    while len(balanced_solutions) < cap and (re_solutions or da_solutions):
        if re_solutions:
            balanced_solutions.append(re_solutions.pop(0))
        if len(balanced_solutions) < cap and da_solutions:
            balanced_solutions.append(da_solutions.pop(0))
    
    return balanced_solutions

def display_solution_details(solution, product_urls):
    # Extract location information
    location = solution.split('|')[2].split(':')[1].strip()
    st.write(f"Location: {location}")
    
    display_product_urls(solution, product_urls)

    # Check for adapter ring requirement
    if "Requires (RE)M3D Adapter Ring" in solution:
        st.write("Note: You will need an (RE)M3D Adapter Ring to use this frame clamp and mount together.")
        adapter_ring_url = product_urls.get("(RE)M3D Adapter Ring", "URL not found")
        st.markdown(f"[(RE)M3D Adapter Ring]({adapter_ring_url})")

def display_product_urls(solution, product_urls):
    frame_clamp = solution.split('|')[0].split(':')[1].strip()
    mount = solution.split('|')[1].split(':')[1].strip()

    frame_clamp_url = product_urls.get(frame_clamp, "URL not found")
    mount_url = product_urls.get(mount, "URL not found")

    st.write(f"Frame Clamp: {frame_clamp}")
    st.markdown(f"[{frame_clamp_url}]({frame_clamp_url})")
    
    st.write(f"Mount: {mount}")
    st.markdown(f"[{mount_url}]({mount_url})")

if __name__ == "__main__":
    main()