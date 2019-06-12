# workspace
Setup and manage your Mac for development.

# Workspace Setup

This file should describe everything you need to get your system ready for dev work, 
if there is anything incorrect, broken, or missing when working through it, please submit a PR with the updates.

## Guided Install

Run `./setup.py`

This install does the following:

- Installs homebrew and uses it to install most other dependencies
- Updates gitconfig and gitignore with some common config
- Updates your shell profile
- Installs nvm and uses it to install the appropriate version of Node
- Installs global node dependencies
- Clones common repositories into `~/workspace/voiceflow`
- Initializes AWS configuration and credentials

## Post-Install Steps

- (if applicable) Set zsh as your default shell
- Go into storyflow/database and run `npm run init:local`
- Contact Eric to get the .env.local files for both storyflow-server and storyflow-creator
- Create an Alexa account here: https://developer.amazon.com/alexa

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

## Testing
This process can be tested by creating a MacOS VM in VirtualBox: https://github.com/AlexanderWillner/runMacOSinVirtualBox
