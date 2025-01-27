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
                    # Check for incompatible combinations
                    if (clamp.manufacturer == "Rehadapt" and mount.manufacturer == "Daessy"):
                        continue  # Skip this combination as it's not allowed

                    adaptor = None
                    if (clamp.manufacturer in ["Daessy", "Etac"] and mount.manufacturer == "Rehadapt"):
                        adaptor = next((p for p in products.values() if p.type == 'adaptor' and p.name == "M3D Adapter Ring"), None)
                    elif clamp.manufacturer == "Etac" and mount.manufacturer == "Daessy":
                        adaptor = next((p for p in products.values() if p.type == 'adaptor' and p.name == "IPA (Inner Piece Adaptor)"), None)
                    
                    if using_eyegaze and mount.manufacturer == "Rehadapt" and mount.name != "M3D Plus HD":
                        continue  # Skip non-M3D Plus HD Rehadapt mounts for eyegaze devices
                    
                    solution = f"Frame Clamp: {clamp.name} | Mount: {mount.name}"
                    if adaptor:
                        solution += f" | Adaptor: {adaptor.name}"
                    solution += f" | Location: {wc.mount_location}"
                    
                    all_solutions.append((solution, clamp, mount, adaptor))

            recommended_solution = select_recommended_solution(all_solutions, using_eyegaze, selected_device_weight)
            
            # Ensure the M3D Adapter Ring is suggested when necessary
            if recommended_solution:
                clamp, mount, adaptor = recommended_solution[1:4]
                if clamp.manufacturer in ["Daessy", "Etac"] and mount.manufacturer == "Rehadapt" and not adaptor:
                    m3d_adapter = next((p for p in products.values() if p.type == 'adaptor' and p.name == "Rehadapt M3D Adapter Ring"), None)
                    if m3d_adapter:
                        new_solution = list(recommended_solution)
                        new_solution[0] += f" | Adaptor: {m3d_adapter.name}"
                        new_solution[3] = m3d_adapter
                        recommended_solution = tuple(new_solution)

            alternative_solutions = [s for s in all_solutions if s != recommended_solution]

            return recommended_solution, alternative_solutions

    return None, []

def select_recommended_solution(solutions, using_eyegaze, device_weight):
    if using_eyegaze or device_weight > 2.5:
        preferred_manufacturer = "Daessy"
    else:
        preferred_manufacturer = "Rehadapt"

    # If eyegaze or device weight > 2.5, prioritize Daessy solutions
    if preferred_manufacturer == "Daessy":
        solution = next((s for s in solutions if s[2].manufacturer == "Daessy"), None)
        if solution:
            return solution
    
    # For Rehadapt preference (device weight <= 2.4 and no eyegaze)
    elif preferred_manufacturer == "Rehadapt":
        solution = next((s for s in solutions if s[2].manufacturer == "Rehadapt"), None)
        if solution:
            return solution
    
    # If no preferred solution is found, return any available solution
    if solutions:
        return solutions[0]
    
    return None

def cap_and_balance_solutions(solutions, cap):
    re_solutions = [s for s in solutions if "Rehadapt" in s[0]]
    da_solutions = [s for s in solutions if "Daessy" in s[0]]
    et_solutions = [s for s in solutions if "Etac" in s[0]]
    
    if len(re_solutions) + len(da_solutions) + len(et_solutions) <= cap:
        return solutions
    
    balanced_solutions = []
    while len(balanced_solutions) < cap and (re_solutions or da_solutions or et_solutions):
        if re_solutions:
            balanced_solutions.append(re_solutions.pop(0))
        if len(balanced_solutions) < cap and da_solutions:
            balanced_solutions.append(da_solutions.pop(0))
        if len(balanced_solutions) < cap and et_solutions:
            balanced_solutions.append(et_solutions.pop(0))
    
    return balanced_solutions