import argparse
import ConfigParser
import keyring
import os
import re
import sys

from github import Github
from github import InputFileContent


# parse args
arg_parser = argparse.ArgumentParser(description='make gists')
arg_parser.add_argument('-p', '--private', action='store_true',
                        help='put gist on configured enterprise github')
arg_parser.add_argument('-s', '--secret', action='store_true',
                        help='gist will be secret (not public)')
arg_parser.add_argument('-v', '--vim', action='store_true',
                        help='gist came from vim, no prompt/history')
args = arg_parser.parse_args()


# get stdin
stdin_lines = []
for line in sys.stdin:
    stdin_lines.append(line)


config_parser = ConfigParser.SafeConfigParser()
files = config_parser.read(['.gister', os.path.expanduser('~/.gister')])

if args.vim:
    payload = ''
else:
    prompt = config_parser.get('gister', 'prompt', raw=True)
    history_file = config_parser.get('gister', 'history_file')
    username = os.environ['LOGNAME']
    hostname = os.uname()[1]
    cwd = re.sub('/home/%s' % username, '~', os.getcwd())
    prompt = prompt % {'username': username, 'hostname': hostname, 'cwd': cwd}

    # get history last line
    command = os.popen('tail -n 1 %s' % history_file).read()
    # zsh timestamp looks like : 2348907234:0;
    command = re.sub(': \d+:\d+;', '', command)
    # remove the gister pipe at the end
    command = '|'.join(command.split('|')[0:-1])

    payload = '%s %s\n%s' % (prompt, command, ''.join(stdin_lines))


# create gist
if args.private:
    url = config_parser.get('gister', 'private_github_url')
    token = keyring.get_password('pgithub', 'token')
    g = Github(token, base_url=url)
else:
    token = keyring.get_password('github', 'token')
    g = Github(token)

u = g.get_user()

f = InputFileContent(payload)
files = {'': f}
u.create_gist(not args.secret, files, 'created by github.com/tr3buchet/gister')
