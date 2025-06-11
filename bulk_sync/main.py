from bulk_synker import BulkSynker
import argparse


def main():
    epi = """bulk_synker csv_file_name [-v]
    """
    parser = argparse.ArgumentParser(
        description="A simple tool to rsync all pairs of src-target paths stored in a single csv file",
        epilog=epi,
    )
    parser.add_argument(
        "csv", type=str, help="csv input file that contains all pairs of src, dest"
    )
    parser.add_argument("default_target", type=str, help="Default target path")

    args = parser.parse_args()
    csv_file = args.csv
    default_target = args.default_target
    synker = BulkSynker(csv_file, default_target)
    print(synker.get_db())
    # print(synker.syncall())


if __name__ == "__main__":
    main()

