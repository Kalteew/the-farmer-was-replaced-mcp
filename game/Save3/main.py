# Ferme AFK adaptative : bootstrap de carottes puis carré de citrouilles.
size = get_world_size()
seed_target = size * size
seed_target = seed_target * 2
carrot_mode = False
if num_items(Items.Carrot) < seed_target:
    carrot_mode = True
clear()

def solve_maze():
    directions = [North, East, South, West]
    facing = 0
    max_steps = get_world_size()
    max_steps = max_steps * max_steps
    max_steps = max_steps * 8

    for step in range(max_steps):
        if get_entity_type() == Entities.Treasure:
            harvest()
            return

        right = (facing + 1) % 4
        if move(directions[right]):
            facing = right
        elif move(directions[facing]):
            pass
        else:
            left = (facing - 1) % 4
            if move(directions[left]):
                facing = left
            else:
                facing = (facing + 2) % 4
                move(directions[facing])

    if get_entity_type() == Entities.Treasure:
        harvest()

def run_maze():
    maze_amount = get_world_size()
    maze_level = num_unlocked(Unlocks.Mazes)
    for level in range(maze_level - 1):
        maze_amount = maze_amount * 2

    if num_items(Items.Weird_Substance) < maze_amount:
        return

    entity = get_entity_type()
    if entity == Entities.Hedge or entity == Entities.Treasure:
        solve_maze()
        return

    if entity != None:
        if can_harvest():
            harvest()
        if get_ground_type() == Grounds.Grassland:
            till()

    if get_entity_type() == None:
        plant(Entities.Bush)

    if get_entity_type() == Entities.Bush:
        use_item(Items.Weird_Substance, maze_amount)
        solve_maze()

def go_to(target_x, target_y):
    while get_pos_x() != target_x:
        move(East)
    while get_pos_y() != target_y:
        move(South)

def maintain_trees():
    size = get_world_size()
    for tree_column in range(3):
        target_x = size - 2 - tree_column * 2
        for target_y in range(0, size, 2):
            go_to(target_x, target_y)
            entity = get_entity_type()
            if entity == None:
                if get_ground_type() == Grounds.Grassland:
                    till()
                if num_items(Items.Wood) > 0:
                    if num_items(Items.Hay) > 0:
                        plant(Entities.Tree)
            elif entity == Entities.Tree:
                if num_items(Items.Fertilizer) > 0:
                    use_item(Items.Fertilizer)
                if can_harvest():
                    harvest()
                if get_entity_type() == None:
                    if num_items(Items.Wood) > 0:
                        if num_items(Items.Hay) > 0:
                            plant(Entities.Tree)
            else:
                if can_harvest():
                    harvest()
                if get_ground_type() == Grounds.Grassland:
                    till()
                if get_entity_type() == None:
                    if num_items(Items.Wood) > 0:
                        if num_items(Items.Hay) > 0:
                            plant(Entities.Tree)

cactus_mode = False

def can_afford(cost):
    if cost == None:
        return False
    for item in cost:
        if num_items(item) < cost[item]:
            return False
    return True

def needs_cactus():
    if num_unlocked(Unlocks.Cactus) <= 1:
        return False

    cost = get_cost(Unlocks.Mazes)
    if cost == None:
        return False

    for item in cost:
        if item == Items.Cactus:
            if num_items(Items.Cactus) < cost[item]:
                return True
    return False

def needs_gold():
    for unlock in [Unlocks.Simulation, Unlocks.Megafarm]:
        cost = get_cost(unlock)
        if cost != None:
            for item in cost:
                if item == Items.Gold:
                    if num_items(Items.Gold) < cost[item]:
                        return True
    return False

def sort_cactus(side):
    for row in range(side):
        for pass_index in range(side):
            go_to(0, row)
            for column in range(side - 1):
                west = measure()
                move(East)
                east = measure()
                if west > east:
                    swap(West)

    for column in range(side):
        for pass_index in range(side):
            go_to(column, 0)
            for row in range(side - 1):
                south = measure()
                move(North)
                north = measure()
                if south > north:
                    swap(South)

def run_cactus_phase():
    size = get_world_size()
    cactus_side = size - 1
    cactus_ready = True

    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()

            cactus_plot = False
            if x < cactus_side:
                if y < cactus_side:
                    cactus_plot = True

            sunflower_plot = False
            if x == size - 1:
                if y < 10:
                    sunflower_plot = True

            if cactus_plot:
                entity = get_entity_type()
                if entity == Entities.Cactus:
                    if not can_harvest():
                        cactus_ready = False
                else:
                    if can_harvest():
                        harvest()
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if can_afford(get_cost(Entities.Cactus)):
                            plant(Entities.Cactus)
                    if get_entity_type() != Entities.Cactus:
                        cactus_ready = False
            elif sunflower_plot:
                if get_ground_type() == Grounds.Grassland:
                    till()
                if get_entity_type() == None:
                    if can_afford(get_cost(Entities.Sunflower)):
                        plant(Entities.Sunflower)
                else:
                    if get_entity_type() == Entities.Sunflower:
                        if can_harvest():
                            harvest()
                        if get_entity_type() == None:
                            if can_afford(get_cost(Entities.Sunflower)):
                                plant(Entities.Sunflower)
            else:
                if can_harvest():
                    harvest()

            if get_water() < 0.5:
                if num_items(Items.Water) > 0:
                    use_item(Items.Water)
            move(North)
        move(East)

    if cactus_ready:
        sort_cactus(cactus_side)
        go_to(0, 0)
        if can_harvest():
            harvest()
        clear()

    go_to(size - 1, size - 1)
    if num_unlocked(Unlocks.Mazes) > 0 and needs_gold():
        run_maze()

