# Potential next steps
This file contains a semi ordered collection of things we might want to do at some point.

## Algorythms / Things we'll need to be able to do
- [ ] Open replay in Polytopia from ID *
- [ ] Get access to screen for further processing *
- [ ] Get access to mouse and keyboard inputs *
- [ ] detect when new turn begins *
- [ ] identify tribes playing *
- [ ] detect who won
- [ ] detect map type
- [ ] detect map size
- [ ] detect stars added per turn
- [ ] detect stars spent per turn
- [ ] detect technologies unlocked so far *
- [ ] detect achievements discovered and completed

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

Tech development should be saved in form of a 10-digit number according to the format presented in general-notes.


