#!/bin/env python
import csv
import re
import shutil
import sys
from collections import defaultdict
from os import environ, walk
from os.path import getsize, join, realpath
from pathlib import Path

import acoustid


def sort_music(source_folder, target_folder):
    for root_folder, folder_names, file_names in walk(source_folder):
        for file_index, file_name in enumerate(file_names, 1):
            source_path = join(root_folder, file_name)
            if not getsize(source_path):  # Skip empty files
                continue
            target_path = get_target_path(source_path)
            print(f'{target_path=}')
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source_path, target_path)
            # shutil.copy2(source_path, target_path)
            print()


def get_target_path(source_path):
    source_path = Path(source_path)
    print(f'{source_path=}')
    suffix = source_path.suffix.lower()
    assert len(suffix) < 6
    size = source_path.stat().st_size
    matches = get_matches(source_path)
    for score, recording_id, title, artist in matches:
        print(f'{score}\t{recording_id}\t{title}\t{artist}')
    if matches:
        match = sorted(matches, key=lambda _: -_[0])[0]
        score, recording_id, title, artist = match
        target_name = (
            f'{format_artist(artist)} - '
            f'{format_title(title)} '
            f'[size={size};score={score:.5f}]{suffix}')
        paths_by_key[(artist, title)].add(target_name)
    if not matches or title is None or artist is None:
        source_stem = stamp_pattern.sub('', source_path.stem)
        target_name = f'{source_stem} [size={size}]{suffix}'
    print(target_name)
    return Path(target_folder) / target_name.replace('/', '-')


def get_matches(source_path):
    while True:
        try:
            matches = list(acoustid.match(api_key, source_path))
        except (
            acoustid.WebServiceError,
            acoustid.FingerprintGenerationError,
        ) as e:
            print(f'{e} ! {source_path}')
            matches = []
            break
        except OSError as e:
            sys.exit(e)
        else:
            break
    return matches


def format_artist(x):
    return x[:MAXIMUM_ARTIST_LENGTH].strip() if x else 'UNKNOWN'


def format_title(x):
    return x[:MAXIMUM_TITLE_LENGTH].strip() if x else 'UNKNOWN'


environ['FPCALC'] = '/usr/bin/fpcalc'
api_key = environ['ACOUSTID_KEY']
stamp_pattern = re.compile(r' \[size=.*\]')
paths_by_key = defaultdict(set)


MAXIMUM_ARTIST_LENGTH = 64
MAXIMUM_TITLE_LENGTH = 128


if __name__ == '__main__':
    source_folder, target_folder = sys.argv[1:]
    if realpath(source_folder) == realpath(target_folder):
        sys.exit('Source and target folders must be different')
    try:
        sort_music(source_folder, target_folder)
    except KeyboardInterrupt:
        pass
    key_count_packs = [(k, len(ps)) for k, ps in paths_by_key.items()]
    key_count_packs = sorted(key_count_packs, key=lambda _: -_[1])
    summary_path = Path(target_folder) / 'tracks.csv'
    with summary_path.open('at') as f:
        csv_writer = csv.writer(f)
        for key, count in key_count_packs:
            csv_writer.writerow([key[0], key[1], count])
    print(f'\nsummary_path = {summary_path}')
