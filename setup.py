#!/usr/bin/python
from copy import deepcopy
import os
import subprocess
import sys
import time

FNULL = open(os.devnull, 'w')

NODE_VERSION = "11"

def main():
    people = {
        'sol_arch': 'Frank Gu <frank@voiceflow.com>',
        'eng_lead': 'Eric Hacke <eric@voiceflow.com>'
    }

    preinstall_check(people)
    usr_shell = get_shell()
    install_shell_utils = query_yes_no('Would you like to install shell appearance optimizations?', default='yes')
    workspace_path = get_workspace_dir()
    install_chrome = query_yes_no('Would you like Google Chrome installed?', default='yes')
    install_iterm2 = query_yes_no('Would you like iTerm2 installed?', default='yes')
    configure_aws_user()

    install_pip()
    print('Automated install step begins. I will need a few minutes, so go grab a coffee ' + u'\u2615'+'!')

    install_homebrew()
    casks = ['docker']
    if install_chrome:
        if os.path.isdir('/Applications/Google Chrome.app'):
            print('You seem to have Google Chrome already installed, so I will not install it again!')
        else:
            casks.append('google-chrome')
    if(install_iterm2):
        casks.append('iterm2')
    install_casks(casks)

    install_tools(['git', 'vim', 'bash-completion', 'docker-completion', 'jq', 'wget', 'libpq', 'awscli'], shell=usr_shell)
    install_nvm(shell=usr_shell)
    configure_shell(usr_shell, install_shell_utils)
    configure_git()
    clone_repositories(['storyflow-creator', 'storyflow-server', 'database'], workspace_path)
    post_install(usr_shell)

def post_install(usr_shell):
    print('\n\nStart: Post install operations '.ljust(62,'>'))
    print("Installing Docker cleanup crontab")
    with open('/tmp/crontab.user', 'w+') as f:
        subprocess.call(['crontab','-l'], stdout=f)
    insert_line('/tmp/crontab.user', '15 23 * * * /usr/local/bin/docker system prune -f')
    subprocess.call(['crontab', '/tmp/crontab.user'])

    print('Login to NPM')
    subprocess.call(['npm', 'login'])
    print('Done: Post install operations '.ljust(60,'<'))

    if usr_shell == 'zsh':
        print('\n\n')
        print('Remember to set your default shell as zsh:')
        print('    $ sudo sh -c "echo $(which zsh) >> /etc/shells"')
        print('    $ chsh -s $(which zsh)')

    print('\n\n')
    print('You are all set to go!')
    
def get_workspace_dir(default_dir='~/workspace/voiceflow'):
    dir_valid = False
    while not dir_valid:
        path = raw_input('Where would you like your workspace to be? ['+default_dir+']: ')
        if path == '':
            path = default_dir
        if subprocess.call(['mkdir', '-p', os.path.expanduser(path)]) != 0:
            print('I cannot put your workspace there. Please enter another path!')
        else: 
            return path

def preinstall_check(personale_dict):
    print('Welcome to Voiceflow! I am going to set up your computer for development.')
    print('Before we begin, I will make sure you have all the information ready!\n\n')
    
    # Check AWS access
    if not query_yes_no('Did you receive AWS credentials?'):
        print('Please speak to %s' % (personale_dict['sol_arch']))
        if not query_yes_no('Continue?'):
            exit(0)

    # Check GitHub setup
    if not query_yes_no('Is your GitHub set up with 2FA'):
        subprocess.call(['open', '-a', 'Safari', 'https://help.github.com/en/articles/securing-your-account-with-two-factor-authentication-2fa'])
        print('If you have any questions, please speak to %s' % (personale_dict['sol_arch']))
        if not query_yes_no('Continue?'):
            exit(0)

    # Check GitHub access
    if not query_yes_no('Did you receive GitHub access?'):
        print('Please speak to %s' % (personale_dict['eng_lead']))
        if not query_yes_no('Continue?'):
            exit(0)
    
    # Check NPM access
    if not query_yes_no('Did you receive NPM access?'):
        print('Please create an NPM account')
        print('Then speak to %s' % (personale_dict['eng_lead']))
        time.sleep(2)
        subprocess.call(['open', '-a', 'Safari', 'https://www.npmjs.com/signup'])
        if not query_yes_no('Continue?'):
            exit(0)

