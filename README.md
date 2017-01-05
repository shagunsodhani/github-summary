# github-summary
Tool to generate (weekly) summary of work done on

## Setup

* Run `./setup.sh`
* Update the config values in `config/config.cfg`. The meaning of config parameters is explained below.
* Run `python3 main.py` to obtain commits for past one week. 

## Config Parameters

* `base_url` - URL for accessing the github api. `https://api.github.com` for github.com.
* `username` - user for whom the commits are to be collected.
* `client_id` and `client_secret` may be created at [https://github.com/settings/developers](https://github.com/settings/developers) while `access_token` maybe created at [https://github.com/settings/tokens](https://github.com/settings/tokens). For making authenticated requests, either populate `client_id` and `client_secret` or populate `access_token`. They may also be left blank in which case unauthenticated requests will be made to github api which are rate limited and will not fetch commits from private repos. Further, enterprise github installations may only support authenticated requests.
* `lookback_time` - number of seconds to lookback since the current time when retriving commits. For example, `lookback_time=604800` means commits older than 604800 seconds (604800 = 60*60*24*7) or 7 days will not be retrived.

## To change the output format

* Update the `summarise_commits()` method in [`github/activity.py`](github/activity.py)

## Why

Everyone in my team has to write a weekly update describing the different tasks that were completed in the last week. While we do use JIRA and hold scrum, the idea is that this one update mail would keep everyone posted about the general work happening in the team. So every Thursday I would go through my commit history, copy-paste the name of the repos and the commit messages and write them down in an email. To automate this boring task, I wrote this small python tool which fetches all my git commits over the last one week and dumps them at one place. I am collecting only commits as that serves my purpose for now. Support for other events and filtering of commits by repo/org etc can be added later.

## Sample Output

```

In repo github.com/shagunsodhani/citadel:

1: 4fb6f09f36fb05884cd0b352c09b21e4d7f45263 - Added GAN links
2: 97fdefc7176fa52edc94ee9c57f572f0befd4b24 - Added link for tensorflow debugging

In repo github.com/shagunsodhani/github-summary:

1: 1323b5e55e95522ed1c556ef8efd9515e6013a08 - Added support for access_tokens
2: ad46b38a011239309ef6bdcfb9a3208a6a84f576 - Added a parameter in the config to control how much older commits are retrived
3: be4cda323349f02cccc4effc5ec304dcf745a328 - Added instructions to setup and use. Fixes #1
4: 5cacfd4570702db3e46932a3e739188842424601 - Make unauthenticated request to github API in case client_id or client_secret is missing
5: 10d0f11057ec9da7c6df5db039e00caa715cbfe6 - Added demo values to the sample config and added setup script

In repo github.com/shagunsodhani/papers-I-read:

1: 63b7cd141ebd95768b94f7ae62866703c8f01091 - Added Open Vocabulary NMT paper

```