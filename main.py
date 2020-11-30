#!/bin/env python

from NOMADSExplorer import nomad
from NOMADSExplorer.explore import discovery

from argparse import ArgumentParser


def create_commandline_parser():
    parser = ArgumentParser("Add Description Here")
    parser.add_argument(
        "address",
        type=str,
        default="https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
        help="Where to find the National Water Model data"
    )
    parser.add_argument(
        "-o",
        metavar="path",
        default="nwm.gpkg",
        type=str,
        help="Where to save the output"
    )
    parser.add_argument(
        "-e",
        metavar="explorer_type",
        dest="explorer_type",
        choices=discovery.EXPLORERS.keys(),
        default="remote",
        type=str,
        help="The type of Netcdf explorer that will look for the data"
    )
    return parser


def main():
    parser = create_commandline_parser()
    parameters = parser.parse_args()
    searcher = nomad.Nomad(parameters.address, parameters.explorer_type)
    searcher.explore()
    print(searcher.catalog)


if __name__ == "__main__":
    main()
