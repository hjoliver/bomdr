# POC workflow DR system.

## Current status

Sync workflow generated on-the-fly from a Jinja2-format config file, to trigger
sync tasks at specified sync checkpoints in a dummy model workflow (which has
tasks that check for the existence of their input files and write their output
files with `touch`).

The sync tasks currently just write what they would do, to stdout.

### TBD

- implement file sync
- implement remote database update
- implement script to start remote workflows from most recent sync checkpoints


## Instructions

Fork this repo on GitHub if you plan to contribute to it.

```
# check your environment:
$ cylc version
8.1.4

# clone your fork locally to to ~/cylc-src/bomdr, then:
$ cd ~/cylc-src/bomdr

# view the Jinja2-processed sync workflow config:
$ cylc view -j ./sync

# install, validate, and run the sync workflow:
$ cylc vip ./sync

# install, validate, and run the model1 workflow:
$ cylc vip ./model1

# check they're both running:
$ cylc scan

# monitor progress (in two terminals):
$ cylc tui bomdr/sync
$ cylc tui bomdr/model1

# or use the web UI:
$ cylc gui

# always validate after making changes:
$ cylc validate ./sync
```

...
