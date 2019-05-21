#!/bin/bash

set -e

NODE_VERSION=11
NVM_VERSION=0.34.0

echo ""
echo ""
echo "###################################################"
echo "   Installing brew, then using brew to install deps"
echo "###################################################"
echo ""
echo ""

if ! hash brew 2>/dev/null; then
    echo "brew not found, installing..."
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    echo "brew already installed, updating"
    brew update
    brew upgrade
    brew cleanup
fi

brew install git bash-completion vim jq wget postgresql
brew tap caskroom/cask
brew cask install docker
brew cask install iterm2
brew install docker-completion

git config --global credential.helper osxkeychain
git config --global alias.push 'push --follow-tags'
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.pr 'pull --rebase'
git config --global alias.rb 'rebase --interactive'
git config --global alias.can 'commit --amend --no-edit'


echo ".idea" >> ~/.gitignore
echo ".DS_STORE" >> ~/.gitignore
echo "scratch.*" >> ~/.gitignore

echo "[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion" >> ~/.bash_profile

AWS_CREDS=~/.aws/credentials

if [[ -f "$AWS_CREDS" ]]; then
    echo "$AWS_CREDS exists"
else
    echo "[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" > ${AWS_CREDS}
fi

echo ""
echo ""
echo "##################################################"
echo "   Installing NVM and related node stuff"
echo "##################################################"
echo ""
echo ""

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

nvm install ${NODE_VERSION}
nvm use ${NODE_VERSION}
nvm alias default ${NODE_VERSION}

npm install -g npm-check mocha npm yarn

echo ""
echo ""
echo "##################################################"
echo "   Updating .bash_prompt"
echo "##################################################"
echo ""
echo ""

echo "alias ll='ls -alFh'" >> ~/.bash_profile
echo "alias v='cd ~/workspace/voiceflow'" >> ~/.bash_profile
echo "NODE_ENV=local" >> ~/.bash_profile

(cd /tmp && git clone --depth 1 --config core.autocrlf=false https://github.com/twolfson/sexy-bash-prompt && cd sexy-bash-prompt && make install) && source ~/.bashrc

echo ""
echo ""
echo "##################################################"
echo "   Setting up workspace and cloning"
echo "##################################################"
echo ""
echo ""

echo "About to prompt for github auth info. In place of the password, supply a person auth token you've created here: https://github.com/settings/tokens"
echo "Press enter when you've created the token and are ready to begin: "
read

mkdir -p ~/workspace/voiceflow/

cd ~/workspace/voiceflow/

if [ ! -d ~/workspace/voiceflow/storyflow-creator ]; then
    git clone https://github.com/storyflow/storyflow-creator
fi

if [ ! -d ~/workspace/voiceflow/storyflow-server ]; then
    git clone https://github.com/storyflow/storyflow-server
fi

if [ ! -d ~/workspace/voiceflow/database ]; then
    git clone https://github.com/storyflow/database
fi

echo ""
echo ""
echo "##################################################"
echo "   Final notes"
echo "##################################################"
echo ""
echo ""

echo "Shortcuts:"
echo "- 'git st' is an alias for 'git status'"
echo "- 'git co' is an alias for 'git checkout'"
echo "- Take a look at ~/.gitconfig for some other git aliases or create your own"
echo "- 'v' is an alias for 'cd ~/workspace/voiceflow'"
echo "- 'll' is an alias for 'ls -alFh'"

echo "Remaining manual steps:"
echo "- Launch Docker from applications to let it complete it's installation"
echo "- Log into npm with 'npm login'"
echo "- Once docker is installed and running, you can run ./scripts/docker_dependencies.sh in any repo to start/restart the docker dependencies for that repo"
