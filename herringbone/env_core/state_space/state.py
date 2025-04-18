class State:
    def __init__(
        self,
        is_terminal: bool,
        location: list[int],
        reward: float,
        character: str,
        color: str,
        idx: int | None
    ):
        self._is_terminal = is_terminal
        self._location = location
        self._reward = reward
        self._character = character
        self._color = color
        self.idx = idx  # 1D, left to right, top to bottom

    def __str__(self):
        return str(self._location)

    def __repr__(self):
        return str(self._location)

    def __eq__(self, other):
        assert isinstance(other, State)
        return self.get_location() == other.get_location()

    def __hash__(self):
        return hash(tuple(self._location))

    # Setters and getters
    def get_is_terminal(self) -> bool:
        return self._is_terminal

    def set_location(self, new_loc: list[int]):
        self._location = new_loc

    def get_location(self) -> list[int]:
        return self._location

    def get_reward(self) -> float:
        return self._reward

    def set_character(self, new_char: str):
        self._character = new_char

    def get_character(self) -> str:
        return self._character

    def set_color(self, new_color: str):
        self._color = new_color

    def get_color(self) -> str:
        return self._color