def configure_aws_user():
    print('\n\nStart: Configure AWS '.ljust(62,'>'))
    aws_credential_path = '~/.aws/credentials'
    aws_config_path = '~/.aws/config'
    subprocess.call(['mkdir', '-p', os.path.expanduser('~/.aws')])

    # Write new aws config
    with open(os.path.expanduser(aws_config_path), 'w+') as f:
        f.write('[default]\n')
        f.write('region = us-east-1\n')
        f.write('output = json\n')

    if query_yes_no('Do you need non-default AWS credentials?', default='no'):
        if os.path.isfile(os.path.expanduser(aws_credential_path)) and \
            not query_yes_no('I found existing AWS credentials. Overwrite?', default='no'):
            # User doesn't want to overwrite existing credentials
            return
        
        # Write new credentials
        aki = raw_input('Aceess Key ID: ')
        sak = raw_input('Secret Access Key: ')
    else: 
        aki = 'AKIAIOSFODNN7EXAMPLE'
        sak = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

    with open(os.path.expanduser(aws_credential_path), 'w+') as f:
        f.write('[default]\n')
        f.write('aws_access_key_id = ' + aki + '\n')
        f.write('aws_secret_access_key = ' + sak + '\n')
    print('\n\nDone: Configure AWS '.ljust(60,'<'))

def configure_shell(shell='bash', install_optimizations=True):
    print('\n\nStart: Configure shell '.ljust(62,'>'))
    if shell == 'bash':
        shell_profile = '~/.bash_profile'
        print('Installing bash_completion scripts')
        bash_completion_line = '[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion\n'
        insert_line(os.path.expanduser('~/.bash_profile'), bash_completion_line)
        if install_optimizations:
            print('Installing sexy-bash-prompt')
            subprocess.call(['rm', '-rf', '/tmp/sexy-bash-prompt'])
            subprocess.call(['mkdir', '/tmp/sexy-bash-prompt'])
            subprocess.call(['git','clone','--depth','1','--config','core.autocrlf=false','https://github.com/twolfson/sexy-bash-prompt', '/tmp/sexy-bash-prompt'])
            subprocess.call(['make', '-C', '/tmp/sexy-bash-prompt', 'install'])
    else: 
        shell_profile = '~/.zshrc'
        
        if install_optimizations:
            print('Installing oh-my-zsh')
            subprocess.call(['curl','-Lo','/tmp/install.sh','https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh'])
            subprocess.call(['sh', '/tmp/install.sh', '--unattended'])
            subprocess.call(['sed', '-i', '', 's:^ZSH_THEME.*$:ZSH_THEME=\"bira\":g',os.path.expanduser('~/.zshrc')])       
    
    subprocess.call(['touch', os.path.expanduser(shell_profile)])
    insert_line(os.path.expanduser(shell_profile),'# Voiceflow environments')
    insert_line(os.path.expanduser(shell_profile),'NODE_ENV=local')
    print('\n\nDone: Configure shell '.ljust(60,'<'))

def install_nvm(shell='bash'):
    if shell == 'bash':
        shell_profile = '~/.bash_profile'
    else: 
        shell_profile = '~/.zshrc'

    # Install NVM
    subprocess.call(['curl', 'https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh', '-o', '/tmp/install_nvm.sh'])
    subprocess.call(['sh', '/tmp/install_nvm.sh'])

    # Install nvm shell profile settings
    subprocess.call(['touch', os.path.expanduser(shell_profile)])
    insert_line(os.path.expanduser(shell_profile), '# NVM')
    insert_line(os.path.expanduser(shell_profile), 'export NVM_DIR="$HOME/.nvm"')
    insert_line(os.path.expanduser(shell_profile), r'[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm')
    insert_line(os.path.expanduser(shell_profile), r'[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion')
    subprocess.call(['sh', './install_node.sh'])

def clone_repositories(repo_list, workspace_dir='~/workspace/voiceflow'):
    print('\n\nStart: Clone repositories '.ljust(62,'>'))
    subprocess.call(['mkdir', '-p', os.path.expanduser(workspace_dir)])
    for repo in repo_list:
        repo_path = os.path.join(os.path.expanduser(workspace_dir), repo)
        if not os.path.isdir(repo_path):
            subprocess.call(['mkdir', '-p', repo_path])
            subprocess.call(['git', 'clone', 'https://github.com/storyflow/'+repo+'.git',repo_path])
        else: 
            print(repo + ' is already cloned. Remember to pull!')
    print('Done: Clone repositories '.ljust(60,'<'))

def get_shell():
    ans = True
    while ans: 
        prompt = (
        "Which shell are you using?\n"
        "1.bash (default)\n"
        "2.zsh\n"
        "Selection: ")

        ans=raw_input(prompt)
        if ans == '1':
            usr_shell = 'bash'
            break
        elif ans == '2':
            usr_shell = 'zsh'
            break
        else:
            print('Please select your shell from the menu!')
            ans = True
    print("Installing for %s" % (usr_shell))
    return usr_shell

def install_pip():
    print('\n\nStart: Install pip '.ljust(62,'>'))

    if subprocess.call(['which', 'pip']) == 0:
        print('Pip is installed for your Python!')
    else:
        # subprocess.call(['curl', 'https://bootstrap.pypa.io/get-pip.py', '-o', '/tmp/get-pip.py'])
        # subprocess.call(['python', '/tmp/get-pip.py', '--user'])
        subprocess.call(['sudo', 'easy_install', 'pip'])
    print('Done: Install pip '.ljust(60,'<'))

