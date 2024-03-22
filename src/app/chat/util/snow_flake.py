import threading
import time


class SnowflakeIdGenerator:
    def __init__(self, data_center_id, worker_id):
        # 41비트 타임스탬프, 5비트 데이터 센터 식별자, 5비트 워커 식별자, 12비트 시퀀스 번호
        self.data_center_id = data_center_id
        self.worker_id = worker_id
        self.sequence = 0

        self.last_timestamp = -1
        self.sequence_mask = 0xFFF  # 시퀀스 번호 최대값

        self.data_center_id_shift = 17
        self.worker_id_shift = 12
        self.timestamp_left_shift = 22

        self.twepoch = 1288834974657  # 기준 시간

    def _current_time(self):
        return int(time.time() * 1000) - self.twepoch

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_time()
        while timestamp <= last_timestamp:
            timestamp = self._current_time()
        return timestamp

    def next_id(self):
        with threading.Lock():
            timestamp = self._current_time()

            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            message_id = (
                (timestamp << self.timestamp_left_shift)
                | (self.data_center_id << self.data_center_id_shift)
                | (self.worker_id << self.worker_id_shift)
                | self.sequence
            )
            return message_id


# 예제: 데이터 센터 ID 1, 워커 ID 1로 ID 생성기 초기화
# generator = SnowflakeIdGenerator(data_center_id=1, worker_id=1)
# print(generator.next_id())
