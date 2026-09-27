import farm_core

while True:
    if num_items(Items.Hay) < farm_core.hay_floor:
        farm_core.run_hay_cycle()
    elif num_items(Items.Wood) < farm_core.wood_floor:
        farm_core.run_wood_bootstrap()
    elif num_items(Items.Carrot) < farm_core.carrot_target():
        farm_core.run_carrot_cycle()
    elif num_items(Items.Pumpkin) < farm_core.pumpkin_target():
        farm_core.run_pumpkin_cycle()
    else:
        cactus_needed = farm_core.needs_cactus()
        if farm_core.cactus_inputs_missing():
            cactus_needed = False
        if cactus_needed:
            if not farm_core.cactus_mode:
                farm_core.cactus_mode = True
                farm_core.pumpkin_mature_passes = 0
                clear()
            farm_core.run_cactus_phase()
        else:
            if farm_core.cactus_mode:
                farm_core.cactus_mode = False
                farm_core.pumpkin_mature_passes = 0
            farm_core.run_pumpkin_cycle()
