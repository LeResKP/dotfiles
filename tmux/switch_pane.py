#!/usr/bin/env python

import subprocess
from optparse import OptionParser


# We want to use the first window to manage all the others.
SWITCHER_WINDOW_ID = 0


def bash(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return process.communicate()[0].strip()


def get_window_ids():
    s = bash('tmux list-window -F "#I"')
    lis = filter(bool, s.split('\n'))
    return map(int, lis)


def get_current_window_id():
    return int(bash('tmux display-message -p "#I"'))


def get_current_pane_id():
    return int(bash("tmux list-pane -F '#P:#{pane_active}' | grep '1$' | cut -d ':' -f 1"))


def parse_title():
    """Parse the title of the window

    We use the title to store the pane used for the switch and the window which
    is display in the switch.
    """
    s = get_window_name()
    lis = s.split('@')
    assert lis
    name = lis[0]
    pane_id = None
    window_id = None
    if len(lis) > 1:
        pane_id = int(lis[1])
    if len(lis) > 2:
        window_id = int(lis[2])
    return name, pane_id, window_id


def get_window_name():
    return bash('tmux display-message -p "#W"')


def rename_window(pane_id, window_id):
    name = get_window_name().split('@')[0]
    new_name = filter(lambda x: x is not None, [name, pane_id, window_id])
    bash('tmux rename-window "%s"' % '@'.join(map(str, new_name)))


def get_pane_ids():
    s = bash("tmux list-panes -F '#P'")
    lis = s.split('\n')
    return map(int, lis)


def get_next_window_id(window_id):
    """Return the id of the next window to display
    """
    window_ids = get_window_ids()
    for i in window_ids:
        if i > window_id:
            return i

    for i in window_ids:
        if i not in [SWITCHER_WINDOW_ID, window_id]:
            return i

    return None


def new_window():
    bash('tmux new-window -d')


def break_pane(pane_id):
    bash('tmux break-pane -d -t %i' % pane_id)


def join_pane(window_id, set_current=True):
    if set_current:
        bash('tmux join-pane -s %i -h' % window_id)
    else:
        bash('tmux join-pane -d -s %i -h' % window_id)


def select_pane(pane_id):
    bash('tmux select-pane -t %i' % pane_id)


def select_switcher_window():
    bash('tmux select-window -t %i' % SWITCHER_WINDOW_ID)


def toggle(force_window_id=None):
    cur_window_id = get_current_window_id()
    name, pane_id, window_id = parse_title()
    pane_ids = get_pane_ids()
    if pane_ids and pane_id in pane_ids:
        break_pane(pane_id)
        if not force_window_id:
            return

    if cur_window_id == SWITCHER_WINDOW_ID:

        if force_window_id:
            next_window_id = force_window_id
        elif window_id in get_window_ids():
            next_window_id = window_id
        else:
            next_window_id = get_next_window_id(cur_window_id)

        if not next_window_id:
            new_window()
            next_window_id = get_next_window_id(cur_window_id)
            assert next_window_id

        before_pane_id = get_current_pane_id()
        join_pane(next_window_id)
        pane_id = get_current_pane_id()
        select_pane(before_pane_id)
        rename_window(pane_id, next_window_id)

    else:
        window_id = get_current_window_id()
        select_switcher_window()
        toggle(window_id)


def display_next_window():
    cur_window_id = get_current_window_id()
    name, pane_id, window_id = parse_title()
    pane_ids = get_pane_ids()
    if not pane_id or pane_id not in pane_ids:
        toggle()
        return

    if cur_window_id == SWITCHER_WINDOW_ID:
        next_window_id = get_next_window_id(window_id)

        if not next_window_id:
            return

        set_current = (get_current_pane_id() == pane_id)
        break_pane(pane_id)
        join_pane(next_window_id, set_current=set_current)
        rename_window(pane_id, next_window_id)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--toggle", action="store_true", dest="toggle",
                      default=False,
                      help="toggle the pane")

    (options, args) = parser.parse_args()
    if options.toggle:
        try:
            toggle()
        except Exception, e:
            print e
            raise
        exit(0)

    try:
        display_next_window()
    except Exception, e:
        print e
        raise
    exit(0)
