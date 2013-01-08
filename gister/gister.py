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


def get_stdin():
    stdin_lines = []
    for line in sys.stdin:
        stdin_lines.append(line)
    return stdin_lines


def get_vim_payload():
    filename = 'asdf'
    text = 'some more!'
    return (filename, text)


def get_commandline_payload(config_parser):
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

    return ('', '%s %s\n%s' % (prompt, command, ''.join(get_stdin())))


def create_gist():
    args = parse_arguments()
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(['.gister', os.path.expanduser('~/.gister')])

    if args.vim:
        payload = get_vim_payload()
    else:
        payload = get_commandline_payload(config_parser)

    if args.private:
        url = config_parser.get('gister', 'private_github_url')
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
