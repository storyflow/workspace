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
This process can be tested by creating a MacOS VM in VirtualBox: https://github.com/geerlingguy/macos-virtualbox-vm

