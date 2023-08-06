import csv
import sys

import fire
import geohash2


class TrieNode:
    def __init__(self):
        self.child = {}
        self.freq = 0

    def insert(self, s):
        curr = self
        for c in s:
            curr.child.setdefault(c, TrieNode())
            curr.child[c].freq += 1
            curr = curr.child[c]

    def find_shortest_prefix(self, geohash, curr_prefix=""):
        if len(geohash) == 0:
            return curr_prefix
        c = geohash[0]
        if self.child[c].freq == 1:
            return curr_prefix + c
        else:
            return self.child[c].find_shortest_prefix(geohash[1:], curr_prefix + c)


def fill_output(csv_reader, csv_writer, trie):
    csv_writer.writerow(("lat", "lng", "geohash", "uniq"))
    next(csv_reader)  # skip headers
    for row in csv_reader:
        lat, lng = float(row[0]), float(row[1])
        geohash = geohash2.encode(lat, lng)
        shortest_prefix = trie.find_shortest_prefix(geohash)
        csv_writer.writerow((lat, lng, geohash, shortest_prefix))


def transform(input_csv="example.csv", output_csv=None):
    trie = TrieNode()
    with open(input_csv) as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip headers
        for row in csv_reader:
            lat, lng = float(row[0]), float(row[1])
            geohash = geohash2.encode(lat, lng)
            trie.insert(geohash)
        f.seek(0)
        if output_csv:
            with open(output_csv, "w") as fw:
                csv_writer = csv.writer(fw)
                fill_output(csv_reader, csv_writer, trie)
        else:
            csv_writer = csv.writer(sys.stdout)
            fill_output(csv_reader, csv_writer, trie)


def main():
    fire.Fire(transform)


if __name__ == "__main__":
    main()
