def find_solutions(data, selected_wheelchair, selected_device, using_eyegaze):
    wheelchairs, aac_devices, mounts, product_urls = data
    selected_device_weight = next(device.weight for device in aac_devices if device.name == selected_device)

    all_solutions = []
    for wc in wheelchairs:
        if wc.model == selected_wheelchair:
            da_solutions = []
            re_solutions = []
            for clamp in wc.frame_clamps:
                clamp_supplier = clamp[:3]
                filtered_mounts = [m for m in mounts if selected_device_weight <= m.weight_capacity]

                for mount in filtered_mounts:
                    if clamp.startswith("(RE)") and mount.name.startswith("(DA)"):
                        continue

                    solution = f"Frame Clamp: {clamp} | Mount: {mount.name} | Location: {wc.mount_location}"
                    
                    if clamp.startswith("(DA)") and mount.name.startswith("(RE)"):
                        solution += " | Note: Requires (RE)M3D Adapter Ring"
                    
                    if mount.name.startswith("(DA)"):
                        da_solutions.append(solution)
                    else:
                        re_solutions.append(solution)

            recommended_solution = select_recommended_solution(da_solutions, re_solutions, using_eyegaze, selected_device_weight)
            alternative_solutions = [s for s in da_solutions + re_solutions if s != recommended_solution]

            return recommended_solution, alternative_solutions

    return None, []

def select_recommended_solution(da_solutions, re_solutions, using_eyegaze, device_weight):
    if using_eyegaze or device_weight > 2.2:
        return select_solution(da_solutions, "(DA)Locking Bent Pole Rigid Mount", "(DA)")
    elif device_weight < 1.3:
        return select_solution(re_solutions, "(RE)H3D", "(RE)")
    elif 1.3 <= device_weight < 2:
        return select_solution(re_solutions, "(RE)M3D Quickshift", "(RE)") or select_solution(da_solutions, "(DA)M3D Quickshift", "(DA)")
    else:
        return select_solution(re_solutions, "", "(RE)") or select_solution(da_solutions, "", "(DA)")

def select_solution(solutions, preferred_mount, preferred_clamp):
    solution = next((s for s in solutions if preferred_mount in s and s.startswith(f"Frame Clamp: {preferred_clamp}")), None)
    if not solution:
        solution = next((s for s in solutions if s.startswith(f"Frame Clamp: {preferred_clamp}")), None)
    if not solution and solutions:
        solution = solutions[0]
    return solution