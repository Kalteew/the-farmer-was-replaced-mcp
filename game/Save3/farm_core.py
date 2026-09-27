# Ferme AFK compacte : carottes, citrouilles, cactus, labyrinthes et dinosaures.
size = get_world_size()
pumpkin_side = 6
if size < 7:
    pumpkin_side = size - 1

cactus_mode = False
pumpkin_mature_passes = 0
maze_cooldown = 0
hay_column = size - 5
hay_floor = 5000
wood_floor = 5000

def go_to(target_x, target_y):
    while get_pos_x() != target_x:
        move(East)
    while get_pos_y() != target_y:
        move(South)

def water():
    if get_water() < 0.5:
        if num_items(Items.Water) > 0:
            use_item(Items.Water)

def can_afford(cost):
    if cost == None:
        return False
    for item in cost:
        if num_items(item) < cost[item]:
            return False
    return True

def plant_carrot():
    if num_items(Items.Wood) > 0:
        if num_items(Items.Hay) > 0:
            plant(Entities.Carrot)

def maintain_carrot():
    entity = get_entity_type()
    if entity == Entities.Carrot:
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            plant_carrot()
    else:
        if can_harvest():
            harvest()
        if get_ground_type() == Grounds.Grassland:
            till()
        if get_entity_type() == None:
            plant_carrot()
    water()

def maintain_hay():
    entity = get_entity_type()
    if entity == Entities.Grass:
        if can_harvest():
            harvest()
    elif entity == Entities.Carrot:
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            if get_ground_type() == Grounds.Soil:
                till()
    elif entity == Entities.Pumpkin:
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            if get_ground_type() == Grounds.Soil:
                till()

def maintain_bush():
    entity = get_entity_type()
    if entity == None:
        plant(Entities.Bush)
    elif entity == Entities.Grass:
        if can_harvest():
            harvest()
        if get_ground_type() == Grounds.Grassland:
            till()
        if get_entity_type() == None:
            plant(Entities.Bush)
    elif entity == Entities.Bush:
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            plant(Entities.Bush)

def farm_bush_column(column):
    go_to(column, 0)
    for row in range(size):
        maintain_bush()
        move(North)

def spawn_bush_workers():
    workers = []
    for column in range(size - 3, size):
        worker = spawn_drone(farm_bush_column, column)
        if worker == None:
            break
        workers.append(worker)
    return workers

def run_wood_bootstrap():
    workers = spawn_bush_workers()
    wait_workers(workers)

def farm_hay_column(column):
    go_to(column, 0)
    for row in range(size):
        maintain_hay()
        move(North)

def run_hay_cycle():
    worker = spawn_drone(farm_hay_column, hay_column)
    if worker == None:
        farm_hay_column(hay_column)
    else:
        wait_for(worker)

def maintain_tree():
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
    water()

def maintain_sunflower():
    if get_ground_type() == Grounds.Grassland:
        till()
    if get_entity_type() == None:
        if can_afford(get_cost(Entities.Sunflower)):
            plant(Entities.Sunflower)
    elif get_entity_type() == Entities.Sunflower:
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            if can_afford(get_cost(Entities.Sunflower)):
                plant(Entities.Sunflower)
    water()

def tree_slot(x, y):
    if y % 2 != 0:
        return False
    if x == size - 2:
        return True
    if x == size - 4:
        return True
    if x == size - 6:
        return True
    return False

def farm_carrot_column(column, start_y):
    for cycle in range(3):
        for target_y in range(start_y, size):
            go_to(column, target_y)
            maintain_carrot()
            move(North)

def spawn_carrot_workers(start_y):
    workers = []
    for column in range(3):
        worker = spawn_drone(farm_carrot_column, column, start_y)
        if worker == None:
            break
        workers.append(worker)
    return workers

def wait_workers(workers):
    for worker in workers:
        wait_for(worker)

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
    amount = get_world_size()
    level = num_unlocked(Unlocks.Mazes)
    for step in range(level - 1):
        amount = amount * 2
    if num_items(Items.Weird_Substance) < amount:
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
        use_item(Items.Weird_Substance, amount)
        solve_maze()

def maybe_run_maze():
    global maze_cooldown
    if maze_cooldown > 0:
        maze_cooldown = maze_cooldown - 1
        return
    if num_unlocked(Unlocks.Mazes) > 0:
        if needs_gold():
            go_to(size - 1, size - 1)
            run_maze()
            maze_cooldown = 8

def needs_gold():
    for unlock in [Unlocks.Simulation, Unlocks.Megafarm]:
        cost = get_cost(unlock)
        if cost != None:
            for item in cost:
                if item == Items.Gold:
                    if num_items(Items.Gold) < cost[item]:
                        return True
    return False

def needs_bones():
    for unlock in [Unlocks.Polyculture, Unlocks.The_Farmers_Remains]:
        cost = get_cost(unlock)
        if cost != None:
            for item in cost:
                if item == Items.Bone:
                    if num_items(Items.Bone) < cost[item]:
                        return True
    return False

