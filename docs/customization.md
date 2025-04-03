# Customization
> [!IMPORTANT]
> *These configs are subject to change, the up-to-date formats can be found in the config directory*.

The package can be customized/configured in the following ways:
1. Custom maps
2. Custom states
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
IDs can be tweaked in the states config.

### Custom States
A state contains the properties of a field on the board (note that this contains the empty field/state). The states config maps the ID of a states to its properties, and is essential for loading maps.

> [!WARNING]
> **IMPORTANT**: A states config should ALWAYS contain a 0 for empty field and 1 for agent!

*Default:*
```json
{
  "0": {
    "is_terminal": false,
    "reward": -1,
    "character": " ",
    "color": "blue"
  },
  "1": {
    "is_terminal": false,
    "reward": -1,
    "character": "=^.^=",
    "color": "red"
  },
  "2": {
    "is_terminal": true,
    "reward": 10,
    "character": "<x)))><",
    "color": "green"
  },
  "3": {
    "is_terminal": true,
    "reward": -1000,
    "character": "hole",
    "color": "red"
  },
  "4": {
    "is_terminal": true,
    "reward": 100,
    "character": "<✰))><",
    "color": "blue"
  },
  "5": {
    "is_terminal": true,
    "reward": -1,
    "character": "<B))><",
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
        "directions": [
            [-1,0]
        ],
        "probabilities": [
            1
        ],
        "cost": 0,
        "char": "↑"
    },
    "down": {
        "id": 1,
        "type": "movement",
        "directions": [
            [1,0]
        ],
        "probabilities": [
            1
        ],
        "cost": 0,
        "char": "↓"
    },
    "left": {
        "id": 2,
        "type": "movement",
        "directions": [
            [0,-1]
        ],
        "probabilities": [
            1
        ],
        "cost": 0,
        "char": "←"
    },
    "right": {
        "id": 3,
        "type": "movement",
        "directions": [
            [0,1]
        ],
        "probabilities": [
            1
        ],
        "cost": 0,
        "char": "→"
    }
}
```

