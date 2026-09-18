# PokeHex

A Python-native save file editor for *Pokémon Legends: Z-A*, in the same spirit as [PKHeX](https://github.com/kwsch/PKHeX): edit boxed Pokémon directly in an exported save file, with a Tkinter GUI.

## How it actually works

Nintendo doesn't expose any official way to read or write Switch save data. The only path in is a Switch running Atmosphère CFW, using a homebrew save manager (Checkpoint or JKSV) to export the raw save file to the SD card. The workflow is:

1. On your CFW Switch, use Checkpoint/JKSV to export the Legends: Z-A save to the SD card.
2. Copy that save file to your Mac.
3. Edit it with PokeHex (GUI or the `pokehex.za` library directly).
4. Copy the edited file back and re-import it with the same save manager.

PokeHex never talks to the console live — no network, no `sys-botbase`, no game has to be running. That's a deliberate simplification over an earlier live-memory-injection design; see git history if you want that instead.

## Scope, honestly

This ports the specific pieces needed to read/write Legends Z-A's save format, by reading PKHeX.Core's own source (GPL-3.0) and re-implementing the structures in Python — not by guessing:

- `pokehex.za.crypto` — the PA9 entity encryption (block-shuffle + LCG stream cipher).
- `pokehex.za.pa9` — the `PA9` Pokémon entity format (species, stats, IVs/EVs, moves, OT info, etc).
- `pokehex.za.swishcrypto` — the save file's block-based container format (`SCBlock`/xorshift keystream/SHA-256 integrity hash).
- `pokehex.za.save` — box layout on top of that (32 boxes × 30 slots) and load/save.
- `pokehex.gui` — a Tkinter GUI over all of the above.

**What's known to be incomplete or unverified:**

- **Species internal↔national ID mapping is not ported.** PKHeX maintains a separate table for this; some species will get written with the wrong internal ID until that table is ported.
- **No legality checker.** Nothing stops you from writing an impossible IV/EV/move/ability combination. PKHeX's real legality checker is thousands of edge cases deep; we have none of it. Illegal data is a known way to trigger crashes/error screens that look like corruption.
- **Never validated against a real save file.** Every test in this repo is a round-trip test against our own encode/decode (56 passing) — that proves internal consistency, not that it matches what the actual game expects on disk. The first real test is loading an actual exported Legends Z-A save.
- Ribbons, marks, and TM record flags are left zeroed (cosmetic, not required for a Pokémon to exist).

## Safety

- **Always back up your save before testing.** The GUI's in-place "Save" makes a `.bak` copy automatically, but keep your own copy elsewhere too — this is unproven software touching your only save file.
- Test with a copy of your save first, not your only one. Confirm the Switch actually loads a PokeHex-written save before trusting it with anything you'd be upset to lose.
- Using edited save data online (trading, battling, GTS) risks a ban under Nintendo's ToS. This tool is for offline/personal use.

## Layout

```
src/pokehex/
  pokemon.py       # Generic, format-agnostic Pokemon dataclass (unused by the save-editing path)
  gui.py           # Tkinter GUI: open a save, browse boxes, edit/add Pokemon, save
  sysbot/          # sys-botbase TCP client (leftover from the earlier live-injection design; unused by the GUI)
  za/
    crypto.py       # PA9 entity encryption
    pa9.py          # PA9 Pokemon entity: field accessors, encode/decode
    swishcrypto.py  # Save file container format (SCBlock)
    save.py         # SAV9ZA: box read/write, load/save a save file
tests/
```

## Running the GUI

```
pip install -e .
pokehex-gui
# or: python -m pokehex.gui
```

Requires Tkinter. On Homebrew Python, install the matching formula first (e.g. `brew install python-tk@3.14`).

## Requirements

- Python 3.11+
- A Switch running Atmosphère CFW with a save manager (Checkpoint/JKSV), to get the save file on and off the SD card. PokeHex itself only ever touches the file on your Mac.

## Disclaimer

Editing save data outside of normal gameplay is against Nintendo's Terms of Service. This project is for offline/personal, educational use.
