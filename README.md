# Mercurial Bugspots

A Python based implementation of the bug prediction algorithm proposed by Google: 
[Bug Prediction at Google](http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html)

## Usage
```
$ pip install bugspots
$ hg bugspots (In the root path of your repo, use --help)
```

## Example usage

niedbalski@machine:~/src/rabbitmq-server$ hg bugspots .


Scanning file:/home/aktive/src/rabbitmq-server repo, branch:default
Found 16 bugfix commits on the last 30 days

Fixes
--------------------------------------------------------------------------------
      -Oops. This was part of an (early, wrong) attempt at bug 25474 which got committed as part of f1317bb80df9 (bug 25358) by mistake. Remove.
      -merge bug19375 into default
      -merge bug25488 into default
      -Merge bug25495
      -Merge bug25497
      -Merged bug25474 and bug25486
      -Merged bug25499
      -merge bug25384 into default
      -merge bug23378 into default
      -Merge bug25461
      -merge bug23749 into default
      -Merge bug24114 into default
      -Merged bug25491 into default
      -Merged bug25499 into default
      -merge bug25487 into default
      -Merge bug25519.

Hotspots
--------------------------------------------------------------------------------
      0.23 = src/rabbit_node_monitor.erl
      0.15 = src/rabbit_channel.erl
      0.08 = src/rabbit_tests.erl
      0.08 = src/rabbit_amqqueue_process.erl
      0.08 = src/rabbit_exchange.erl