while True:
    size = get_world_size()
    pumpkin_side = size - 1
    seed_target = size * size
    seed_target = seed_target * 2

    cactus_needed = needs_cactus()
    if cactus_needed and not cactus_mode:
        cactus_mode = True
        clear()
    elif not cactus_needed and cactus_mode:
        cactus_mode = False
        carrot_mode = True
        clear()

    if cactus_mode:
        run_cactus_phase()
        continue

    if carrot_mode:
        if num_items(Items.Carrot) >= seed_target:
            carrot_mode = False

    if not carrot_mode:
        if num_items(Items.Carrot) < seed_target:
            carrot_mode = True
            clear()
            continue

    tree_drone = None

    if carrot_mode:
        if num_unlocked(Unlocks.Megafarm) > 0:
            tree_drone = spawn_drone(maintain_trees)

        for column in range(size):
            for row in range(size):
                x = get_pos_x()
                y = get_pos_y()

                maze_plot = False
                if x == size - 1:
                    if y == size - 1:
                        maze_plot = True

                sunflower_plot = False
                if x == size - 1:
                    if y < 10:
                        sunflower_plot = True

                tree_plot = False
                if x == size - 2 or x == size - 4 or x == size - 6:
                    if y % 2 == 0:
                        tree_plot = True

                grass_plot = False
                if x >= size - 7:
                    grass_plot = True

                if maze_plot and num_unlocked(Unlocks.Mazes) > 0 and needs_gold():
                    run_maze()
                elif sunflower_plot:
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if can_afford(get_cost(Entities.Sunflower)):
                            plant(Entities.Sunflower)
                    else:
                        if get_entity_type() == Entities.Sunflower:
                            if can_harvest():
                                harvest()
                            if get_entity_type() == None:
                                if can_afford(get_cost(Entities.Sunflower)):
                                    plant(Entities.Sunflower)
                elif tree_plot and tree_drone == None:
                    entity = get_entity_type()
                    if entity == None:
                        if get_ground_type() == Grounds.Grassland:
                            till()
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Tree)
                    elif entity == Entities.Tree:
                        if num_items(Items.Fertilizer) > 0:
                            use_item(Items.Fertilizer)
                        if can_harvest():
                            harvest()
                        if get_entity_type() == None:
                            if num_items(Items.Wood) > 0:
                                if num_items(Items.Hay) > 0:
                                    plant(Entities.Tree)
                    else:
                        if can_harvest():
                            harvest()
                        if get_ground_type() == Grounds.Grassland:
                            till()
                        if get_entity_type() == None:
                            if num_items(Items.Wood) > 0:
                                if num_items(Items.Hay) > 0:
                                    plant(Entities.Tree)
                elif grass_plot:
                    if can_harvest():
                        harvest()
                else:
                    if can_harvest():
                        harvest()
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Carrot)

                if get_water() < 0.5:
                    if num_items(Items.Water) > 0:
                        use_item(Items.Water)
                move(North)
            move(East)

        if tree_drone != None:
            wait_for(tree_drone)
    else:
        pumpkin_ready = True

        for column in range(size):
            for row in range(size):
                x = get_pos_x()
                y = get_pos_y()

                maze_plot = False
                if x == size - 1:
                    if y == size - 1:
                        maze_plot = True

                pumpkin_plot = False
                if x < pumpkin_side:
                    if y < pumpkin_side:
                        pumpkin_plot = True

                sunflower_plot = False
                if x >= pumpkin_side:
                    if y < 5:
                        sunflower_plot = True

                grass_plot = False
                if x >= pumpkin_side:
                    if y >= 5:
                        grass_plot = True

                if maze_plot and num_unlocked(Unlocks.Mazes) > 0 and needs_gold():
                    run_maze()
                elif pumpkin_plot:
                    entity = get_entity_type()
                    if entity == Entities.Dead_Pumpkin:
                        harvest()
                        if num_items(Items.Carrot) > 0:
                            plant(Entities.Pumpkin)
                            pumpkin_ready = False
                        else:
                            pumpkin_ready = False
                    else:
                        if entity == None:
                            if get_ground_type() == Grounds.Grassland:
                                till()
                            if num_items(Items.Carrot) > 0:
                                plant(Entities.Pumpkin)
                                pumpkin_ready = False
                            else:
                                pumpkin_ready = False
                        else:
                            if entity == Entities.Pumpkin:
                                if not can_harvest():
                                    pumpkin_ready = False
                            else:
                                if can_harvest():
                                    harvest()
                                if get_ground_type() == Grounds.Grassland:
                                    till()
                                if get_entity_type() == None:
                                    if num_items(Items.Carrot) > 0:
                                        plant(Entities.Pumpkin)
                                        pumpkin_ready = False
                                    else:
                                        pumpkin_ready = False
                                else:
                                    pumpkin_ready = False
                elif sunflower_plot:
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if can_afford(get_cost(Entities.Sunflower)):
                            plant(Entities.Sunflower)
                    else:
                        if get_entity_type() == Entities.Sunflower:
                            if can_harvest():
                                harvest()
                            if get_entity_type() == None:
                                if can_afford(get_cost(Entities.Sunflower)):
                                    plant(Entities.Sunflower)
                elif grass_plot:
                    if can_harvest():
                        harvest()
                else:
                    if can_harvest():
                        harvest()
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Carrot)

                if get_water() < 0.5:
                    if num_items(Items.Water) > 0:
                        use_item(Items.Water)
                move(North)
            move(East)

        if pumpkin_ready:
            for column in range(size):
                for row in range(size):
                    x = get_pos_x()
                    y = get_pos_y()
                    if x < pumpkin_side:
                        if y < pumpkin_side:
                            if can_harvest():
                                harvest()
                move(North)
            move(East)
            carrot_mode = True
            clear()
