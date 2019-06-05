#!/usr/local/bin/python3
import sys
import os
import subprocess
from copy import deepcopy

def main():
    print('Welcome to Voiceflow! I am going to set up your computer for development.')
    usr_shell = get_shell()
    print("Installing for %s" % (usr_shell))
    # install_iterm = query_yes_no('Would you like me to install iTerm2?', default='yes')
    # install_pip3()
    # install_homebrew()
    install_tools(['git', 'vim', 'bash-completion', 'jq', 'wget', 'libpq'], shell=usr_shell)
    # install_casks(['docker', 'iterm2'])
    # install_tools(['docker-completion'])
    configure_git()

def get_shell():
    ans = True
    while ans: 
        prompt = (
        "Which shell are you using?\n"
        "1.bash (default)\n"
        "2.zsh\n"
        "Selection: ")

        ans=input(prompt)
        if ans == '1':
            return 'bash'
        elif ans == '2':
            return 'zsh'
        else:
            print('Please select your shell from the menu!')

def install_pip3():
    print('\n\nStart: Install pip3 '.ljust(62,'>'))

    if subprocess.run(['which', 'pip3']).returncode == 0:
        print('Pip3 is installed for your Python!')
    else:
        subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py', '-o', '/tmp/get-pip.py'])
        subprocess.run(['python3', '/tmp/get-pip.py'])
    print('Done: Install pip3 '.ljust(60,'<'))

def install_homebrew():
    print('\n\nComponent: Homebrew '.ljust(62,'>'))
    if subprocess.run(['which', 'brew']).returncode == 0:
        print('Homebrew already installed; upgrading...')
        subprocess.run(['brew', 'update'])
        subprocess.run(['brew', 'upgrade'])
        subprocess.run(['brew', 'cleanup'])
    else:
        print('Installing CLT for Xcode...')
        subprocess.run(['xcode-select', '--install'])
        print('Installing Homebrew...')
        retCode = subprocess.run(['/usr/bin/ruby','e','"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'])
        if retCode != 0:
            print("Homebrew install failed!!")
            exit(retCode)
    print('Done: Homebrew '.ljust(60,'<'))

def brew_install_list(bin_list, mode='tap'):
    if mode == 'cask':
        brew_cmd = ['brew', 'cask']
    else: 
        brew_cmd = ['brew']
    brew_args = deepcopy(brew_cmd).append('install')
    install_needed = False
    for tool in bin_list:
        check_cmd = deepcopy(brew_cmd)
        check_cmd.extend(['list', tool])
        if subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode != 0:
            print('Added %s to installation' % (tool))
            brew_args.append(tool)
            install_needed = True
        else: 
            print('%s is installed!' % (tool))
    if install_needed:
        subprocess.run(brew_args)
    
def install_tools(tools_list, shell='bash'):
    print('\n\nStart: Install tools '.ljust(62,'>'))
    brew_install_list(tools_list, mode='tap')

    # Add libpq binaries to PATH
    libpq_path = 'export PATH="/usr/local/opt/libpq/bin:$PATH"'
    if shell == 'bash':
        insert_line(os.path.expanduser('~/.bash_profile'), libpq_path)
    elif shell == 'zsh':
        insert_line(os.path.expanduser('~/.zshrc'), libpq_path)
    print('Done: Install tools '.ljust(60,'<'))

def install_casks(cask_list):
    print('\n\nStart: Install casks '.ljust(62,'>'))    
    brew_install_list(cask_list, mode='cask')
    print('Done: Install casks '.ljust(60,'<'))

def configure_git():
    print('\n\nStart: Configure git '.ljust(62,'>'))  
    subprocess.run(['git', 'config', '--global', 'credential.helper', 'osxkeychain'])
    subprocess.run(['git', 'config', '--global', 'alias.push', "'push --follow-tags'"])
    subprocess.run(['git', 'config', '--global', 'alias.st', 'status'])
    subprocess.run(['git', 'config', '--global', 'alias.co', 'checkout'])
    subprocess.run(['git', 'config', '--global', 'alias.br', 'branch'])
    subprocess.run(['git', 'config', '--global', 'alias.pr', "'pull --rebase'"])
    subprocess.run(['git', 'config', '--global', 'alias.rb', "'rebase --interactive'"])
    subprocess.run(['git', 'config', '--global', 'alias.can', "'commit --amend --no-edit'"])
    subprocess.run(['git', 'config', '--global', 'core.excludesfile', os.path.expanduser('~/.gitignore')])
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
        choice = input().lower()
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

def insert_line(file_path, line):
    existingLines = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as rof:
            existingLines = [line.rstrip('\n') for line in rof.readlines()]
        
    with open(file_path, 'a+') as af:
        if line not in existingLines:
            af.write(line + '\n')

if __name__ == '__main__':
    main()
