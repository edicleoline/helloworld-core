from __future__ import annotations

import time

# Twitter SnowFlake
# Edicleo Oliveira
# 0 - 0000000000 0000000000 0000000000 0000000000 0000000000 0000000000
# ^    ^                                              ^           ^
# |    |                                              |           |
# |    |                                              |        Seq Number (12 bits)
# |    |                                              Worker ID (10 bits)
# |    Timestamp (41 bits)
# Sinal (1 bit)

class Snowflake:
    epoch: int
    worker_id: int
    datacenter_id: int
    sequence: int

    worker_id_bits: int
    datacenter_id_bits: int
    sequence_bits: int

    max_worker_id: int
    max_datacenter_id: int
    sequence_mask: int

    worker_id_shift: int
    datacenter_id_shift: int
    timestamp_shift: int
    last_timestamp: int


    def init(self, worker_id: int, datacenter_id: int, epoch=1288834974657):
        self.epoch = epoch
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0

        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.sequence_bits = 12

        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

        self.last_timestamp = -1

        if worker_id > self.max_worker_id or worker_id < 0:
            raise ValueError(f"Worker ID deve estar entre 0 e {self.max_worker_id}")
        if datacenter_id > self.max_datacenter_id or datacenter_id < 0:
            raise ValueError(f"Datacenter ID deve estar entre 0 e {self.max_datacenter_id}")

    @staticmethod
    def _current_timestamp():
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate(self):
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("O relógio foi ajustado para trás. Não podemos gerar IDs.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        snow_flake_id = (
            ((timestamp - self.epoch) << self.timestamp_shift) |
            (self.datacenter_id << self.datacenter_id_shift) |
            (self.worker_id << self.worker_id_shift) |
            self.sequence
        )

        return snow_flake_id


snow_flake = Snowflake()
snow_flake.init(worker_id=1, datacenter_id=1)
# snowflake_id = snow_flake.generate()
# print(snowflake_id)
