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
* post an anonymous gist on public github
`cat dog | gister -a`
* post an anonymous and secret gist on public github
` cat dog | gister -as`
* post an anonymous gist on private github deployment
`cat dog | gister -ap`
* post an anonymous and secret gist on private github deployment
` cat dog | gister -aps`

### usage
    gister [-h] [-p] [-s] [-a] [-v]

    make gists!

    optional arguments:
      -h, --help       show this help message and exit
      -p, --private    put gist on configured enterprise github
      -s, --secret     gist will be secret (not public)
      -a, --anonymous  gist will be anonymous
      -v, --vim        gist came from vim, no prompt/history

### install
fix weird hgtools dependency issue: `pip install hgtools`
clone the repo and `python setup.py install`

### config file - .gister
an example configuration file `.gister` is given for you to use. it will be looked for in `~/.gister`. it supports three values:

* prompt - configure your own prompt (using variables username/hostname/cwd)
* history_file - location of shell history file for command display
* private\_github\_url - if you plan on using `-p/--private` this url needs to be set to the location of your private github deployment

### keyring
i prefer to store my oauth tokens in [keyring](http://pypi.python.org/pypi/keyring) because it's safer than storing it plain text in the .gister file. your python keyring needs to have a section for *github* with a key *token* containing a github oauth token linked to your account. if you use the private github, do the same for *pgithub* and *token*. i added mine like this: [gist](https://gist.github.com/4481060).

### github oauth tokens
here is a [gist](http://gist.github.com/4482201) of the process by which a token is acquired. the returned dict will have a *token* key in it denoting your token. you can also manage your tokens by managing your github account and selecting *Applications*.

### using with vim
I added the following to [my .vimrc](http://github.com/tr3buchet/conf/blob/master/.vimrc) to interact with gister:

    " ------- gist making! --------------------------------
    fun Gister(...)
      let gister_call = "gister -v"
      for flag in a:000
        let gister_call = gister_call . " " . flag
      endfor
      let result = system(gister_call, expand("%:t") . "\n" . getreg("\""))
      echo result
    endfun
    " public gist on github from selection or single line
    vnoremap <F9> y:call Gister()<cr>
    nnoremap <F9> yy:call Gister()<cr>

    " secret gist on github from selection or single line
    vnoremap <F10> y:call Gister("-s")<cr>
    nnoremap <F10> yy:call Gister("-s")<cr>

    " public gist on private github from selection or single line
    vnoremap <F11> y:call Gister("-p")<cr>
    nnoremap <F11> yy:call Gister("-p")<cr>

    " secret gist on private github from selection or single line
    vnoremap <F12> y:call Gister("-p", "-s")<cr>
    nnoremap <F12> yy:call Gister("-p", "-s")<cr>
    " ------- end pastie.org ---------------------------
