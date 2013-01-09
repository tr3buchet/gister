#!/usr/bin/env python
#
# Copyright 2013 Trey Morris
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import argparse
import ConfigParser
import json
import keyring
import os
import re
import requests
import sys


GITHUB_API = 'https://api.github.com'


def parse_arguments():
    parser = argparse.ArgumentParser(description='make gists!')
    parser.add_argument('-p', '--private', action='store_true',
                        help='put gist on configured enterprise github')
    parser.add_argument('-s', '--secret', action='store_true',
                        help='gist will be secret (not public)')
    parser.add_argument('-v', '--vim', action='store_true',
                        help='gist came from vim, no prompt/history')
    return parser.parse_args()


def parse_config():
    config_parser = ConfigParser.SafeConfigParser(
            defaults={'prompt': '[%(username)s|%(hostname)s %(cwd)s]%%',
                      'history_file': '~/.bash_history',
                      'private_github_url': None})
    config = config_parser.read(os.path.expanduser('~/.gister'))
    if config:
        prompt = config_parser.get('gister', 'prompt', raw=True)
        history_file = config_parser.get('gister', 'history_file')
        url = config_parser.get('gister', 'private_github_url')
    else:
        defaults = config_parser.defaults()
        prompt = defaults['prompt']
        history_file = defaults['history_file']
        url = defaults['private_github_url']
    return prompt, history_file, url


def get_stdin():
    stdin_lines = []
    for line in sys.stdin:
        stdin_lines.append(line)
    return stdin_lines


def get_vim_payload():
    lines = get_stdin()
    filename = lines.pop(0)
    return (filename, ''.join(lines))


def get_commandline_payload(prompt, history_file):
    try:
        username = os.environ['LOGNAME']
        hostname = os.uname()[1]
        cwd = re.sub('/home/%s' % username, '~', os.getcwd())
        prompt = prompt % {'username': username,
                           'hostname': hostname, 'cwd': cwd}
    except:
        prompt = ''

    # get history last line
    command = os.popen('tail -n 1 %s 2>/dev/null' % history_file).read()
    # zsh prefix looks like : 2348907234:0;
    command = re.sub(': \d+:\d+;', '', command)
    # remove the gister pipe at the end
    command = '|'.join(command.split('|')[0:-1])
    if command and prompt:
        prompt_command = '%s %s\n' % (prompt, command)
    else:
        prompt_command = ''

    return ('', '%s%s' % (prompt_command, ''.join(get_stdin())))


def create_gist():
    args = parse_arguments()
    prompt, history_file, private_github_url = parse_config()

    if args.vim:
        payload = get_vim_payload()
    else:
        payload = get_commandline_payload(prompt, history_file)

    if args.private:
        if not private_github_url:
            msg = ('private github url not specified in config file '
                   'see http://github.com/tr3buchet/gister for details')
            raise Exception(msg)
        url = private_github_url
        token = keyring.get_password('pgithub', 'token')
    else:
        url = GITHUB_API
        token = keyring.get_password('github', 'token')

    headers = {'Authorization': 'token %s' % token}
    payload = {'description': 'created by github.com/tr3buchet/gister',
               'public': not args.secret,
               'files': {payload[0]: {'content': payload[1]}}}
    r = requests.post(url + '/gists', data=json.dumps(payload),
                      headers=headers)
    print json.loads(r.text)['html_url']
