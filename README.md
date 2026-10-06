# PolyAnalytics
Applying some statistical methods to discover patterns in Polytopia 1v1 replays.

**Status: paused.** The replay IDs in `data/1v1replays.csv` are no longer valid, so no new games can be opened. The pipeline collected one batch of 10 games (`code/collected_data/Batch1.csv`).

Quick access:
- [general notes](./plan/general_notes.md)
- [potential next steps](./plan/potential_next_steps.md)
- [replay controls and pixel coordinates](./plan/replay_controls_and_coordinates.md)

## How it works
The scripts automate the game itself: a replay is opened through Steam (`steam://run/874390//opengame?id=<ID>`), the scripts send mouse and keyboard inputs, take screenshots and read pixel colours at fixed coordinates (window size 800x500) plus a bit of OCR. Per game this collects map type and size, both tribes, whether it is a 1v1, and the winner (see [general notes](./plan/general_notes.md) for tribe identifiers and the tech encoding). The colour detection is fragile by design: it depends on exact window sizes and on the game's current UI.

- `code/dataCollection.py` - collection on macOS (Polytopia window open on screen)
- `code/run_poly_fixed.py` - collection on Linux in a virtual display (`pyvirtualdisplay`, software rendering)
- `code/imageProcessing.py`, `code/colorProcessing.py` - screenshot analysis
- `code/dataHandling.py` - splits the ID list into batches of 10 (`data/out.csv`, one batch per row)
- `code/MacOS_specific/`, `code/Linux-specific/` - window handling and input emulation per OS

## Libraries you need
### general
- numpy
- pandas
- Pillow
- pytesseract (plus the [tesseract](https://github.com/tesseract-ocr/tesseract) binary)
### macOS
- pyobjc (Quartz, AppKit)
- pywinctl
### Linux
- pyvirtualdisplay
- pyscreenshot
- psutil
- evdev (preferred, see `code/Linux-specific/setup_uinput.sh`) or pynput as fallback
