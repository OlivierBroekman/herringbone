from piece import Piece

class Cell:
    """This class represents a cell in a gridworld"""
    def __init__(self, coordinates: list[int], piece: Piece = None):
        self._coordinates = coordinates
        self._piece = piece

    def __str__(self):
        return str(self._piece)
    
    # Setters and getters
    @property
    def coordinates(self) -> list[int]:
        return self.coordinates
    
    @coordinates.setter
    def coordinates(self, new_coordinates: list[int]):
        self.coordinates = new_coordinates
    
    @property
    def piece(self) -> Piece:
        return self.piece
    
    @piece.setter
    def piece(self, new_piece: Piece):
        self.piece = new_piece