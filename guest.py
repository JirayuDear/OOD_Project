# guest.py
class Guest:
    def __init__(self, channel_name, channel_order, room=0):
        self.channel_name = channel_name
        self.channel_order = channel_order
        self.room = room

    # MODIFIED: ปรับปรุงการแสดงผลเป็นรูปแบบคอลัมน์ที่อ่านง่าย
    def __repr__(self):
        # จัดคอลัมน์: Channel (กว้าง 25 ตัวอักษร), Order (5), Room (ที่เหลือ)
        return f"  {self.channel_name:<25} | Order: {self.channel_order+1:<5} | Room: {self.room}"