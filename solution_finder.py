import tkinter as tk
import webbrowser

def find_solutions(app):
    selected_wheelchair = app.wheelchair_var.get()
    selected_device = app.device_var.get()
    using_eyegaze = app.eyegaze_var.get()

    all_solutions = []

    selected_device_weight = next(device.weight for device in app.aac_devices if device.name == selected_device)

    for wc in app.wheelchairs:
        if wc.model == selected_wheelchair:
            da_solutions = []
            re_solutions = []
            for clamp in wc.frame_clamps:
                clamp_supplier = clamp[:3]  # Get the prefix (RE) or (DA)
                filtered_mounts = [m for m in app.mounts if selected_device_weight <= m.weight_capacity]

                for mount in filtered_mounts:
                    # Skip invalid combinations
                    if clamp.startswith("(RE)") and mount.name.startswith("(DA)"):
                        continue

                    solution = f"Frame Clamp: {clamp} | Mount: {mount.name} | Location: {wc.mount_location}"
                    
                    # Add note for DA frame clamp with RE mount
                    if clamp.startswith("(DA)") and mount.name.startswith("(RE)"):
                        solution += " | Note: Requires (RE)M3D Adapter Ring"
                    
                    if mount.name.startswith("(DA)"):
                        da_solutions.append(solution)
                    else:
                        re_solutions.append(solution)

            # Determine recommended solution
            if using_eyegaze or selected_device_weight > 2.2:
                # Prioritize DA solutions for Eyegaze or heavy devices
                recommended_solution = next((s for s in da_solutions if "(DA)Locking Bent Pole Rigid Mount" in s and s.startswith("Frame Clamp: (DA)")), None)
                if not recommended_solution:
                    recommended_solution = next((s for s in da_solutions if s.startswith("Frame Clamp: (DA)")), None)
                if not recommended_solution and da_solutions:
                    recommended_solution = da_solutions[0]
                elif not recommended_solution and re_solutions:
                    recommended_solution = re_solutions[0]
            elif selected_device_weight < 1.3:
                # Prioritize RE solutions for light devices
                recommended_solution = next((s for s in re_solutions if "(RE)H3D" in s and s.startswith("Frame Clamp: (RE)")), None)
                if not recommended_solution:
                    recommended_solution = next((s for s in re_solutions if s.startswith("Frame Clamp: (RE)")), None)
                if not recommended_solution and re_solutions:
                    recommended_solution = re_solutions[0]
                elif not recommended_solution and da_solutions:
                    recommended_solution = da_solutions[0]
            elif 1.3 <= selected_device_weight < 2:
                # Prioritize RE M3D Quickshift for medium-weight devices
                recommended_solution = next((s for s in re_solutions if "(RE)M3D Quickshift" in s and s.startswith("Frame Clamp: (RE)")), None)
                if not recommended_solution:
                    recommended_solution = next((s for s in da_solutions if "(DA)M3D Quickshift" in s and s.startswith("Frame Clamp: (DA)")), None)
                if not recommended_solution and re_solutions:
                    recommended_solution = re_solutions[0]
                elif not recommended_solution and da_solutions:
                    recommended_solution = da_solutions[0]
            else:
                # For other cases, prioritize matching frame clamp and mount
                recommended_solution = next((s for s in re_solutions if s.startswith("Frame Clamp: (RE)")), None)
                if not recommended_solution:
                    recommended_solution = next((s for s in da_solutions if s.startswith("Frame Clamp: (DA)")), None)
                if not recommended_solution and re_solutions:
                    recommended_solution = re_solutions[0]
                elif not recommended_solution and da_solutions:
                    recommended_solution = da_solutions[0]

            # Ensure we always have a recommended solution
            if not recommended_solution:
                if re_solutions:
                    recommended_solution = re_solutions[0]
                elif da_solutions:
                    recommended_solution = da_solutions[0]

            # Collect alternative solutions
            alternative_solutions = [s for s in da_solutions + re_solutions if s != recommended_solution]

            break  # Exit the loop once we've processed the selected wheelchair

    # Clear the listboxes
    app.recommended_listbox.delete(0, tk.END)
    app.alternative_listbox.delete(0, tk.END)

    # Add recommended solution to the recommended listbox
    if recommended_solution:
        app.recommended_listbox.insert(tk.END, recommended_solution)

    # Add alternative solutions to the alternative listbox
    for solution in alternative_solutions:
        app.alternative_listbox.insert(tk.END, solution)

    # Clear the result text
    app.result_text.delete(1.0, tk.END)
    app.result_text.insert(tk.END, "Select a solution to see product URLs.")

def on_solution_select(app, event):
    widget = event.widget
    if widget.curselection():
        index = widget.curselection()[0]
        solution = widget.get(index)
        
        # Extract frame clamp and mount from the solution
        frame_clamp = solution.split('|')[0].split(':')[1].strip()
        mount = solution.split('|')[1].split(':')[1].strip()

        # Look up the URLs for the selected products
        frame_clamp_url = app.product_urls.get(frame_clamp, "URL not found")
        mount_url = app.product_urls.get(mount, "URL not found")

        # Display the URLs
        app.result_text.delete(1.0, tk.END)
        app.result_text.insert(tk.END, f"Product URLs for the selected solution:\n\n")
        app.result_text.insert(tk.END, f"Frame Clamp: {frame_clamp}\n")
        insert_hyperlink(app.result_text, frame_clamp_url, frame_clamp_url + "\n\n")
        app.result_text.insert(tk.END, f"Mount: {mount}\n")
        insert_hyperlink(app.result_text, mount_url, mount_url + "\n")

        # Check if adapter ring is needed
        if "Requires (RE)M3D Adapter Ring" in solution:
            adapter_ring_url = app.product_urls.get("(RE)M3D Adapter Ring", "URL not found")
            app.result_text.insert(tk.END, "\nNote: You will need an (RE)M3D Adapter Ring to use this frame clamp and mount together.\n")
            app.result_text.insert(tk.END, "(RE)M3D Adapter Ring:\n")
            insert_hyperlink(app.result_text, adapter_ring_url, adapter_ring_url + "\n")

def insert_hyperlink(text_widget, url, display_text):
    text_widget.tag_config("hyperlink", foreground="blue", underline=1)
    text_widget.insert(tk.END, display_text, "hyperlink")
    text_widget.tag_bind("hyperlink", "<Button-1>", lambda e: open_url(url))

def open_url(url):
    webbrowser.open_new(url)