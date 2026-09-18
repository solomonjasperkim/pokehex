# PokeHex

A Python-native reimplementation of a small slice of what [PKHeX](https://github.com/kwsch/PKHeX) / [SysBot.NET](https://github.com/kwsch/SysBot.NET) do, aimed at *Pokémon Legends: Z-A*.

## Scope, honestly

PKHeX.Core represents years of community reverse-engineering across every mainline Pokémon game — save formats, per-game encryption/checksums, personal stat tables, and a legality checker with thousands of edge cases. This project does **not** attempt to replace that. It's scoped to:

1. A game-agnostic in-memory representation of a single Pokémon's data (`pokehex.pokemon.Pokemon`).
2. A client for the [`sys-botbase`](https://github.com/olliz0r/sys-botbase) protocol used to read/write a running Switch's memory over the local network (`pokehex.sysbot`).
3. (Future) Encoding/decoding to and from Legends Z-A's actual in-memory Pokémon format — this depends on reverse-engineered offsets that are still evolving upstream in PKHeX.Core as of late 2026, and is the hard, unsolved part of this project.
4. (Future) A Discord bot frontend once (1)-(3) work end to end.

If you just want a working trade bot today, [SysBot.NET](https://github.com/kwsch/SysBot.NET) already supports Legends Z-A out of the box — this repo exists to build the same thing natively in Python, not because the C# version is missing something.

## Status

Early scaffold. Data model and sys-botbase client are usable; Z-A-specific binary encoding is not implemented yet.

## Layout

```
src/pokehex/
  pokemon.py      # Game-agnostic Pokemon dataclass
  sysbot/
    client.py      # TCP client for the sys-botbase protocol
tests/
```

## Requirements

- Python 3.11+
- A Switch running Atmosphère CFW with `sys-botbase` installed, reachable over local Wi-Fi, for anything involving live memory access.

## Disclaimer

Editing or injecting Pokémon data outside of normal gameplay is against Nintendo's Terms of Service. Using edited Pokémon in any online-connected mode (trading, battling, GTS) risks an account ban. This project is for offline/personal use and educational purposes.
