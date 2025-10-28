# Potential next steps
This file contains a semi ordered collection of things we might want to do at some point.

## Algorythms / Things we'll need to be able to do
Due to the time consuming matter of working through a replay, in the best case all relevant data should be extracted out of a replay in one go.
- [ ] Open replay in Polytopia from ID *
- [ ] Get access to screen for further processing *
- [ ] Get access to mouse and keyboard inputs *
- [ ] Detect when new turn begins *
- [ ] Identify tribes playing *
- [ ] Detect who won
- [ ] Detect map type
- [ ] Detect map size
- [ ] Detect stars added per turn
- [ ] Detect stars spent per turn
- [ ] Detect technologies unlocked so far *
- [ ] Detect achievements discovered and completed
- [ ] Get a way to analyse multiple replays at once

## Ways to structure the data 
It may be worth considering to split the List of IDs and every subsequent file into 10 files each containing 1_000 IDs to facilitate processing.
### replay_overview_X.csv


| ID  | TribeA | TribeB | Winner | TurnsTotal | mType | mSize |
| --- | ------ | ------ | ------ | ---------- | ----- | ----- |

### tech_deveolopment_X.csv

| Turn | ID1-A | ID1-B | ID2-A | ID2-B | ID3-A | ... |
| ---- | ----- | ----- | ----- | ----- | ----- | --- |
| 1    |       |       |       |       |       |     |
| 2    |       |       |       |       |       |     |
| ...  |       |       |       |       |       |     |

Tech development should be saved in form of a 5-digit number according to the format presented in general-notes.


