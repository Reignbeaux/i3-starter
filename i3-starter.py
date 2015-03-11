# Outline

# start dmenu, get selected application
# save current workspace by using "i3-msg -t ..."
# start app using "i3-msg exec <app>"
# get the pid using "pidof <app>"

    # now list all windows of that process using this:
    # http://stackoverflow.com/questions/2250757/is-there-a-linux-command-to-determine-the-window-ids-associated-with-a-given-pro
    # when there is a new window, queck it's workspace
    # when the window isn't on saved workspace, then move it there

    # repeat for x seconds every y seconds

import subprocess


def run_dmenu():
    path_process = subprocess.Popen(['dmenu_path'], stdout=subprocess.PIPE)
    dmenu_process = subprocess.Popen(['dmenu'], stdin=path_process.stdout, stdout=subprocess.PIPE)

    path_process.wait()
    dmenu_process.wait()

    return dmenu_process.communicate()[0].decode("utf-8")

def active_workspace():
    pass


application = run_dmenu()

current_workspace = subprocess.check_output('i3-msg', '-t', 'get_workspaces');



#dmenu_path | dmenu "$@"