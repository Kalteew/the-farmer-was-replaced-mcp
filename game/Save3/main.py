# Ferme AFK torique : foin, puissance solaire, carottes, arbres et buissons.
# Les 10 tournesols sont inspectés à chaque tour et seul celui qui a le
# plus de pétales est récolté, ce qui active le bonus de puissance x8.
clear()

while True:
    size = get_world_size()
    best_petals = -1
    best_x = -1
    best_y = -1
    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()

            reserve_plot = False
            if x == 0:
                reserve_plot = True

            sunflower_plot = False
            if x == 3:
                if y == 0:
                    sunflower_plot = True
                if y == 1:
                    sunflower_plot = True
                if y == 2:
                    sunflower_plot = True
                if y == 3:
                    sunflower_plot = True
                if y == 4:
                    sunflower_plot = True
                if y == 5:
                    sunflower_plot = True
            if x == 4:
                if y == 0:
                    sunflower_plot = True
                if y == 1:
                    sunflower_plot = True
                if y == 2:
                    sunflower_plot = True
                if y == 3:
                    sunflower_plot = True

            carrot_plot = False
            if x == 1:
                carrot_plot = True
            if x == 2:
                if y == 0:
                    carrot_plot = True
                if y == 1:
                    carrot_plot = True
                if y == 2:
                    carrot_plot = True
                if y == 3:
                    carrot_plot = True
                if y == 4:
                    carrot_plot = True
                if y == 5:
                    carrot_plot = True
                if y == 6:
                    carrot_plot = True

            tree_plot = False
            if size % 2 == 0:
                if x % 2 == 0:
                    if y % 2 == 0:
                        tree_plot = True
                else:
                    if y % 2 == 1:
                        tree_plot = True
            else:
                if x == 1:
                    if y == 1:
                        tree_plot = True
                    if y == 3:
                        tree_plot = True
                if x == 2:
                    if y == 0:
                        tree_plot = True
                    if y == 2:
                        tree_plot = True
                if x == 3:
                    if y == 1:
                        tree_plot = True
                    if y == 3:
                        tree_plot = True

            if sunflower_plot:
                if get_ground_type() == Grounds.Grassland:
                    till()
                if get_entity_type() == None:
                    plant(Entities.Sunflower)
                else:
                    if get_entity_type() == Entities.Sunflower:
                        if can_harvest():
                            petals = measure()
                            if petals > best_petals:
                                best_petals = petals
                                best_x = x
                                best_y = y
            elif reserve_plot:
                if can_harvest():
                    harvest()
            else:
                harvested = False
                if can_harvest():
                    harvest()
                    harvested = True

                if carrot_plot:
                    if get_ground_type() == Grounds.Grassland:
                        till()
                    if get_entity_type() == None:
                        if num_items(Items.Wood) > 0:
                            if num_items(Items.Hay) > 0:
                                plant(Entities.Carrot)
                else:
                    if tree_plot:
                        if get_ground_type() == Grounds.Grassland:
                            if harvested:
                                plant(Entities.Tree)
                            else:
                                if get_entity_type() == None:
                                    plant(Entities.Tree)
                    else:
                        if get_ground_type() == Grounds.Grassland:
                            if harvested:
                                plant(Entities.Bush)
                            else:
                                if get_entity_type() == None:
                                    plant(Entities.Bush)

            if not reserve_plot:
                if get_water() < 0.5:
                    if num_items(Items.Water) > 0:
                        use_item(Items.Water)
            move(North)
        move(East)

    if best_x != -1:
        while get_pos_x() != best_x:
            move(East)
        while get_pos_y() != best_y:
            move(North)
        if can_harvest():
            harvest()
        if get_entity_type() == None:
            plant(Entities.Sunflower)

