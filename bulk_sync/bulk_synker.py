import pandas as pd
import os
import subprocess
import logging

logger = logging.getLogger(__name__)


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

    def _process_target(self, row) -> str:
        raw_target = row["raw_target"]
        src = row["src"]
        if not raw_target or str(raw_target) == "nan":
            prefix = self._add_user_dir(self.default_target)
            # remove left / from the src so that it isn't treated
            # as absolute path
            return os.path.join(prefix, src.lstrip("/"))
        else:
            return self._add_user_dir(raw_target)

    def load_db(self, filename: str) -> None:
        # load a csv file in the format of
        # source,destinationaction='store_true'
        try:
            df = pd.read_csv(filename, header=None)
            df.columns = ["raw_src", "raw_target"]
            df["src"] = df.raw_src.apply(self._process_path)
            df["target"] = df.apply(self._process_target, axis=1)
            self.db = df[["src", "target"]]
        except Exception as _e:
            logger.exception("Failed to load file: ", _e.__class__)
            self.db = None

    def validate_row(self, src) -> bool:
        # Validate a single pair of src and target directory
        if not os.path.exists(src):
            logger.warning(f"Source path {src} does not exist!")
            return False
        else:
            return True

    def validate(self, db) -> tuple:
        # Validate the input file before running the sync job.
        if db is None:
            logger.warning("no db")
            return None, 0, 0
        total = db.shape[0]
        db["is_valid"] = db["src"].apply(self.validate_row)
        valid_count = db.is_valid.sum()
        if valid_count < db.shape[0]:
            logger.warning(
                f"{valid_count} out of {db.shape[0]} rows have valid source path"
            )
        else:
            logger.info(f"All {db.shape[0]} rows have valid source path")

        db = db[db.is_valid]
        if db is not None and db.shape[0] > 0:
            db = db[["src", "target"]]
        else:
            db = None
        return db, valid_count, total

    def sync(self, src: str, target: str, dryrun: bool = True) -> int:
        # use self.assertNotInubprocess to call rsync on src -> dest
        cmd = ["rsync", "-avP", "--mkpath", src, target]
        if dryrun:
            cmd.append("--dry-run")
        try:
            result = subprocess.run(cmd)
            logger.info(result.stdout)
            return result.returncode
        except Exception as e:
            logger.exception("Sync command failed with ", e.__class__)
            return -1

    def syncall(self, dryrun: bool = True) -> None:
        # sync all paths. Instead of mapping, I want to go
        # line by line, so that the stdouts aren't mixed up
        succeed_cnt = 0
        if self.db is None:
            logger.warning("No valid input")
        else:
            for _, row in self.db.iterrows():
                result = self.sync(row["src"], row["target"], dryrun=dryrun)
                if result == 0:
                    succeed_cnt += 1
            logger.info(f"{succeed_cnt} jobs succeeded out of {self.db.shape[0]} jobs")
