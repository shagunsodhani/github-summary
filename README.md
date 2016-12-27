# github-summary
Tool to generate (weekly) summary of work done on

## Why

Everyone in my team has to write a weekly update describing the different tasks that were completed in the last week. While we do use JIRA and hold scrum, the idea is that this one update mail would keep everyone posted about the general work happening in the team. So every Thursday I would go through my commit history, copy-paste the name of the repos and the commit messages and write them down in an email. To automate this boring task, I wrote this small python tool which fetches all my git commits over the last one week and dumps them at one place. I am collecting only commits as that serves my purpose for now. Support for other events and filtering of commits by repo/org etc can be added later.