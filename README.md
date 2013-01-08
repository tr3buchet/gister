## gister - make gists!

### examples
* post a public gist on public github:
`cat dog | gister`
* post a secret gist on public github:
`cat dog | gister -s`
* post a public gist on private github deployment:
`cat dog | gister -p`
* post a secret gist on private github deployment:
`cat dog | gister -ps`

### usage
    gister [-h] [-p] [-s] [-v]

    make gists!

    optional arguments:
      -h, --help     show this help message and exit
      -p, --private  put gist on configured enterprise github
      -s, --secret   gist will be secret (not public)
      -v, --vim      gist came from vim, no prompt/history

### config file - .gister
an example configuration file `.gister` is given for you to use. it will be looked for in `~/.gister`. it supports three values:

* prompt - configure your own prompt (using at most user/host/cwd)
* history_file - location of shell history file for command display
* private\_github\_url - if you plan on using `-p/--private` this url needs to be set to the location of your private github deployment

### keyring
i prefer to store my oauth tokens in [keyring](http://pypi.python.org/pypi/keyring) because it's safer than storing it plain text in the .gister file. your python keyring needs to have a section for *github* with a key *token* containing a github oauth token linked to your account. if you use the private github, do the same for *pgithub* and *token*. i added mine like this: [gist](https://gist.github.com/4481060).


TODO:
* add support for vim
