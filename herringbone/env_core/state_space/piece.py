class Piece:
    def __init__(
            self,
            is_terminal: bool,
            location: list[int],
            start_location: list[int],
            reward: float,
            is_visitable: bool,
            character: str,
            color: str,
            value: float = 0
    ):
        
        self._is_terminal = is_terminal
        self._location = location
        self._start_location = start_location
        self._reward = reward
        self._is_visitable = is_visitable
        self._character = character
        self._color = color
        self._value = value

    def __str__(
            self
            ):
        return self._character

    # Setters and getters
    def set_is_terminal(
            self, 
            new_terminal: bool
            ):
        
        self._is_terminal = new_terminal
    
    def get_is_terminal(
            self
            ) -> bool: 
        
        return self._is_terminal

    def set_location(
            self, 
            new_loc: list[int]
            ):
        
        self._location = new_loc

    def get_location(
            self
            ) -> list[int]:
        
        return self._location

    def set_start_location(
            self, 
            new_start_loc: list[int]
            ):
        
        self._start_location = new_start_loc
    
    def get_start_location(
            self
            ) -> list[int]:
        
        return self._start_location
    
    def set_reward(
            self, 
            new_reward: float):
        
        self._reward = new_reward
    
    def get_reward(
            self
            ) -> float:
        
        return self._reward
    
    def set_is_visitable(
            self, new_visitable: bool
            ):
        
        self._is_visitable = new_visitable

    def get_is_visitable(
            self
            ) -> bool:
        
        return self._is_visitable
    
    def set_character(
            self, 
            new_char: str):
        
        self._character = new_char
    
    def get_character(
            self
            ) -> str:
        
        return self._character

    def set_color(
            self, 
            new_color: str
            ):
        
        self._color = new_color
    
    def get_color(
            self
            ) -> str:
        
        return self._color
    
    def set_value(
            self, 
            new_val: float
            ):
        
        self._value = new_val

    def get_value(
            self
            ) -> float:
        
        return self._value