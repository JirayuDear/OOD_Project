# guest.py

class Guest:
    def __init__(self, order, channel_ids, preferred_room, channel_names, arrival_round):
        self.order = order
        self.channel_ids = channel_ids
        self.preferred_room = preferred_room
        self.channel_names = channel_names
        self.arrival_round = arrival_round  # CHANGED: Renamed for clarity
        self.room = -1

    def __str__(self):
        path_str = ' -> '.join(f"{name} {id_}" for name, id_ in zip(self.channel_names, self.channel_ids))
        # CHANGED: Added arrival_round to the printout
        return (f"Guest(Round: {self.arrival_round}, Path: {path_str}, Order: {self.order}, "
                f"Room: {self.room})")