def install_homebrew():
    print('\n\nStart: Install Homebrew '.ljust(62,'>'))
    if subprocess.call(['which', 'brew']) == 0:
        print('Homebrew already installed; upgrading...')
        subprocess.call(['brew', 'update'])
        subprocess.call(['brew', 'upgrade'])
        subprocess.call(['brew', 'cleanup'])
    else:
        print('Installing CLT for Xcode...')
        subprocess.call(['xcode-select', '--install'])
        print('Installing Homebrew...')
        subprocess.call(['curl', 'https://raw.githubusercontent.com/Homebrew/install/master/install', '-o', '/tmp/install_homebrew.rb'])
        retCode = subprocess.call(['/usr/bin/ruby','/tmp/install_homebrew.rb'], stdin=FNULL)

        if retCode != 0:
            print("Homebrew install failed!!")
            exit(retCode)
    print('Done: Install Homebrew '.ljust(60,'<'))

def install_node(version='11'):
    print('\n\nStart: Install node '.ljust(62,'>'))
    subprocess.call(['nvm', 'install', version])
    subprocess.call(['nvm', 'use', version])
    subprocess.call(['nvm', 'alias', 'default', version])
    subprocess.call(['npm', 'install', '-g', 'npm-check','mocha','npm','yarn'])
    print('Done: Install node '.ljust(60,'<'))

def brew_install_list(bin_list, mode='tap'):
    if mode == 'cask':
        brew_cmd = ['brew', 'cask']
    else: 
        brew_cmd = ['brew']
    brew_args = deepcopy(brew_cmd)
    brew_args.append('install')
    
    install_needed = False
    for tool in bin_list:
        check_cmd = deepcopy(brew_cmd)
        check_cmd.extend(['list', tool])
        
        if subprocess.call(check_cmd, stdout=FNULL, stderr=subprocess.STDOUT) != 0:
            print('Added %s to installation' % (tool))
            brew_args.append(tool)
            install_needed = True
        else: 
            print('%s is installed!' % (tool))
    if install_needed:
        subprocess.call(brew_args)
    
def install_tools(tools_list, shell='bash'):
    print('\n\nStart: Install tools '.ljust(62,'>'))
    if shell == 'zsh':
        tools_list.append('zsh')
        shell_path = '~/.zshrc'
    else:
        shell_path = '~/.bash_profile'
    subprocess.call(['touch', os.path.expanduser(shell_path)])
    brew_install_list(tools_list, mode='tap')

    # Add libpq binaries to PATH
    libpq_path = 'export PATH="/usr/local/opt/libpq/bin:$PATH"'

    insert_line(os.path.expanduser(shell_path), '# Postgres utilities')
    insert_line(os.path.expanduser(shell_path), libpq_path)
    subprocess.call(['mkdir', '-p', os.path.expanduser('~/.nvm')])
    print('Done: Install tools '.ljust(60,'<'))

def install_casks(cask_list):
    print('\n\nStart: Install casks '.ljust(62,'>'))    
    brew_install_list(cask_list, mode='cask')
    print('Done: Install casks '.ljust(60,'<'))

def configure_git():
    print('\n\nStart: Configure git '.ljust(62,'>'))
    subprocess.call(['touch', os.path.expanduser('~/.gitignore')]) 
    subprocess.call(['git', 'config', '--global', 'credential.helper', 'osxkeychain'])
    subprocess.call(['git', 'config', '--global', 'alias.push', "'push --follow-tags'"])
    subprocess.call(['git', 'config', '--global', 'alias.st', 'status'])
    subprocess.call(['git', 'config', '--global', 'alias.co', 'checkout'])
    subprocess.call(['git', 'config', '--global', 'alias.br', 'branch'])
    subprocess.call(['git', 'config', '--global', 'alias.pr', "'pull --rebase'"])
    subprocess.call(['git', 'config', '--global', 'alias.rb', "'rebase --interactive'"])
    subprocess.call(['git', 'config', '--global', 'alias.can', "'commit --amend --no-edit'"])
    subprocess.call(['git', 'config', '--global', 'core.excludesfile', os.path.expanduser('~/.gitignore')])
    write_gitignore(os.path.expanduser('~/.gitignore'), ['.idea', '.DS_STORE', 'scratch.*'])
    print('Done: Configure git '.ljust(60,'<'))

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def write_gitignore(file_path, ignores):  
    for line in ignores:
        insert_line(file_path, line)

def insert_line(file_path, needle):
    add_newline = False
    # Only check if a newline needs to be added for non-empty files
    if os.stat(file_path).st_size != 0:
        with open(file_path, 'rb+') as f:
            f.seek(-1,2)
            lastChar = f.read()
            if lastChar != b'\n':
                add_newline = True

    with open(file_path, "r+") as file:
        for line in file:
            if needle in line:
                break
        else: # not found, we are at the eof
            if add_newline:
                file.write('\n')
            file.write(needle + '\n') # append missing data

if __name__ == '__main__':
    main()
