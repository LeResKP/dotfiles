#!/usr/bin/env python

import subprocess
from optparse import OptionParser


def bash(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return process.communicate()[0].strip()


def get_window_ids():
    s = bash('tmux list-window -F "#I"')
    lis = filter(bool, s.split('\n'))
    return map(int, lis)


def get_window_name():
    return bash('tmux display-message -p "#W"')


def get_current_id():
    s = get_window_name()
    lis = s.split('@')
    cid = int(bash('tmux display-message -p "#I"'))
    if len(lis) == 2:
        v = int(lis[1])
        if v == cid:
            return v + 1
        return v
    elif len(lis) == 1:
        return  cid + 1

    raise Exception('Error while getting current id')


def get_next_id():
    ident = get_current_id()
    ids = get_window_ids()

    for i in ids:
        if i > ident:
            return i
    return ids[1]


def rename_window(ident):
    name = get_window_name().split('@')[0]
    bash('tmux rename-window "%s@%i"' % (name, ident))


def get_nb_pane():
    return int(bash('tmux list-panes | wc -l'))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--toggle", action="store_true", dest="toggle",
                      default=False,
                      help="toggle the pane")

    (options, args) = parser.parse_args()
    if options.toggle:
        if get_nb_pane() > 1:
            bash('tmux break-pane -d')
            exit(0)

    if get_nb_pane() > 1:
        next_id = get_next_id()
        cid = get_current_id()
        bash('tmux break-pane -d')
        bash('tmux join-pane -s %i -h' % (next_id))
        rename_window(next_id)
    else:
        cid = get_current_id()
        bash('tmux join-pane -s %i -h' % (cid))
        rename_window(cid)

