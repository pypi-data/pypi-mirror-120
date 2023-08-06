[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pygitgrab 

grab only certain information from remote git repo and store them local

# general information

`pygitgrab` is not intended to be a replacement for git and it's capabilities.
`pygitgrab` will not do housekeeping, meaning maintaing the local directory content like syncing or such a like.
in case remote files or folders are dropped it is required to clean local folders manually.

# What's new ?

Check
[`CHANGELOG`](https://github.com/kr-g/pygitgrab/blob/master/CHANGELOG.md)
for latest ongoing, or upcoming news

# installation

the module is on [pypi](https://pypi.org/kr-g/pygitgrab) and can be installed with pip

# run from cmd line

    python3 -m pygitgrab -h
    
    python3 -m pygitgrab -u user_name # user_name is optional, will prompt for password
    
    # use credits file for github authentication 
    python3 -m pygitgrab -c 
    
    # use other .pygg files, here web.pygg, and cntrl.pygg
    python3 -m pygitgrab -u user_name -f web -f cntrl   
    
    # use remote .pygg files, use ref for selecting the github tag
    # if ref=master fails try ref=main or any valid tag, no detail error message from github
    python3 -m pygitgrab -u user_name -url https://github.com/kr-g/pygitgrab/cntrl.pygg?ref=master
    
    
github offers downloading for unauthenticed users only within certain rate limits [https://developer.github.com/v3/rate_limit/](https://developer.github.com/v3/rate_limit/).
in case downloading a bunch of serveral project files it is required to authenticate. (see also deprecation note of GitHub at the end of this document)


# pygg.cfg structure

`pygitgrab` loads a `pygg.cfg` config file from the current directory to perform the required steps.
the structure is as following:

    [repo_alias]
    # url to repo
    url=https://github.com/_owner_name_/_repo_name_
    # optional version to check out, defaults to 'master'
    tag=master
    # optional destination folder given, defaults to 'repo_alias' (name of this section in the config file)
    # pull_alias is just a name for the pull task
    pull_alias="*.py", "new_folder"
    # sample for pulling a license and store them at a different place
    license="LICENSE.md", "LICENSE/a_license.MD"
    

`pygitgrab` will create the directory structure as found in the remote git repo when pattern matching is used.

`pygitgrab` uses python [configparser](https://docs.python.org/3/library/configparser.html).
general information regarding the syntax can be found there.

# other pygg files

when calling with parameter `-f cfgfile` the configuration is read from there instead of `pygg.cfg` config file.
if a file extension is missing an extension `.pygg` is added as default.


# cmd line parameter

    usage: python3 -m pygitgrab [options]

    grab files from remote git repo.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version info and exit
      -L, --license         show license info and exit
      -s, --simulate        dry run, do not download files
      -f FILE, --file FILE  name of pygg file to read, adds as '.pygg' extension
                            if missing
      -url URL              name of remote pygg file on github to read, adds as
                            '.pygg' extension if missing
      -u [USER], --user [USER]
                            authenticate with user, no user for prompt. create a
                            personal access token in your github settings instead
                            of using a password. unauthenticated users have a
                            lower rate for downloading from github.
                            https://developer.github.com/v3/rate_limit/
      -c [CREDITS], --credits [CREDITS]
                            read user and personal token from a file instead of
                            prompting. make sure to put the file not in git
                            controlled directory, (default: '~/pygg.credits.txt')

    for more information refer to https://github.com/kr-g/pygitgrab


# 3rd party licenses

when you move 3rd party license information into the special folder 'LICENSE' the cmd `python3 -m pygitgrab -L` will produce a summary of all found licences together with a 'LICENSE' file found in the current directory. use as `python3 -m pygitgrab -L > LICENSES` to produce a summary plain text file.


# limitations

works only with github as backend.


# deprecation of user and password authentication 

github recently [announced](https://developer.github.com/changes/2019-11-05-deprecated-passwords-and-authorizations-api/) to discontinue user/password authentication soon.

use a [personal access token](https://developer.github.com/v3/auth/#basic-authentication) instead of a password.

create your personal access token under [GitHub developer settings](https://github.com/settings/tokens) as described in the help for [creating a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

the minimum required scope(s) of the token is `public_repo`


# using a credits file instead of manual authentication
                              
with the option `-c` or `--credits` pygitgrab reads the github user credits from a file.
                              
this defaults to `~/pygg.credits.txt` in the home directory if not specified.
dont put it under a git controlled directory to prevent exposing your sensitive data.
                              
the file itself should have 2 lines the following structure:
                              
    user-name
    user-token

it can have blank lines at any place.
                              
