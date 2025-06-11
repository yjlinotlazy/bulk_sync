import pandas as pd
import os
import subprocess


class BulkSynker:
    def __init__(self, csv_path, default_target):
        self.default_target = default_target
        self.load_db(csv_path)
        self.db, _, _ = self.validate(self.db)

    def _add_user_dir(self, path: str) -> str:
        home_path = os.path.expanduser("~")
        if "~" in path:
            return os.path.join(home_path, path.strip("~/"))
        return path

    def _process_path(self, path: str, is_target: bool = False) -> str:
        if not path or str(path) == "nan":
            if is_target:
                return self._add_user_dir(self.default_target)
            else:
                return path
        else:
            return self._add_user_dir(path)

    def get_db(self):
        return self.db

    def load_db(self, filename: str) -> None:
        # load a csv file in the format of
        # source,destination
        try:
            df = pd.read_csv(filename, header=None)
            df.columns = ["raw_src", "raw_target"]
            df["src"] = df.raw_src.apply(self._process_path)
            df["target"] = df.raw_target.apply(self._process_path, is_target=True)
            self.db = df[["src", "target"]]
        except Exception as _e:
            print("Failed to load file: ", _e.__class__)
            self.db = None

    def validate_row(self, src) -> bool:
        # Validate a single pair of src and target directory
        if not os.path.exists(src):
            print(f"Source path {src} does not exist!")
            return False
        else:
            return True

    def validate(self, db) -> tuple:
        # Validate the input file before running the sync job.
        if db is None:
            print("no db")
            return None, 0, 0
        total = db.shape[0]
        db["is_valid"] = db["src"].apply(self.validate_row)
        valid_count = db.is_valid.sum()
        if valid_count < db.shape[0]:
            print(f"{valid_count} out of {db.shape[0]} rows have valid source path")
        else:
            print(f"All {db.shape[0]} rows have valid source path")

        db = db[db.is_valid]
        if db is not None and db.shape[0] > 0:
            db = db[["src", "target"]]
        else:
            db = None
        return db, valid_count, total

    def sync(self, src: str, target: str) -> None:
        # use subprocess to call rsync on src -> dest
        pass

    def syncall(self) -> None:
        # sync all paths
        pass
