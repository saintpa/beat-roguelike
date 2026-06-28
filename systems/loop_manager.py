import time
from typing import Optional


class LoopSlot:
    def __init__(self):
        self.events: list[tuple[float, str]] = []
        self.is_recording: bool = False
        self.is_playing: bool = False
        self.record_start_time: Optional[float] = None
        self.length: float = 0.0


class LoopManager:
    def __init__(self):
        self.slots: dict[int, LoopSlot] = {i: LoopSlot() for i in range(10)}
        self.active_recording_slot: Optional[int] = None

    def toggle_recording(self, slot_number: int):
        slot = self.slots[slot_number]

        if slot.is_recording:
            self.stop_recording(slot_number)
        else:
            self.start_recording(slot_number)

    def start_recording(self, slot_number: int):
        if self.active_recording_slot is not None:
            self.stop_recording(self.active_recording_slot)

        slot = self.slots[slot_number]

        slot.events = []
        slot.is_recording = True
        slot.is_playing = False
        slot.record_start_time = time.time()
        slot.length = 0.0

        self.active_recording_slot = slot_number

        print(f"Recording loop slot {slot_number}")

    def stop_recording(self, slot_number: int):
        slot = self.slots[slot_number]

        if not slot.is_recording or slot.record_start_time is None:
            return

        slot.length = time.time() - slot.record_start_time
        slot.is_recording = False
        slot.record_start_time = None

        if self.active_recording_slot == slot_number:
            self.active_recording_slot = None

        print(f"Stopped recording slot {slot_number}")
        print(f"Events: {slot.events}")
        print(f"Length: {slot.length:.2f}s")

    def record_pad_press(self, pad_key: str):
        if self.active_recording_slot is None:
            return

        slot = self.slots[self.active_recording_slot]

        if not slot.is_recording or slot.record_start_time is None:
            return

        elapsed = time.time() - slot.record_start_time
        slot.events.append((elapsed, pad_key))

        print(f"Recorded {pad_key} at {elapsed:.2f}s")

    def record_initial_active_pads(self, active_pad_keys: list[str]):
        if self.active_recording_slot is None:
            return

        slot = self.slots[self.active_recording_slot]

        if not slot.is_recording:
            return

        for pad_key in active_pad_keys:
            slot.events.append((0.0, pad_key))
            print(f"Recorded active pad {pad_key} at 0.00s")
