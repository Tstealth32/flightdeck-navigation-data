#!/usr/bin/env python3
"""Build redistributable Europe/Spain airport references, never AIRAC procedures.

Only reads the pinned OurAirports CSV snapshot and license in --sources. Unknown
magnetic courses/transition altitudes remain null. No NATS/ENAIRE data is used.
"""
import argparse
import collections
import csv
import datetime
import hashlib
import json
import math
import re
import shutil
import sqlite3
from pathlib import Path


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def position(row, prefix=''):
    lat, lon = (number(row[prefix + field]) for field in ('latitude_deg', 'longitude_deg'))
    return dict(lat=lat, lon=lon) if lat is not None and lon is not None and abs(lat) <= 90 and abs(lon) <= 180 else dict(lat=None, lon=None)


def build(sources, output):
    origin = json.loads((sources / 'sources.json').read_text())
    for item in origin['files']:
        assert hashlib.sha256((sources / item['file']).read_bytes()).hexdigest() == item['sha256'], item['file']
    assert origin['repository'] == 'https://github.com/davidmegginson/ourairports-data'
    assert 'public domain' in (sources / 'LICENSE').read_text().lower()
    output.mkdir(parents=True, exist_ok=True)
    candidates = collections.defaultdict(list)
    for row in csv.DictReader((sources / 'airports.csv').open()):
        if row['type'] not in ('large_airport', 'medium_airport', 'small_airport'):
            continue
        if row['continent'] != 'EU' and row['iso_country'] != 'ES':
            continue
        ident = row['icao_code']
        # ICAO-only: do not silently fabricate airport codes from local identifiers.
        if not re.fullmatch('[A-Z]{4}', ident):
            continue
        p = position(row)
        if p['lat'] is None:
            continue
        candidates[ident].append((row, p))
    airports, refs = {}, {}
    ambiguous = sorted(ident for ident, entries in candidates.items() if len(entries) != 1)
    for ident, entries in sorted(candidates.items()):
        if len(entries) != 1:
            continue
        row, p = entries[0]
        airport = dict(key=ident, ident=ident, name=row['name'], region=row['iso_country'], **p,
                       elevation=number(row['elevation_ft']), transition=None, runways=[],
                       departures=[], arrivals=[], approaches=[], basicReference=True,
                       source='OurAirports public-domain airport/runway reference', sourceId=row['id'])
        airports[ident] = refs[row['ident']] = airport
    for row in csv.DictReader((sources / 'runways.csv').open()):
        airport, feet = refs.get(row['airport_ident']), number(row['length_ft'])
        if airport is None or row['closed'] == '1' or feet is None or feet <= 0:
            continue
        for end, opposite in [('le', 'he'), ('he', 'le')]:
            ident = row[end + '_ident'].upper()
            if not re.fullmatch('(0[1-9]|[12][0-9]|3[0-6])[LRC]?', ident):
                continue
            if any(r['ident'] == ident for r in airport['runways']):
                continue
            other = position(row, opposite + '_')
            airport['runways'].append(dict(ident=ident, length=round(feet * .3048, 3),
                elevation=number(row[end + '_elevation_ft']), course=None,
                headingTrue=number(row[end + '_heading_degT']), **position(row, end + '_'),
                oppositeIdent=row[opposite + '_ident'].upper(), oppositeLat=other['lat'],
                oppositeLon=other['lon'], sourceId=row['id']))
    results = []
    snapshot = origin['sourceCommitDate'][:10]
    for subset, title in [('europe', 'Europe'), ('spain', 'Spain')]:
        chosen = {k: v for k, v in airports.items() if subset == 'europe' or v['region'] == 'ES'}
        assert all(k in chosen for k in ['LEMD', 'LEBL', 'LEPA', 'GCLP', 'GCTS'])
        if subset == 'europe':
            assert 'EGLL' in chosen
        counts = dict(airports=len(chosen), waypoints=0, navaids=0, airways=0, routes=0, procedures=0)
        countries = dict(sorted(collections.Counter(a['region'] for a in chosen.values()).items()))
        coverage = (title + ' ICAO airport/runway reference, including Spanish Canary Islands. '
                    'No SID, STAR, approach, airway, waypoint, navaid or transition-altitude data. '
                    'Not an AIRAC navigation database; community snapshot for simulator reference only.')
        name = f'flightdeck-{subset}-reference-{snapshot.replace("-", "")}.navdb'
        target = output / name
        if target.exists():
            raise FileExistsError(target)
        # The current Android region library has USA and Europe slots. Spain is
        # an explicitly labeled smaller alternative for that same Europe slot.
        metadata = dict(schema=1, productId='flightdeck_navdata', name=title + ' — airport reference only',
            regionId='europe', subsetId=subset, cycle='REF-' + snapshot.replace('-', ''),
            validFrom=snapshot, validTo=(datetime.date.fromisoformat(snapshot) + datetime.timedelta(days=1)).isoformat(),
            validityKind='reference-snapshot-not-airac', snapshotDate=snapshot, coverage=coverage,
            supplier='OurAirports community', licenseReference='OurAirports Unlicense / public domain; see OurAirports-LICENSE.txt',
            referenceOnly=True, partialCoverage=True, personal=True, evaluation=False,
            airportCountries=countries, counts=counts, source=origin, ambiguousExcluded=ambiguous)
        with sqlite3.connect(target) as db:
            db.executescript('PRAGMA application_id=1179533654; PRAGMA user_version=1; CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);')
            for table in ['airports', 'waypoints', 'navaids', 'airways', 'routes']:
                db.execute(f'CREATE TABLE {table}(key TEXT PRIMARY KEY,ident TEXT NOT NULL,region TEXT NOT NULL,lat REAL,lon REAL,payload TEXT NOT NULL)')
                db.execute(f'CREATE INDEX {table}_ident ON {table}(ident,region)')
            db.execute('CREATE INDEX airports_geo ON airports(lat,lon)')
            db.execute('CREATE TABLE procedures(airport TEXT NOT NULL,kind TEXT NOT NULL,ident TEXT NOT NULL,payload TEXT NOT NULL,PRIMARY KEY(airport,kind,ident))')
            db.executemany('INSERT INTO airports VALUES(?,?,?,?,?,?)', [(k, k, a['region'], a['lat'], a['lon'], compact(a)) for k, a in chosen.items()])
            db.executemany('INSERT INTO metadata VALUES(?,?)', [(k, compact(v)) for k, v in metadata.items()])
            db.commit()
            db.execute('VACUUM')
            assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
            assert db.execute('PRAGMA application_id').fetchone()[0] == 0x464E4156
        manifest = dict(metadata, bytes=target.stat().st_size, sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                        file=name, runwayEnds=sum(len(a['runways']) for a in chosen.values()))
        (output / (name + '.manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
        results.append(manifest)
    shutil.copy2(sources / 'LICENSE', output / 'OurAirports-LICENSE.txt')
    (output / 'SOURCES.json').write_text(json.dumps(origin, indent=2) + '\n')
    (output / 'SHA256SUMS.txt').write_text(''.join(f'{x["sha256"]}  {x["file"]}\n' for x in results))
    (output / 'catalog.json').write_text(json.dumps(dict(referenceOnly=True, packs=results), indent=2) + '\n')
    print(json.dumps([dict(file=x['file'], bytes=x['bytes'], sha256=x['sha256'], airports=x['counts']['airports'], runwayEnds=x['runwayEnds']) for x in results], indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.sources, args.output)
