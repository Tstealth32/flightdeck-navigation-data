# Flightdeck navigation downloads

## Download a database

| Pack | Download | Coverage |
| --- | --- | --- |
| USA — FAA AIRAC 2610 | [Download USA .navdb](https://github.com/Tstealth32/flightdeck-navigation-data/releases/download/faa-2610/flightdeck-faa-2610.navdb) | FAA airports, fixes, airways and available procedures; U.S. and included territories |
| Europe — airport reference only | [Download Europe .navdb — 1.88 MiB](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/flightdeck-europe-reference-20261016.navdb) | 1,896 ICAO airports, 4,329 runway ends; includes the Spain subset |
| Spain — airport reference only | [Download Spain .navdb — 156 KiB](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/flightdeck-spain-reference-20261016.navdb) | 74 ICAO airports, 170 runway ends, including the Canary Islands |

**Europe and Spain are airport/runway reference snapshots, NOT full AIRAC navigation databases. They contain no SIDs, STARs, approaches, waypoints, navaids or airways.** They cannot resolve a full IFR route. Do not buy an upgrade expecting European procedures from these files. Spain is a smaller alternative to Europe; downloading both is unnecessary.

The open reference source snapshot is October 16, 2026. It is community data, not certified or guaranteed current. Its REF cycle and one-day source date interval do not represent AIRAC validity; an expired-date indicator is expected. Unknown magnetic courses and transition altitudes remain unavailable. True headings are stored separately and never relabeled magnetic.

## Install in the Android development app

1. Download the `.navdb` file directly on your device. Do not rename a CSV/XML/ZIP to `.navdb`.
2. Open MCDU → Install / switch USA or Europe → Europe → Import Europe .navdb file, and select the file from Downloads.
3. After verification, select **Use Europe database** while parked/preflight. The selected pack name identifies Europe or Spain. Spain uses the same Europe slot, replacing the previously staged Europe alternative. USA stays saved separately.

Importing stages a file; selecting activates it. Database activation clears FMGC flight-plan/init/performance data and retains AOC records. These reference files do not populate missing procedures.

**The current public Play Store build does not offer European file import.** These files are for the compatible Android development build. Hosting them does not update the store app or enable a new in-app downloader. Keep your existing procedure pack unless you intentionally want the smaller reference-only alternative.

## Integrity and source

- [SHA-256 checksums](https://raw.githubusercontent.com/Tstealth32/flightdeck-navigation-data/main/reference/20261016/SHA256SUMS.txt)
- [Pack manifests and catalog](reference/20261016/catalog.json)
- [Source URLs, pinned commit and source hashes](reference/20261016/SOURCES.json)
- [OurAirports public-domain license](reference/20261016/OurAirports-LICENSE.txt)
- [Reproducible reference-pack builder](tools/build-open-reference-packs.py)
- [Original FAA notices](https://github.com/Tstealth32/flightdeck-navigation-data/releases/download/faa-2610/FAA-notices-2610.zip)

OurAirports permits commercial/noncommercial copying and redistribution under the Unlicense. Only its openly licensed airport and runway data are in these reference files. No NATS or ENAIRE evaluation data is mirrored here. The separate private UK/Spain evaluation file is incomplete and has not been cleared for public redistribution; these reference downloads do not claim to replace its terminal procedures.

For simulator practice only. No application source, user account data, signing keys, or proprietary navigation databases are hosted here.
