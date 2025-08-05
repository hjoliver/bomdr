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

The model and sync workflows are configured to run 3 cycle points. Choose a
syncpoint in the second cycle point to demo the remote start.

After running the model workflow once, you can repeat run the sync as many
times as you like (each run will generate new remote sync run-dir).

Syncpoint files look like
`~/cylc-run/REMOTE/bomdr/sync/run3/share/sync-model1-20220101T0000Z-mainfc.json`

```console
# to start the remote model worflow (ID: REMOTE/bomdr/model1/run1:
$ start-remote.py <syncpoint.json>

```
## Appendix: mid-run start-up in Cylc 8

### list start-tasks that need the synced input files

Start with (e.g.) `cylc play --pause --start-task=ID1 --start-task=ID2 ...`:
- The start-tasks will run at start-up regardless of prerequisites
- Dependence on cycles prior to the earliest start-task will be ignored

### off-flow prerequisites

These will stall stall the next cycle, if not downstream of the start-tasks.
If needed (depending on workflow graph structure):
- `cylc set --pre=all` to spawn cycle-start tasks that wait on clock-triggers
- `cylc set --pre=PRE` to satisfy particular prerequisites
- `cylc set [--out=OUT]` to satisfy outputs

### future simplification

With group trigger (8.5.0) and extended task matching (8.6.0) start a whole cycle point
(if only using a single sync point at the start of each cycle).


### [!WARNING]

Beware of previous-cycle ignore behaviour if using start-tasks: if there are any
intercycle dependencies downstream of start-tasks, the corresponding files must
must be synced before start-up.
