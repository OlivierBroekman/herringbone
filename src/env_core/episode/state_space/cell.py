class Cell:
    """This class represents a cell in a gridworld"""
    # TODO: Change piece in constructor to instance of piece class, added str as placeholder
    def __init__(self, coordinates: list[int], piece: str = None):
        self.coordinates = coordinates
        self.piece = piece