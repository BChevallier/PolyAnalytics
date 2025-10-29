# Replay controls and coordinates
## Controls

| Key     | Effect                         |
| ------- | ------------------------------ |
| G       | Toggle showing turn bar        |
| H       | Toggle showing menu bar        |
| P       | Select Point of view           |
| W,A,S,D | Move camera                    |
| ARROWS  | Move tile selection            |
| E       | Show map view of current tribe |
| R       | Show map view of all tribes    |
| T       | Uncover complete map           |
| C       | Center map and zoom out        |

## Coordinates
### Techtree
The following provides the coordinates (in a 800x500 image with 0-0 at the top left) to our color sampling pixels for each tech. These will be blueish if a tech is not completed and greenish if it is completed. The tech tree should be at max zoom out level.

| Tech         | coords    |
| ------------ | --------- |
| Riding       | (403,204) |
| Roads        | (393,171) |
| Trade        | (383,138) |
| Free Spirit  | (430,184) |
| Chivalry     | (458,164) |
| Organisation | (425,236) |
| Farming      | (453,217) |
| Construction | (481,197) |
| Strategy     | (453,257) |
| Diplomacy    | (480,278) |
| Climbing     | (400,269) |
| Mining       | (428,289) |
| Smithery     | (456,310) |
| Meditation   | (390,301) |
| Philosophy   | (378,333) |
| Fishing      | (362,255) |
| Sailing      | (352,288) |
| Navigation   | (340,320) |
| Ramming      | (329,256) |
| Aquatism     | (295,255) |
| Hunting      | (363,215) |
| Archery      | (329,215) |
| Spiritualism | (295,215) |
| Forrestry    | (353,183) |
| Mathematics  | (343,150) |

### Turn detection
Turn detection should be done by looking at the color of the pixel at (10,33). This one will always have the color of the currently playing tribe. 
