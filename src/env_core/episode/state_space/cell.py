class Cell:
    """This class represents a cell in a gridworld"""
    # TODO: Change piece in constructor to instance of piece class, added str as placeholder
    def __init__(self, coordinates: list[int], piece: str = None):
        self._coordinates = coordinates
        self._piece = piece
    
    # Setters and getters
    @property
    def coordinates(self) -> list[int]:
        return self.coordinates
    
    @coordinates.setter
    def coordinates(self, new_coordinates: list[int]):
        self.coordinates = new_coordinates
    
    @property
    def piece(self) -> str:
        return self.piece
    
    @piece.setter
    def piece(self, new_piece):
        self.piece = new_piece