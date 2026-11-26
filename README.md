# Super Mario Odyssey - Archipelago Mod
A mod adding Archipelago Multi World support to Super Mario Odyssey.
WARNING: This mod only works on version 1.0.0 of Super Mario Odyssey.

## Features
- Randomize Power Moons
- Randomize Captures
- Supports all non-achievement (Toadette Moon) power moon locations.
- Supports all outfits, stickers, and souvenirs.
- Choose which kingdom is your win condition.

## Installation and Usage
* Install the latest version from the releases page. `smo.apworld` and either `SMO_Archipelago_Vx.x_Switch.zip` for console or `SMO_Archipelago_Vx.x_Emu.zip` for emulator.
* Place `smo.apworld` in the `custom_worlds` folder of your Archipelago install which the default directory is `C:\ProgramData\Archipelago\custom_worlds`

<details>
<summary>Switch</summary> 
  
- Extract `SMO_Archipelago_Vx.x_Switch.zip` and Place the `atmosphere` folder onto the root of your sd card.

</details>

<details>
<summary>Emulator</summary>

### Ryujinx and forks 
- Extract `SMO_Archipelago_Vx.x_Emu.zip` and Place `SMOAP` folder in the mods directory for Super Mario Odyssey.

### Suyu and other Yuzu forks
- Right Click on Super Mario Odyssey in the game menu and select `Open Mod Data Location`.
- Extract `SMO_Archipelago_Vx.x_Emu.zip` and Place `SMOAP` folder in the mods directory that opened.
</details>

### Connecting to the Connector from Super Mario Odyssey.
- When prompted, the `IP Address` you are connecting to is your computer's local ipv4 this is found by entering the `ipconfig` command into command prompt on Windows.
- When prompted, the `Port` is `1027` by default which does not need to be changed.

Credits
- [Sanae](https://github.com/sanae6) Author of original server code
- [CraftyBoss](https://github.com/CraftyBoss) Author of SMO Online
- All other contributors to the aforementioned repos.

## Experimental, seed-randomized early kingdoms

This is a development option, not a released or emulator-verified build.
Use the APWorld, Windows connector, and game mod from **the same commit**.
The upstream connector/mod will not honor the shuffled order.

```yaml
name: OdysseyTest
game: Super Mario Odyssey
Super Mario Odyssey:
  goal: moon
  extra_moons: some
  early_kingdom_order: shuffle
```

The seed independently shuffles **Cascade, Sand and Lake** after Cap and
before Wooded, for six possible sequences (including the normal order).
The same seed uses the same order; different seeds can coincidentally repeat.
Wooded and later story progression stay in their normal order. The selected
route is recorded in slot data and the spoiler. The game uses the same order
from the connector rather than rolling its own. The default `vanilla` option
retains the original graph and the original slot packet size.

The experimental option currently requires a Metro or later goal. Random
moon requirements and capture randomization are not supported with the
experimental option. The shuffle uses the departing kingdom's normal quota
(Cascade 5, Sand 16, Lake 8 if it has another early kingdom after it).
Cascade still uses its story-clear region. Lake followed by Wooded preserves
the existing no-extra-gate graph edge; the later Cloud gate is unchanged.
Revisit checks are kept after the early route in the APWorld.

### Playtest checklist

- Use Odyssey **1.0.0**, a new save per route, and join a fresh AP room
  **before leaving Cap**. Don't reuse a save across rooms.
- For all six permutations, compare the actual first visit to the route in
  the spoiler. Test Sand's native Lake/Wooded choice and Lake's exit in
  particular: the draft only hooks story departures, and the map UI,
  first-visit flags, and actual gate behavior need in-game validation.
- Confirm non-route transports (shop doors, subareas, ordinary revisits),
  that Cloud cannot be skipped to early, and that the later Cloud gate still
  works. Check both sides of each quota and a reconnect after save/resume.
- Check cross-game item delivery in both directions in a disposable room.
  Do not publish this as a stable APWorld or add it to a shared Hero catalog
  until the game-mod checks pass.

`python -m unittest discover -s tests` tests route selection and packet encoding.
`g++ -std=c++17 -I Mod/include tests/early_kingdom_route.cpp -o /tmp/early_kingdom_route && /tmp/early_kingdom_route`
tests the pure routing code, not the Switch integration. A full mod link still
needs devkitA64 and the Odyssey 1.0.0 symbol map; the repo contains only a stub.
