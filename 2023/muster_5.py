#!/usr/bin/env python3

import re
import sys
import os
from typing import TextIO

Map = list[tuple[int, int, int]]

def parse_input(f: TextIO) -> tuple[list[int], list[Map]]:
  seeds = []
  maps = []

  for line in (r.strip() for r in f.readlines()):
    if line.startswith("seeds: "):
      seeds = [int(x) for x in line[7:].split()]
    elif re.match(r'^[^-]+-to-[^-]+\s', line):
      maps.append([])
    elif line:
      dest, src, dist = (int(x) for x in line.split())
      maps[-1].append((src, dest, dist))

  for mapping in maps:
    mapping.sort()

  return seeds, maps

def lowest_location(seeds: list[int], maps: list[Map]) -> int:
  locations = []

  for seed in seeds:
    for mapping in maps:
      for src, dest, dist in mapping:
        if seed >= src and seed < src + dist:
          seed = dest + (seed - src)
          break

    locations.append(seed)

  return min(locations)

def lowest_range_location(seeds: list[int], maps: list[Map]) -> int:
  lowest_locations = []

  for start, length in zip(*[iter(seeds)] * 2):
    src_ranges = [(start, start + length - 1)]
    dst_ranges = []

    for mapping in maps:
      for lo, hi in src_ranges:
        for src, dest, dist in mapping:

          # entire source range is less than any mapping
          # pass through source range as destination range
          if hi < src:
            dst_ranges.append((lo, hi))
            break

          # source range is contained within this range
          elif lo >= src and lo < src + dist:

            # the end of the source range is past this range
            # add a destination range for the part within this range
            # and continue processing the rest of the source range
            if hi >= src + dist:
              dst_ranges.append((dest + (lo - src), dest + dist - 1))
              lo = src + dist

            # the source range is wholly contained within this range
            # map the entire range as the destination range
            else:
              dst_ranges.append((dest + (lo - src), dest + (hi - src)))
              break

          # part of the source range is less than any mapping
          # add a destination range passing through the part not in a mapping
          # and continue processing for the rest of the source range
          elif lo < src and hi >= src:
            dst_ranges.append((lo, src - 1))
            lo = src

        # the source range was not contained within any mapping
        # pass through the source range as the destination range
        else:
          dst_ranges.append((lo, hi))

      # results of one mapping become the ranges for the next
      src_ranges = dst_ranges
      dst_ranges = []

    # find the lowest result out of all the final ranges
    lowest_locations.append(min(lo for lo, _ in src_ranges))

  return min(lowest_locations)

def run() -> None:
  

  HERE = os.path.abspath(os.path.dirname(__file__))
  with open(os.path.join(HERE,'input_5.txt')) as f:
     seeds, maps = parse_input(f)

  lowest = lowest_location(seeds, maps)
  lowest_range = lowest_range_location(seeds, maps)

  print(f"Lowest location: {lowest}")
  print(f"Lowest range-based location: {lowest_range}")

if __name__ == '__main__':
  run()
  sys.exit(0)