# POC workflow DR system.

## Current status

### `bomdr/model1`

This is a dummy model workflow with dummy tasks that check for the existence of
input files and write output files with `touch`. Tasks fail if their expected
input files do not exist.

### `bomdr/sync`

This contains a Jinja2 template to automatically generate a sync workflow for
target tasks in target workflows, as defined in `config.j2`.

The sync workflow has cycles that match the target tasks, and xtriggers that
wait on their success. When an xtrigger is satisfied, a sync task triggers to
copy the target task's output file(s) to the remote, then (once the copy has
succeeded) a task to update the sync point information on the remote: i.e.,
which tasks need to be triggered on the remote to start from the sync point.

It also syncs the target workflow definition, to allow restart on the remote.

### The remote

For this POC, the "remote" is simply a new top-level directory under cylc-run.

The sync process replicates the directory structure of the source
run-directories, for the synced files. Note this means `cylc install` is not
needed on the remote. We can just play the faked workflow directly, from the
latest recorded sync point.

### TBD

- implement script to start remote workflows from most recent sync checkpoints


## Instructions

```
# check your environment:
$ cylc version
8.2.1

# clone your fork locally to to ~/cylc-src/bomdr, then:
$ cd ~/cylc-src/bomdr

# view the Jinja2-processed sync workflow config:
$ cylc view -j ./sync

# validate, install, and run the model1 workflow:
$ cylc vip ./model1

# validate, install, and run the sync workflow:
$ cylc vip ./sync

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
