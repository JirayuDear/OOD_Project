class Guest:
    def __init__(self, order, channel_ids, preferred_room, channel_names):
        self.order = order                 # ลำดับของแขก
        self.channel_ids = channel_ids     # ID ของแต่ละช่องทาง เช่น [1, 3]
        self.preferred_room = preferred_room # **ห้องที่ต้องการ (คำนวณแค่ครั้งเดียวตอนสร้าง)**
        self.channel_names = channel_names # ชื่อช่องทาง (เพื่อแสดงผล)
        self.room = -1                     # ห้องจริงที่ได้รับ

    def __str__(self):
        path_str = ' -> '.join(f"{name} {id}" for name, id in zip(self.channel_names, self.channel_ids))
        return f"Guest(Path: {path_str}, Order: {self.order}, Pref. Room: {self.preferred_room}, Final Room: {self.room})"