# Ferme AFK adaptative : bootstrap de carottes puis carré de citrouilles.
size = get_world_size()
seed_target = size * size
seed_target = seed_target * 10
carrot_mode = False
if num_items(Items.Carrot) < seed_target:
    carrot_mode = True
clear()

while True:
    size = get_world_size()
    pumpkin_side = size - 2
    seed_target = size * size
    seed_target = seed_target * 10

    if carrot_mode:
        if num_items(Items.Carrot) >= seed_target:
            carrot_mode = False
            clear()

    if carrot_mode:
        for column in range(size):
            for row in range(size):
                x = get_pos_x()

                grass_plot = False
                if x >= size - 8:
                    grass_plot = True

                if grass_plot:
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
    else:
        pumpkin_ready = True

        for column in range(size):
            for row in range(size):
                x = get_pos_x()
                y = get_pos_y()

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

                if pumpkin_plot:
                    entity = get_entity_type()
                    if entity == Entities.Dead_Pumpkin:
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
