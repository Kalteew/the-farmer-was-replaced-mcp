# Ferme AFK torique optimisée : huit cases de foin,
# quinze parcelles de carottes, puis arbres et buissons.
clear()

while True:
    size = get_world_size()
    for column in range(size):
        for row in range(size):
            x = get_pos_x()
            y = get_pos_y()
            harvested = False
            if can_harvest():
                harvest()
                harvested = True

            reserve_plot = False
            if x == 0:
                reserve_plot = True

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

            if reserve_plot:
                pass
            else:
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

                if get_water() < 0.5:
                    if num_items(Items.Water) > 0:
                        use_item(Items.Water)
            move(North)
        move(East)