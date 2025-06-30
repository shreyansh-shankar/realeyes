import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        content = str(self.index) + str(self.timestamp) + str(self.data) + str(self.prev_hash)
        return hashlib.sha256(content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, prev_block.hash)
        self.chain.append(new_block)

    def get_chain(self):
        return self.chain

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]

            if cur.hash != cur.compute_hash():
                return False
            if cur.prev_hash != prev.hash:
                return False
        return True