# bulk_sync

## Dependency

rsync

## Usage

In the project root where `pyproject.toml` lives, run the following to install:

`pip install .`

This will install a script together with this package.

You need to create a file to store all src-target pairs to run rsync on. A example
file looks like,

```
~/.config,~/Dropbox/Linux/
/etc/nanorc,
/usr/share/nano/light,
/etc/fstab,
```

Note that some of the rows don't have a target. A default target root is needed
to handle this. The src will be appended to the default target root to generate
the final target path.

With all this, run

```
bulk_synker <db file name> <default target path> [--dryrun]
```

I recommend doing a dryrun before actual execution. Example:

```
bulk_synker ~/syncall_list.csv ~/Dropbox/Linux --dry
```

This runs the rsync dryrun.

Additionally, I set up a cron job to execute the following script

```
bulk_synker ~/syncall_list.csv ~/Dropbox/Linux > ~/log/synk.log
```

## testing

```
coverage run -m unittest discover
coverage report
```
