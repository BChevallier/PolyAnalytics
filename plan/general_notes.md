# General Notes
This file is where we write down everything we figured out that might be important to writing the project code. It is recommended to take a look at this file at the beginning of each coding session.

## Accessing replays from IDs
We were provided with a list of IDs. Replays have to accessed through the game (steam, epic, iOS). Add the ID to the following URL to open in...
- ...Steam: steam://run/874390//opengame?id=
- ...Epic: com.epicgames.launcher://apps/3ce838d7a25c49368a22918b56e88f2a?action=launch&silent=true&arg=-deeplink%3Dopengame%3Fid%3D
- ...iOS: polytopia://opengame?id=

## Identifier by Tribe
To save space (even though it's kinda ridiculous) tribes will referenced by the following identifiers in the code and csv.


| Identifier | Tribe    |
| ---------- | -------- |
| Tr1        | Xin-xi   |
| Tr2        | Imperius |
| Tr3        | Bardour  |
| Tr4        | Oumaji   |
| Tr5        | Kickoo   |
| Tr6        | Hoodrick |
| Tr7        | Luxidoor |
| Tr8        | Vengir   |
| Tr9        | Zebasi   |
| Tr10       | Ai-Mo    |
| Tr11       | Quetzali |
| Tr12       | Yadakk   |
| Tr13       | Aquarion |
| Tr14       | Elyrion  |
| Tr15       | Polaris  |
| Tr16       | Cymanti  |

identifier2tribe = {
    "Tr1": "Xin-xi",
    "Tr2": "Imperius",
    "Tr3": "Bardour",
    "Tr4": "Oumaji",
    "Tr5": "Kickoo",
    "Tr6": "Hoodrick",
    "Tr7": "Luxidoor",
    "Tr8": "Vengir",
    "Tr9": "Zebasi",
    "Tr10": "Ai-Mo",
    "Tr11": "Quetzali",
    "Tr12": "Yadakk",
    "Tr13": "Aquarion",
    "Tr14": "Elyrion",
    "Tr15": "Polaris",
    "Tr16": "Cymanti"
}

## Color values by tribe:
Each tribe has a distinct color value associated with it. This color can be seen in the territory borders (if there are no duplicate tribes in a game). It can also be seen in the circle in the top left corner while watching replays (which can be used for turn and tribe-detection).

| Identifier | Color           |
|------------|-----------------|
| Tr1        | (204, 0, 0)     |
| Tr2        | (0, 0, 255)     |
| Tr3        | (53, 37, 20)    |
| Tr4        | (255, 255, 0)   |
| Tr5        | (0, 255, 0)     |
| Tr6        | (153, 102, 0)   |
| Tr7        | (171, 59, 214)  |
| Tr8        | (255, 255, 255) |
| Tr9        | (255, 153, 0)   |
| Tr10       | (54, 226, 170)  |
| Tr11       | (39, 92, 74)    |
| Tr12       | (125, 35, 28)   |
| Tr13       | (243, 131, 129) |
| Tr14       | (255, 0, 153)   |
| Tr15       | (182, 161, 133) |
| Tr16       | (194, 253, 0)   |


identifier2color = {
    "Tr1": (204, 0, 0),
    "Tr2": (0, 0, 255),
    "Tr3": (53, 37, 20),
    "Tr4": (255, 255, 0),
    "Tr5": (0, 255, 0),
    "Tr6": (153, 102, 0),
    "Tr7": (171, 59, 214),
    "Tr8": (255, 255, 255),
    "Tr9": (255, 153, 0),
    "Tr10": (54, 226, 170),
    "Tr11": (39, 92, 74),
    "Tr12": (125, 35, 28),
    "Tr13": (243, 131, 129),
    "Tr14": (255, 0, 153),
    "Tr15": (182, 161, 133),
    "Tr16": (194, 253, 0)
}

## Format for saving tech development
The current technological development of any given player can be saved in a 5-digit number with the following format.
When no technology is unlocked, we start at 00000. Each position corresponds to a a branch of the tech tree, with the first being the "Organisation" branch and the rest following a clockwise order. The number at a position becomes 1 if only the first tech of the corresponding branch is unlocked. For example: 10010 would mean the player unlocked "Organisation" and "Hunting".
 
After the first tech on a branch, one adds +3 to the branch number for each further tech on the counterclockwise path and +1 one for each tech on the clockwise path. This gives a unique 5-digit number for every possible tech combination, where 99999 means everything is unlocked.

