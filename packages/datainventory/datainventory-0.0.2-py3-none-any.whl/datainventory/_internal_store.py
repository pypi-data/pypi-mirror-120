# Copyright © 2021 by IoT Spectator. All rights reserved.

"""Internal module that defines common class and definitions."""

CREATE_KEY = "0x4352454154455f4b4559"  # CREATE_KEY ASCII Code


class InternalStore:
    """Basic data store definition used internally."""

    def __init__(self, create_key, device_id: str) -> None:
        if create_key is not CREATE_KEY:
            raise RuntimeError("This method should not be called from outside")
        self._device_id = device_id
