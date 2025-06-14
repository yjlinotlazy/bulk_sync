from bulk_sync.bulk_synker import BulkSynker
import argparse


def main():
    epi = """bulk_synker <db file name> <default target path> [--dryrun]
    """
    parser = argparse.ArgumentParser(
        description="A simple tool to rsync all pairs of src-target paths stored in a single csv file",
        epilog=epi,
    )
    parser.add_argument(
        "csv", type=str, help="csv input file that contains all pairs of src, dest"
    )
    parser.add_argument(
        "default_target",
        type=str,
        help="Default target root path. If you don't specify the target, src will be appended to the default target root to generate a target path",
    )
    parser.add_argument("--dry", action="store_true", help="dryrun mode")
    args = parser.parse_args()
    csv_file = args.csv
    default_target = args.default_target
    dryrun = args.dry
    synker = BulkSynker(csv_file, default_target)
    synker.syncall(dryrun=dryrun)


if __name__ == "__main__":
    main()
