class Piece:
    def __init__(
            self,
            is_terminal: bool,
            location: list[int],
            start_location: list[int],
            reward: float,
            is_visitable: bool,
            character: str,
            color: str
    ):
        self._is_terminal = is_terminal
        self._location = location
        self._start_location = start_location
        self._reward = reward
        self._is_visitable = is_visitable
        self._character = character
        self._color = color

    def __str__(self):
        return self._character

    # Setters and getters
    @property
    def is_terminal(self) -> bool:
        return self._is_terminal

    @is_terminal.setter
    def is_terminal(self, new_value: bool):
        self._is_terminal = new_value

    @property
    def location(self) -> list[int]:
        return self._location

    @location.setter
    def location(self, new_location: list[int]):
        self._location = new_location

    @property
    def start_location(self) -> list[int]:
        return self._start_location

    @property
    def reward(self) -> float:
        return self._reward

    @reward.setter
    def reward(self, new_reward: float):
        self._reward = new_reward

    @property
    def is_visitable(self) -> bool:
        return self._is_visitable

    @is_visitable.setter
    def is_visitable(self, new_value: bool):
        self._is_visitable = new_value

    @property
    def character(self) -> str:
        return self._character

    @character.setter
    def character(self, new_char: str):
        self._character = new_char

    @property
    def color(self) -> str:
        return self._color
