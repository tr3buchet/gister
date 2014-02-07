====================
gister - make gists!
====================


examples
========
* post a public gist on public github:
  ``cat doge | gister``

* post a secret gist on public github:
  ``cat doge | gister -s``

* post a public gist on private github deployment:
  ``cat doge | gister -p``

* post a secret gist on private github deployment:
  ``cat doge | gister -ps``

* post an anonymous gist on public github:
  ``cat doge | gister -a``

* post an anonymous and secret gist on public github:
  ``cat doge | gister -as``

* post an anonymous gist on private github deployment:
  ``cat doge | gister -ap``

* post an anonymous and secret gist on private github deployment:
  ``cat doge | gister -aps``

* post a public gist on public github with a command:
  ``cat doge | tail -n4 | gister -c "cat doge | tail -n4"``

usage
=====

.. code:: console

    gister [-h] [-p] [-s] [-a] [-c COMMAND] [-v]

    make gists!

    optional arguments:
      -h, --help            show this help message and exit
      -p, --private         put gist on configured enterprise github
      -s, --secret          gist will be secret (not public)
      -a, --anonymous       gist will be anonymous
      -c COMMAND, --command COMMAND
      -v, --vim             gist came from vim, no prompt/history


install
=======
* ``pip install gister`` or clone the repo and ``python setup.py install``

config file - .gister
=====================
an example configuration file ``.gister`` is given for you to use.
it will be looked for in ``~/.gister``. it supports these values:

* public_oauth - your public github oauth token (not necessary
  for anonymous gists)
* private_oauth - your private github oauth token (if you plan on
  using private github) (not necessary for anonymous gists)
* prompt - configure prompt that is displayed when using the
  ``-c/--command`` option
* public_github_url - this defaults to the url for public github
* private_github_url - if you plan on using ``-p/--private``
  this url needs to be set to the location of your private github
  deployment


github oauth tokens
===================
gister can be used with no oauth tokens, but can only create anonymous
gists by specifying the ``-a/--anonymous`` flag

you can manage your github oauth tokens here by visiting
`applications <https://github.com/settings/applications>`__ in your
account settings

you can also create an oauth token using the github api as I did in
this `gist <http://gist.github.com/4482201>`__


keyring
=======
use of `keyring <http://pypi.python.org/pypi/keyring>`__ is optional.
it allows you store your oauth tokens in a safer place than the
``~/.gister`` config file

if you wish to use keyring, specify your ``public_oauth`` and/or
``public_oauth`` tokens as follows:

.. code:: console

    [gister]
    private_oauth = KEYRING
    public_oauth = KEYRING

gister will look for a section called *gister* with keys *public_oauth*
and/or *private_oauth* containing a github oauth tokens linked to your
public github and/or private github account. an
`example <https://gist.github.com/4481060>`__ of adding keys to python
keyring


using with vim
==============
I added the following to
`my .vimrc <http://github.com/tr3buchet/conf/blob/master/.vimrc>`__
to interact with gister:

.. code:: vim

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
