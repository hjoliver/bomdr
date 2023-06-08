# POC workflow DR system.

## Current status

Sync workflow generated on-the-fly to trigger sync tasks off of one dummy model
workflow (with tasks that write their output files with `touch` and check for
the existence of their input files).

The sync tasks currently just write out what they would do.

### TBD

Implement actually file sync and remote database update, to enable restarting
the system on the remote side at the most recent sync checkpoints.

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
