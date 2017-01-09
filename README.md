# github-summary
Tool to generate (weekly) summary of work done on

## Setup

* Run `./setup.sh`
* Update the config values in `config/config.cfg`. The meaning of config parameters is explained below.
* Run `python3 main.py` to obtain commits for past one week.
* There are two ways for specifying how much time to look back since the current time when retriving commits:
    * Commandline option - `python3 main.py -t *lookback_time*`. The supported formats are discussed under `lookback_time`[here](README.md#config-parameters)
    * Setting as a config parameter - discussed under `lookback_time`[here](README.md#config-parameters)
* There are two ways for specifying how to group the commits:
	* Commandline option - `python3 main.py -g *group_by*`. The supported formats are discussed under `group_by`[here](README.md#config-parameters)
    * Setting as a config parameter - discussed under `group_by`[here](README.md#config-parameters)

## Config Parameters

* `base_url` - URL for accessing the github api. `https://api.github.com` for github.com.
* `username` - user for whom the commits are to be collected.
* `client_id` and `client_secret` may be created at [https://github.com/settings/developers](https://github.com/settings/developers) while `access_token` maybe created at [https://github.com/settings/tokens](https://github.com/settings/tokens). For making authenticated requests, either populate `client_id` and `client_secret` or populate `access_token`. They may also be left blank in which case unauthenticated requests will be made to github api which are rate limited and will not fetch commits from private repos. Further, enterprise github installations may only support authenticated requests.
* `lookback_time` - How much time to look back since the current time when retriving commits.
Supported values:
	* **n**s - commits older than **n** seconds.
	* **n**m - commits older than **n** minutes.
	* **n**h - commits older than **n** hours.
	* **n**d - commits older than **n** days.
	* **n**w - commits older than **n** weeks.
For example, `lookback_time=7d` means commits older than 7 days will not be retrived.
* `group_by* - How to group the list of commits.
Supported values:
	* **r** - group commits by repo.
	* **rd** - group commits by repo and then by date.
	* **dr** - group commits by date and then by repo.

## To change the output format

* Update the `summarise_commits()` method in [`github/activity.py`](github/activity.py)

## Why

Everyone in my team has to write a weekly update describing the different tasks that were completed in the last week. While we do use JIRA and hold scrum, the idea is that this one update mail would keep everyone posted about the general work happening in the team. So every Thursday I would go through my commit history, copy-paste the name of the repos and the commit messages and write them down in an email. To automate this boring task, I wrote this small python tool which fetches all my git commits over the last one week and dumps them at one place. I am collecting only commits as that serves my purpose for now. Support for other events and filtering of commits by repo/org etc can be added later.

## Sample Output

```

In repo github.com/shagunsodhani/citadel:

1: 4fb6f09f36fb05884cd0b352c09b21e4d7f45263 - Added GAN links

=============================================================================

In repo github.com/shagunsodhani/github-summary:

1: b8cc12f68c6581d36f21342ba77d48a2f28a5e88 - Not listing messages related to merges and formatted the commit messages to have consistent formatting. Fixes #2
2: 167d792d4ec707390c13cfafd453cd9d2213c8a2 - Added support for commandline flag for specifying duration. Fixes #4
3: 208c2bce0e8a7185b17a00bc5936b303231ca703 - Added support for commandline flag for specifying duration. Fixes #3
4: 3a8934baf1ee2a809bb7b973fe5bd07bac26d0b8 - Improve formatting in README.md
5: b864f739ffd86285820668eac9af8cbef5856a13 - Added constants in place of strings
6: 7e052c5d84f6c5ab55e2813dfabeb209c99e3e2e - Added more formats to specify time. Related to #4

=============================================================================

In repo github.com/shagunsodhani/papers-I-read:

1: 1a978b4bb793be955edda082bdf6e91a84cf0634 - Added paper on "Addressing the Rare Word Problem in Neural Machine Translation"

=============================================================================

```