def run_dinosaur():
    if num_unlocked(Unlocks.Dinosaurs) <= 0:
        return
    if not needs_bones():
        return
    if num_items(Items.Cactus) < size * 4:
        return

    clear()
    go_to(0, 0)
    change_hat(Hats.Dinosaur_Hat)
    target_x = get_pos_x()
    target_y = get_pos_y()

    for step in range(size * size * 4):
        if get_entity_type() == Entities.Apple:
            target_x, target_y = measure()
        moved = False
        current_x = get_pos_x()
        current_y = get_pos_y()
        if current_x < target_x:
            if can_move(East):
                move(East)
                moved = True
        elif current_x > target_x:
            if can_move(West):
                move(West)
                moved = True
        elif current_y < target_y:
            if can_move(North):
                move(North)
                moved = True
        elif current_y > target_y:
            if can_move(South):
                move(South)
                moved = True
        if not moved:
            for direction in [North, East, South, West]:
                if can_move(direction):
                    move(direction)
                    moved = True
                    break
        if not moved:
            break
    change_hat(Hats.Gold_Hat)

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
    side = size - 1
    cactus_ready = True
    cactus_cycle_complete = False
    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()
            cactus_plot = x < side and y < side
            sunflower_plot = x == size - 1 and y < 10
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
                maintain_sunflower()
            else:
                if can_harvest():
                    harvest()
            water()
            move(North)
        move(East)

    if cactus_ready:
        sort_cactus(side)
        go_to(0, 0)
        if can_harvest():
            harvest()
        clear()
        cactus_cycle_complete = True
        maze_cost = get_cost(Unlocks.Mazes)
        if maze_cost != None:
            for item in maze_cost:
                if item == Items.Cactus:
                    if needs_bones():
                        if num_items(Items.Cactus) >= maze_cost[item] + size * 4:
                            run_dinosaur()
                            return

    if cactus_cycle_complete:
        maybe_run_maze()

def pumpkin_ready_cell():
    entity = get_entity_type()
    if entity == Entities.Dead_Pumpkin:
        harvest()
        if num_items(Items.Carrot) > 0:
            plant(Entities.Pumpkin)
        return False
    if entity == None:
        if get_ground_type() == Grounds.Grassland:
            till()
        if num_items(Items.Carrot) > 0:
            plant(Entities.Pumpkin)
        return False
    if entity == Entities.Pumpkin:
        return can_harvest()
    if can_harvest():
        harvest()
    if get_ground_type() == Grounds.Grassland:
        till()
    if get_entity_type() == None:
        if num_items(Items.Carrot) > 0:
            plant(Entities.Pumpkin)
    return False

def carrot_target():
    target = 25000
    required = pumpkin_side * pumpkin_side * 2
    if target < required:
        target = required
    return target

def pumpkin_target():
    return 130000

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

def cactus_inputs_missing():
    cost = get_cost(Entities.Cactus)
    if cost == None:
        return False
    return not can_afford(cost)

def run_carrot_cycle():
    workers = spawn_carrot_workers(0)
    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()
            delegated = x < 3
            if not delegated:
                if x == hay_column:
                    maintain_hay()
                elif x == size - 1 and y < 10:
                    maintain_sunflower()
                elif tree_slot(x, y):
                    maintain_tree()
                else:
                    maintain_carrot()
            move(North)
        move(East)
    wait_workers(workers)

def run_pumpkin_cycle():
    global pumpkin_mature_passes
    workers = spawn_carrot_workers(6)
    pumpkin_ready = True
    pumpkin_count = 0

    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()
            delegated = x < 3 and y >= 6
            pumpkin_plot = x < pumpkin_side and y < pumpkin_side
            if delegated:
                pass
            elif pumpkin_plot:
                if not pumpkin_ready_cell():
                    pumpkin_ready = False
                else:
                    pumpkin_count = pumpkin_count + 1
            elif tree_slot(x, y):
                maintain_tree()
            elif x == hay_column:
                maintain_hay()
            elif x == size - 1 and y < 10:
                maintain_sunflower()
            elif x < pumpkin_side:
                maintain_carrot()
            else:
                if can_harvest():
                    harvest()
            water()
            move(North)
        move(East)

    if pumpkin_count < pumpkin_side * pumpkin_side:
        pumpkin_ready = False
    if pumpkin_ready:
        pumpkin_mature_passes = pumpkin_mature_passes + 1
    else:
        pumpkin_mature_passes = 0

    if pumpkin_mature_passes >= 2:
        before = num_items(Items.Pumpkin)
        for column in range(size):
            for row in range(size):
                if get_pos_x() < pumpkin_side and get_pos_y() < pumpkin_side:
                    if can_harvest():
                        harvest()
                move(North)
            move(East)
        if num_items(Items.Pumpkin) > before:
            pumpkin_mature_passes = 0
    wait_workers(workers)
    if pumpkin_ready:
        maybe_run_maze()
