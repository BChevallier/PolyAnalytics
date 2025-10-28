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
    "Tr12": "Yadakk"
}

## Color values by tribe:
Each tribe has a distinct color value associated with it. This color can be seen in the territory borders (if there are no duplicate tribes in a game). It can also be seen in the circle in the top left corner while watching replays (which can be used for turn and tribe-detection).

| Identifier | Color    |
| ---------- | -------- |
| Tr1        ||
| Tr2        ||
| Tr3        ||
| Tr4        ||
| Tr5        ||
| Tr6        ||
| Tr7        ||
| Tr8        ||
| Tr9        ||
| Tr10       ||
| Tr11       ||
| Tr12       ||

identifier2tribe = {
    "Tr1": ,
    "Tr2": ,
    "Tr3": ,
    "Tr4": ,
    "Tr5": ,
    "Tr6": ,
    "Tr7": ,
    "Tr8": ,
    "Tr9": ,
    "Tr10": ,
    "Tr11": ,
    "Tr12": ,
}
