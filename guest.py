
class Guest:
    def __init__(self, order, aircraft_id, barge_id, car_id, room=0):
        self.order = order # guest_num
        self.aircraft_id = aircraft_id
        self.barge_id = barge_id
        self.car_id = car_id
        self.room = room

    def get_channel_string(self):
        # ถ้าเป็นแขกเริ่มต้น (ที่เราจะมาร์คด้วย -1) ให้แสดงผลเป็นพิเศษ
        if self.aircraft_id == -1:
            return f"initial_guest"
        return f"aircraft{self.aircraft_id}_barge{self.barge_id}_car{self.car_id}"

    def __repr__(self):
        return f"Guest(channel={self.get_channel_string()}, order={self.order}, room={self.room})"