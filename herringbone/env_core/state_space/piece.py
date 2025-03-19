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

    def __str__(
            self
            ):
        return self._character
    
    def __repr__(
            self
            ):
        return str(self._start_location)
    
    # Setters and getters    
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
    
    def get_start_location(
            self
            ) -> list[int]:
        
        return self._start_location
    
    def get_reward(
            self
            ) -> float:
        
        return self._reward

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