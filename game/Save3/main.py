# Maintenance torique : chaque case est visitée une fois, sans casser le wrap.
size = get_world_size()
for column in range(size):
    for row in range(size):
        if can_harvest():
            harvest()
        if get_ground_type() == Grounds.Soil:
            if num_items(Items.Wood) > 0:
                if num_items(Items.Hay) > 0:
                    plant(Entities.Carrot)
        else:
            if get_pos_x() == 0:
                if get_pos_y() == 0:
                    pass
                else:
                    plant(Entities.Bush)
            else:
                plant(Entities.Bush)
        move(North)
    move(East)
