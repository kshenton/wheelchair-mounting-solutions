def find_solutions(data, selected_wheelchair, selected_device, using_eyegaze):
    wheelchairs, aac_devices, products = data
    
    selected_device_obj = next((device for device in aac_devices if f"{device.make} {device.model}" == selected_device), None)
    if not selected_device_obj:
        return None, []
    
    selected_device_weight = selected_device_obj.weight

    for wc in wheelchairs:
        if wc.model == selected_wheelchair:
            all_solutions = []
            available_frame_clamps = [products[clamp_id] for clamp_id in wc.frame_clamp_ids if products.get(clamp_id) and products[clamp_id].type == 'frame_clamp']
            
            compatible_mounts = [m for m in products.values() if m.type == 'mount' and selected_device_weight <= m.weight_capacity]

            for clamp in available_frame_clamps:
                for mount in compatible_mounts:
                    if clamp.manufacturer == "Rehadapt" and mount.manufacturer == "Daessy":
                        continue  # Skip this combination as it's not allowed

                    solution = f"Frame Clamp: {clamp.name} | Mount: {mount.name} | Location: {wc.mount_location}"
                    
                    if clamp.manufacturer == "Daessy" and mount.manufacturer == "Rehadapt":
                        solution += " | Adapter Ring: Rehadapt M3D Adapter Ring"
                    
                    if using_eyegaze and mount.manufacturer == "Rehadapt" and mount.name != "M3D Plus HD":
                        continue  # Skip non-M3D Plus HD Rehadapt mounts for eyegaze devices
                    
                    all_solutions.append((solution, clamp.manufacturer, mount.manufacturer))

            recommended_solution = select_recommended_solution(all_solutions, using_eyegaze, selected_device_weight)
            alternative_solutions = [s[0] for s in all_solutions if s != recommended_solution]

            return recommended_solution[0] if recommended_solution else None, alternative_solutions

    return None, []

def select_recommended_solution(solutions, using_eyegaze, device_weight):
    if using_eyegaze or device_weight >= 2.4:
        preferred_manufacturer = "Daessy"
    else:
        preferred_manufacturer = "Rehadapt"

    # If eyegaze or device weight >= 2.4, prioritize Daessy solutions
    if preferred_manufacturer == "Daessy":
        solution = next((s for s in solutions if s[1] == "Daessy" and s[2] == "Daessy"), None)
        if solution:
            return solution
        # If no full Daessy solution, try Daessy mount with any frame clamp
        solution = next((s for s in solutions if s[2] == "Daessy"), None)
        if solution:
            return solution
        # If still no solution and using eyegaze, try Rehadapt M3D Plus HD
        if using_eyegaze:
            solution = next((s for s in solutions if "M3D Plus HD" in s[0]), None)
            if solution:
                return solution
    
    # For Rehadapt preference (device weight < 2.4 and no eyegaze)
    if preferred_manufacturer == "Rehadapt":
        # Try to find a solution with Rehadapt for both frame clamp and mount
        solution = next((s for s in solutions if s[1] == "Rehadapt" and s[2] == "Rehadapt"), None)
        if solution:
            return solution
        # If not found, try to find a solution with at least a Rehadapt mount
        solution = next((s for s in solutions if s[2] == "Rehadapt"), None)
        if solution:
            return solution

    # If no preferred solution is found, return any available solution
    if solutions:
        return solutions[0]
    
    return None