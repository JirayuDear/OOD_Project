# hash_table.py (Optimized Resize Version)

class HashTable:
    def __init__(self, size=16):
        self.size = size
        self.table = [None] * self.size
        self.count = 0
        self._DELETED = object()

    @property
    def load_factor(self):
        return self.count / self.size
    
    def __len__(self):
        return self.count

    def _hash(self, key):
        return key % self.size

    def search(self, key):
        index = self._hash(key)
        start_index = index
        while self.table[index] is not None:
            if self.table[index] != self._DELETED and self.table[index][0] == key:
                return self.table[index][1]

            index = (index + 1) % self.size
            if index == start_index: return None
        return None

    def insert(self, preferred_key, value):

        if self.load_factor > 0.7:
            self.resize()
            
        final_key = preferred_key
        # Loop ที่ช้านี้จะทำงานเฉพาะตอนเพิ่มแขกใหม่เท่านั้น
        while self.search(final_key) is not None:
            final_key += 1

        # เมื่อได้ final_key แล้ว ก็เรียกใช้ internal_insert ที่เร็วมาก
        self._internal_insert(final_key, value)
        
        return final_key

    def _internal_insert(self, key, value):

        index = self._hash(key)
        start_index = index
        while self.table[index] is not None and self.table[index] != self._DELETED:
            index = (index + 1) % self.size
            if index == start_index:
                 raise Exception("HashTable is full during internal insert")

        self.table[index] = (key, value)
        self.count += 1
        
    def resize(self):

        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        print(f"\n--- Resizing hash table to {self.size} (Fast Path) ---")
        
        for item in old_table:
            if item is not None and item != self._DELETED:
                self._internal_insert(item[0], item[1])

    def remove(self, key):
        index = self._hash(key)
        start_index = index
        while self.table[index] is not None:
            if self.table[index] != self._DELETED and self.table[index][0] == key:
                # ใช้ Tombstone มาร์คตำแหน่งว่าถูกลบแล้ว
                self.table[index] = self._DELETED
                self.count -= 1
                return True # คืนค่าว่าลบสำเร็จ

            index = (index + 1) % self.size
            if index == start_index:
                return False # วนกลับมาที่เดิมแล้วแต่ไม่เจอ
        return False # ไม่เจอ key ที่จะลบ





