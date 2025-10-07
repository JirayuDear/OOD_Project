class Guest: ##เก็บข้อมูลช่องทางเข้ามา ลำดับแขก(เอาไว้ดูกรณีมาหลายคนเฉยๆ) แล้วก็เลขห้องนะ##
    def __init__(self, channel, order, room):
        self.channel = channel
        self.order = order
        self.room = room

    def __repr__(self):
        return f"Guest(channel={self.channel}, order={self.order}, room={self.room})"