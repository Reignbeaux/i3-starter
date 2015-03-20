import subprocess
import json
import time
import re
import psutil,os


def select_application():
    # pass output of "dmenu_path" to dmenu
    path_process = subprocess.Popen(['dmenu_path'], stdout=subprocess.PIPE)
    dmenu_process = subprocess.Popen(['dmenu'], stdin=path_process.stdout, stdout=subprocess.PIPE)

    path_process.wait()
    dmenu_process.wait()

    return dmenu_process.communicate()[0].decode("utf-8").rstrip()


def get_active_workspace():
    workspaces_json = subprocess.check_output(['i3-msg', '-t', 'get_workspaces'])
    workspaces = json.loads(workspaces_json.decode("utf-8"))

    for workspace in workspaces:
        if workspace["focused"]:
            return workspace["num"]


def start_application(application):
    process = subprocess.Popen([application])

    # pids = subprocess.check_output(['pidof', application])
    return process.pid


def check_i3_windows(process_id, workspace):
    end_time = time.time() + 23  # time + 23 seconds

    old_nodes = []

    windows_json = subprocess.check_output(['i3-msg', '-t', 'get_tree'])
    windows = json.loads(windows_json.decode('utf-8'))
    read_node(old_nodes, windows)

    while time.time() < end_time:
        time.sleep(0.1)

        windows_json = subprocess.check_output(['i3-msg', '-t', 'get_tree'])
        windows = json.loads(windows_json.decode('utf-8'))

        nodes_to_compare = []
        # fill nodes_to_compare with current windows
        read_node(nodes_to_compare, windows)

        # compare to get just added windows
        new_nodes = get_new_nodes(old_nodes, nodes_to_compare)

        if old_nodes:
            for new_node in new_nodes:
                # check if new node depends to the pid
                output = subprocess.check_output(['xwininfo', '-id', str(new_node['window']), '-wm']).decode("utf-8")

                pattern = re.compile(r'Process\sid:\s([0-9]+)')
                match = pattern.search(output)

                pid_of_window = match.groups()[0]

                # sometimes, this is not working, since the started process id doesn't match the window's id!
                # this can happen when software is using multiple processes
                # if that's the case, parent and child processes have to be considered as well

                pid_list = [process_id]

                get_parents(process_id, pid_list)
                children_pids = psutil.Process(process_id).get_children(recursive=True)
                pid_list.extend(map(lambda process: process.pid, children_pids))

                if int(pid_of_window) in pid_list:
                    print("Moving '{}' to workspace '{}'".format(new_node['window'], workspace))
                    subprocess.Popen(['i3-msg', '[id="' + str(new_node['window']) + '"]', 'move', 'to', 'workspace', str(workspace)])

                    #   for node in new_nodes:
                    #       if 'window' in node and 'class' in node:
                    #           print('Window-ID: {}; Class: {}'.format(node['window'], node['class']))
                    #       else:
                    #           print('Unspecified')

        old_nodes = nodes_to_compare


def get_parents(current_pid, pid_list):
    new_pid = psutil.Process(current_pid).parent()

    if new_pid is None:
        return
    else:
        pid_list.append(new_pid.pid)
        get_parents(new_pid.pid, pid_list)


def get_new_nodes(nodes1, nodes2):
    check = set([(d['class'], d['window']) for d in nodes1])
    return [d for d in nodes2 if (d['class'], d['window']) not in check]


def read_node(nodes_list, node_to_add):
    new_node = {}

    if 'window' in node_to_add and 'window_properties' in node_to_add:
        new_node['window'] = node_to_add['window']
        new_node['class'] = node_to_add['window_properties']['class']

        nodes_list.append(new_node)

    if "nodes" in node_to_add:
        for node in node_to_add['nodes']:
            read_node(nodes_list, node)


selected_application = select_application()
active_workspace = get_active_workspace()
pid = start_application(selected_application)

check_i3_windows(pid, active_workspace)
