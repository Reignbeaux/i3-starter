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