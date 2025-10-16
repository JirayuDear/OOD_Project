# guest.py

class Guest:
    def __init__(self, order, channel_ids, preferred_room, channel_names, arrival_round,manual=None):
        self.order = order
        self.channel_ids = channel_ids
        self.preferred_room = preferred_room
        self.channel_names = channel_names
        self.arrival_round = arrival_round  # CHANGED: Renamed for clarity
        self.room = -1
        self.manual = manual

    def __str__(self):
        path_str = ' -> '.join(f"{name} {id_}" for name, id_ in zip(self.channel_names, self.channel_ids))
        # CHANGED: Added arrival_round to the printout
        if self.manual != None:
            return (f"Guest(Round: {self.arrival_round} ({self.manual}), Path: {path_str}, Order: {self.order}, "
                f"Room: {self.room})")
        return (f"Guest(Round: {self.arrival_round}, Path: {path_str}, Order: {self.order}, "
                f"Room: {self.room})")
    
    def get_channel_string(self):
        
        if not self.channel_names or not self.channel_ids:
            return "N/A"
        return " -> ".join(
            f"{name} {id_}" for name, id_ in zip(self.channel_names, self.channel_ids)
        )