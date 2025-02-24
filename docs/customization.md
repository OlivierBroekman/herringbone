# Customization
> [!IMPORTANT]
> *These configs are subject to change, the up-to-date formats can be found in the config directory*.

The package can be customized/configured in the following ways:
1. Custom maps
2. Custom pieces
3. Custom actions.

### Custom Maps

A map is a `.csv` file of IDs. 

*Default:*
```csv
1,0,0,0,0
0,0,0,0,0
0,0,0,0,0
0,0,0,0,2
```
IDs can be tweaked in the pieces config.

### Custom Pieces
A piece contains the properties of a field on the board (note that this contains the empty field/piece). The pieces config maps the ID of a piece to its properties, and is essential for loading maps.

> [!WARNING]
> **IMPORTANT**: A pieces config should ALWAYS contain a 0 for empty field and 1 for agent!

*Default:*
```json
{
  "0": {
    "is_terminal": false,
    "reward": -1,
    "is_visitable": true,
    "character": " ",
    "color": "blue"
  },
  "1": {
    "is_terminal": false,
    "reward": 0,
    "is_visitable": true,
    "character": "=^.^=",
    "color": "red"
  },
  "2": {
    "is_terminal": true,
    "reward": 10,
    "is_visitable": true,
    "character": "<x)))><",
    "color": "green"
  }
}
```
### Custom actions
*Default:*
```json
{
    "up": {
        "id": 0,
        "type": "movement",
        "direction": [
            0,
            1
        ],
        "cost": 0
    },
    "down": {
        "id": 1,
        "type": "movement",
        "direction": [
            0,
            -1
        ],
        "cost": 0
    },
    "left": {
        "id": 2,
        "type": "movement",
        "direction": [
            -1,
            0
        ],
        "cost": 0
    },
    "right": {
        "id": 3,
        "type": "movement",
        "direction": [
            1,
            0
        ],
        "cost": 0
    },
    "observe": {
        "id": 4,
        "type": "observation",
        "direction": [
            0,
            0
        ],
        "cost": 1
    }
}
```

