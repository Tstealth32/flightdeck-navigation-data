# Flightdeck navigation downloads

## Download a database

| Pack | Download | Coverage |
| --- | --- | --- |
| USA — FAA AIRAC 2610 | [Download USA .navdb](https://github.com/Tstealth32/flightdeck-navigation-data/releases/download/faa-2610/flightdeck-faa-2610.navdb) | FAA airports, fixes, airways and available procedures; U.S. and included territories |
| Europe — airport reference only | [Download Europe .navdb — 1.88 MiB](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/flightdeck-europe-reference-20261016.navdb) | 1,896 ICAO airports, 4,329 runway ends; includes the Spain subset |
| Spain — airport reference only | [Download Spain .navdb — 156 KiB](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/flightdeck-spain-reference-20261016.navdb) | 74 ICAO airports, 170 runway ends, including the Canary Islands |
| India — airport reference only | [Download India .navdb — 248 KiB](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/flightdeck-india-reference-20261016.navdb) | 180 ICAO airports, 370 runway ends |

**Europe, Spain and India are airport/runway reference snapshots, NOT full AIRAC navigation databases. They contain no SIDs, STARs, approaches, waypoints, navaids or airways.** They cannot resolve a full IFR route. Do not buy an upgrade expecting procedures from these files. Spain is a smaller alternative to Europe; downloading both is unnecessary.

The open reference source snapshot is October 16, 2026. It is community data, not certified or guaranteed current. Its REF cycle and one-day source date interval do not represent AIRAC validity; an expired-date indicator is expected. Unknown magnetic courses and transition altitudes remain unavailable. True headings are stored separately and never relabeled magnetic.

## Install in the Android development app

1. Download the `.navdb` file directly on your device. Do not rename a CSV/XML/ZIP to `.navdb`.
2. Open MCDU → Regions and databases, then import the file from Downloads on a compatible development build.
3. After verification, select the matching region while parked/preflight. Spain uses the Europe slot; India has a separate slot. USA stays saved separately.

Importing stages a file; selecting activates it. Database activation clears FMGC flight-plan/init/performance data and retains AOC records. These reference files do not populate missing procedures.

**Hosting these files does not update an installed app.** A compatible app version is required to select India. Keep your existing procedure pack unless you intentionally want a reference-only alternative.

## Integrity and source

- [SHA-256 checksums](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/SHA256SUMS.txt)
- [Pack manifests and catalog](reference/20261016/catalog.json)
- [Source URLs, pinned commit and source hashes](reference/20261016/SOURCES.json)
- [OurAirports public-domain license](reference/20261016/OurAirports-LICENSE.txt)
- [Reproducible reference-pack builder](tools/build-open-reference-packs.py)
- [Original FAA notices](https://github.com/Tstealth32/flightdeck-navigation-data/releases/download/faa-2610/FAA-notices-2610.zip)

OurAirports permits commercial/noncommercial copying and redistribution under the Unlicense. Only its openly licensed airport and runway data are in these reference files. No NATS or ENAIRE evaluation data is mirrored here. The separate private UK/Spain evaluation file is incomplete and has not been cleared for public redistribution; these reference downloads do not claim to replace its terminal procedures.

For simulator practice only. No application source, user account data, signing keys, or proprietary navigation databases are hosted here.
