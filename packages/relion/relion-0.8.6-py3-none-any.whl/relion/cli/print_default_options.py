import argparse

from relion.cryolo_relion_it import dls_options
from relion.cryolo_relion_it.cryolo_relion_it import RelionItOptions


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        help="Print options to file. Default is relion_it_options.py. Extension should be .py",
        dest="options_file",
        default="relion_it_options.py",
    )
    args = parser.parse_args()
    opts = RelionItOptions()
    opts.update_from(vars(dls_options))
    opts.print_options(out_file=open(args.options_file, "w"))
