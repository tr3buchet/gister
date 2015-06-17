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
from __future__ import print_function
import argparse
import json
import os
import re
import requests
import sys


# keyring is optional
try:
    import keyring
except ImportError:
    keyring = None
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


def parse_arguments():
    parser = argparse.ArgumentParser(description='make gists!')
    parser.add_argument('-p', '--private', action='store_true',
                        help='put gist on configured enterprise github')
    parser.add_argument('-a', '--anonymous', action='store_true',
                        help='gist will be anonymous '
                             'even if you have oauth configured')
    parser.add_argument('-c', '--command', action='store',
                        help='command to prepend to gist')
    parser.add_argument('-v', '--vim', action='store_true',
                        help='gist came from vim, no prompt/history')
    parser.add_argument('file', nargs='*', action='store',
                        help='name of file(s) to gist')
    parser.add_argument('-d', '--description', action='store',
                        default=('created by '
                                 'https://github.com/tr3buchet/gister'),
                        help='description of the file')
    return parser.parse_args()


def parse_config():
    config_parser = ConfigParser.RawConfigParser(
        defaults={'prompt': '[%(username)s|%(hostname)s %(cwd)s]%%',
                  'public_github_url': 'https://api.github.com',
                  'private_github_url': None,
                  'public_oauth': None,
                  'private_oauth': None})
    # read from ~/.gister if it exists else use defaults
    config_parser.read(os.path.expanduser('~/.gister'))
    if config_parser.has_section('gister'):
        items = config_parser.items('gister')
    else:
        items = config_parser.items('DEFAULT')
    config = {}
    for name, value in items:
        # add in tokens from keyring if necessary
        if 'oauth' in name and value == 'KEYRING':
            if keyring:
                value = keyring.get_password('gister', name)
            else:
                raise Exception('KEYRING specified in config but '
                                'python keyring package not available')
        config[name] = value
    return config


def get_stdin():
    stdin_lines = []
    for line in sys.stdin:
        stdin_lines.append(line)
    return ''.join(stdin_lines)


def get_filedata(filenames):
    filedata = {}
    for filename in filenames:
        try:
            with open(filename) as f:
                filedata[filename.split('/')[-1]] = {'content': f.read()}
        except IOError as e:
            print(e)
            sys.exit(1)
    return filedata


def get_vim_payload():
    lines = [line for line in sys.stdin]
    filename = lines.pop(0).rstrip()
    return {filename: {'content': ''.join(lines)}}


def get_commandline_payload(prompt=None, command=None, filenames=None):
    if filenames:
        return get_filedata(filenames)
    if not (prompt and command):
        return {'': {'content': get_stdin()}}
    try:
        username = os.environ['LOGNAME']
        hostname = os.uname()[1]
        cwd = re.sub('/home/%s' % username, '~', os.getcwd())
        prompt = prompt % {'username': username,
                           'hostname': hostname, 'cwd': cwd}
    except:
        prompt = ''

    if prompt:
        prompt_command = '%s %s\n' % (prompt, command)
    else:
        prompt_command = ''

    return {'': {'content': '%s%s' % (prompt_command, get_stdin())}}


def get_headers(token):
    return {'Authorization': 'token %s' % token}


def private_gist_url(conf, anonymous):
    if not conf.get('private_github_url'):
        raise Exception('private_github_url must be set in ~/.gister '
                        'to create a gist on private github.\n'
                        'see https://github.com/tr3buchet/gister'
                        '#config-file---gister for more info on config '
                        'settings or create a gist on public github by '
                        'not specifying the -p flag')
    return conf.get('private_github_url')


def create_gist(anonymous=False, command=None, description=None,
                file=None, private=False, vim=False):
    conf = parse_config()

    if vim:
        payload = get_vim_payload()
    else:
        payload = get_commandline_payload(conf.get('prompt'), command, file)
    if private:
        url = private_gist_url(conf, anonymous)
        token = None if anonymous else conf.get('private_oauth')
    else:
        url = conf.get('public_github_url')
        token = None if anonymous else conf.get('public_oauth')
    headers = get_headers(token) if token else None
    payload = {'description': description,
               'public': False,
               'files': payload}
#               'files': dict((k, {'content': v}) for k, v in payload)}
#               'files': {payload[0]: {'content': payload[1]}}}

    r = requests.post(url + '/gists', data=json.dumps(payload),
                      headers=headers)
    r.raise_for_status()
    return r.json()['html_url']


def print_gist_url():
    args = parse_arguments()

    print(create_gist(args.anonymous, args.command, args.description,
                      args.file, args.private, args.vim))
