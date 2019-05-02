# workstation
Setup and manage your Mac for development

## Initial Manual Steps
Not everything in the setup process can be automated, so let's do the manual steps first

1. Download and install Docker Desktop from this link: https://download.docker.com/mac/stable/Docker.dmg
1. Send your NPM user ID to Eric to be added to the org. If you don't have an NPM account, create one here: https://www.npmjs.com/signup
1. Install the IDE of your choice.
1. Install git using this link: https://git-scm.com/download/mac

1. (Optional) Install iTerm2. It's generally a better terminal than the default Mac one
1. (Optional) Install sexy-bash. Just provides better visibility of branch status

## Automated Install 
This install does the following:

- Installs homebrew in case you need it
- Installs nvm and uses it to install the appropriate version of Node
- Installs global node dependencies
- Pulls and starts Docker images for Redis, Postgres, and Elasticsearch
- creates a directory structure called 'workspace' and clones all the common repos
- Creates fake AWS creds file (you can replace it later if necessary)
- Runs the database initialization

## Final Manual Steps

- Contact Eric or Tyler to get the .env.local files for both storyflow-server and storyflow-creator
- Talk to Andrew to get an AWS account created
- Create an Alexa account


# Notes
This process can be tested by creating a MacOS VM in VirtualBox: https://github.com/AlexanderWillner/runMacOSinVirtualBox

# Commits and Versioning

In order to provide an accurate changelog as we fix bugs and deploy features, we apply a linter to commit messages. [commitlint](https://commitlint.js.org/#/) applies a bunch of rules to ensure that commit messages can be rolled up into a release and changelog. 

In general the pattern mostly looks like this:
```sh
type(scope?): subject  #scope is optional
```
Real world examples can look like this:
```
chore: run tests on travis ci
```
```
fix(server): send cors headers
```
```
feat(blog): add comment section
```

If you are unsure about the format, you can run `npm run commit` and it'll run you through an interactive commit builder.

Pull requests to `master` and `production` branches must have at least one commit that follows this convention, or a PR title that does in order to be mergable.
