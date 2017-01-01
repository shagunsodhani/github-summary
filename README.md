# github-summary
Tool to generate (weekly) summary of work done on

## Setup

* Run `./setup.sh`
* Update the config values in `config/config.cfg`. The meaning of config parameters is explained below.
* Run `python3 main.py` to obtain commits for past one week. 

## Config Parameters

* `base_url` - URL for accessing the github api. `https://api.github.com` for github.com.
* `username` - user for whom the commits are to be collected.
* `client_id` and `client_secret` may be created at [https://github.com/settings/tokens](https://github.com/settings/tokens). They may also be left blank in which case unauthenticated requests will be made to github api which are rate limited and will not fetch commits from private repos. Further, enterprise github installations may only support authenticated requests.
* `lookback_time` - number of seconds to lookback since the current time when retriving commits. For example, `lookback_time=604800` means commits older than 604800 seconds (604800 = 60*60*24*7) or 7 days will not be retrived.

## To change the output format

* Update the `summarise_commits()` method in [`github/activity.py`](github/activity.py)

## Why

Everyone in my team has to write a weekly update describing the different tasks that were completed in the last week. While we do use JIRA and hold scrum, the idea is that this one update mail would keep everyone posted about the general work happening in the team. So every Thursday I would go through my commit history, copy-paste the name of the repos and the commit messages and write them down in an email. To automate this boring task, I wrote this small python tool which fetches all my git commits over the last one week and dumps them at one place. I am collecting only commits as that serves my purpose for now. Support for other events and filtering of commits by repo/org etc can be added later.

## Sample Output

```

In repo shagunsodhani/github-summary:
1: Make unauthenticated request to github API in case client_id or client_secret is missing        https://github.com/shagunsodhani/github-summary/commit/5cacfd4570702db3e46932a3e739188842424601
2: Added demo values to the sample config and added setup script        https://github.com/shagunsodhani/github-summary/commit/10d0f11057ec9da7c6df5db039e00caa715cbfe6
3: updated README        https://github.com/shagunsodhani/github-summary/commit/6213f1b4dc73450906ba3b5355a95593db3ee5a5
4: Added main.py        https://github.com/shagunsodhani/github-summary/commit/fbb08e5d30519f340c109b178f1b1f1fef1e4f97
5: renamed github.py as activity.py        https://github.com/shagunsodhani/github-summary/commit/87777c618fd44a1955c885444b3bd6b60c07a86f
6: added placeholder method to generate summary of commits and using config dict to pass around params        https://github.com/shagunsodhani/github-summary/commit/9039df13e8dc4dfbe298660657ed8adb28af9514
7: Added class to handle events returned by github API        https://github.com/shagunsodhani/github-summary/commit/c1ec78a4c80bba9115c74a2bbdb6dbc5fad7927d
8: Added commit class        https://github.com/shagunsodhani/github-summary/commit/321a77ada28ab66774e74df4b8b9541c1eea491d
9: completed method to generate summary for commits in last one week.        https://github.com/shagunsodhani/github-summary/commit/3194da7aa67a4ab49f56096cefd46a230bc706b5
10: added .idea and config to gitignore        https://github.com/shagunsodhani/github-summary/commit/f87818793ef906c4ec54a33fa83adceffecdeeb5
11: Added sample config file        https://github.com/shagunsodhani/github-summary/commit/a01b92f757802bdee6bfafae91d24acb1d77e647
12: added method to obtain all events since a given date        https://github.com/shagunsodhani/github-summary/commit/d46e747617bb915ea9653fb30f229b646d2046ac
13: added method to obtain all user commits since a given date        https://github.com/shagunsodhani/github-summary/commit/97593bae00ed7c273f3ebb9bdf5e534fa16947d3
14: Added utility package with config parser and constants file        https://github.com/shagunsodhani/github-summary/commit/8cca28dc0a2c5df0e05cf7aa93dad6d5fd1401d4

In repo shagunsodhani/papers-I-read:
1: Added Open Vocabulary NMT paper        https://github.com/shagunsodhani/papers-I-read/commit/63b7cd141ebd95768b94f7ae62866703c8f01091
2: Added RNTN paper        https://github.com/shagunsodhani/papers-I-read/commit/d3eaf079b3c59a8dc4a7dbad58fbfbf69ee33367
3: Added images from RNTN paper        https://github.com/shagunsodhani/papers-I-read/commit/cb31fe3f638f893f0cae8dfd7cd756d85be56346

In repo shagunsodhani/citadel:
1: Added link for tensorflow debugging        https://github.com/shagunsodhani/citadel/commit/97fdefc7176fa52edc94ee9c57f572f0befd4b24

```