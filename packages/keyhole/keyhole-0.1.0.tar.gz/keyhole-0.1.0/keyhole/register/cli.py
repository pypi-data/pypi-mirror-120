import json
import logging
from pathlib import Path

import numpy as np

from .coregister import coregister_all


log = logging.getLogger("cast.keyhole.coregister")


def config_parser(parser):

    parser.add_argument(
        "panels",
        metavar="panel_file",
        nargs="+",
        type=Path,
        help="Panel image files from one or more images.",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="JSON file to write with coregistration transforms.",
    )

    parser.add_argument(
        "--kh",
        choices=["4A", "9"],
        help="Type of satellite images. If omitted, the program will guess.",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Increase verbosity; mainly used for debugging.",
    )


def cli(args):

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    if args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    all_tforms = coregister_all(args.panels)
    with open(args.output, "w") as json_file:
        json.dump(all_tforms, json_file, indent=4, cls=NumpyEncoder)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
