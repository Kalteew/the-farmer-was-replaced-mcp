# Ferme AFK adaptative : bootstrap de carottes puis carré de citrouilles.
size = get_world_size()
seed_target = size * size
seed_target = seed_target * 10
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

while True:
    size = get_world_size()
    pumpkin_side = size - 1
    seed_target = size * size
    seed_target = seed_target * 10

    if carrot_mode:
        if num_items(Items.Carrot) >= seed_target:
            carrot_mode = False

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

                if maze_plot and num_unlocked(Unlocks.Mazes) > 0:
                    run_maze()
                elif sunflower_plot:
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Sunflower)
                    else:
                        if get_entity_type() == Entities.Sunflower:
                            if can_harvest():
                                harvest()
                            if get_entity_type() == None:
                                if num_items(Items.Wood) > 0:
                                    if num_items(Items.Hay) > 0:
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

                if maze_plot and num_unlocked(Unlocks.Mazes) > 0:
                    run_maze()
                elif pumpkin_plot:
                    entity = get_entity_type()
                    if entity == Entities.Dead_Pumpkin:
                        harvest()
                        if num_items(Items.Carrot) > 0:
                            plant(Entities.Pumpkin)
                        else:
                            pumpkin_ready = False
                    else:
                        if entity == None:
                            if get_ground_type() == Grounds.Grassland:
                                till()
                            if num_items(Items.Carrot) > 0:
                                plant(Entities.Pumpkin)
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
                                    else:
                                        pumpkin_ready = False
                                else:
                                    pumpkin_ready = False
                elif sunflower_plot:
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Sunflower)
                    else:
                        if get_entity_type() == Entities.Sunflower:
                            if can_harvest():
                                harvest()
                            if get_entity_type() == None:
                                if num_items(Items.Wood) > 0:
                                    if num_items(Items.Hay) > 0:
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
