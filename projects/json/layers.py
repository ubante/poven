# !/usr/bin/env python

"""
If you have a rediculous json blob, how do you present a slice?

To make it more spicy, let's use poorly named json objects.
"""

from __future__ import print_function

import argparse
import logging
import pprint
import sys

# from pprint import pprint


class JsonWrapper(object):
    """
    It's a little confusing but the key 'play' is only part of an
    element of 'plays'.
    """

    def __init__(self):
        self.j = {}
        self.initialize()

    def initialize(self):
        self.j["plays"] = []
        self.j["stats"] = {}

    def display(self, title=""):
        print("\n{} {}".format("-" * 40, title))
        pprint.PrettyPrinter().pprint(self.j)

    def add_play(self, playname):
        self.j["plays"].append({"play": {"name": playname,
                                         "id": 43,
                                         "serial_str": "alsdfja;sdfj asdf kasdf asfd asdf"},
                                "tasks": []})

    def add_task(self, playname, taskname):
        for play in self.j["plays"]:
            if play["play"]["name"] == playname:
                # newtask = {"hosts": {}, "name": taskname, "id": 100}
                newtask = {"hosts": {}, "task": {"name": taskname, "id": 100}}
                play["tasks"].append(newtask)

    def add_host(self, hostname):
        # Add to plays->play->tasks.  To every task in every play.
        for play in self.j["plays"]:
            for task in play["tasks"]:
                # pass
                # print("here's a task; it has {} hosts".format(len(task["hosts"])))
                host_element = {"atime": 2345, "skipped": True}
                task["hosts"].update({hostname: host_element})
                # print("here's a task; it now has {} hosts".format(len(task["hosts"])))

        # Add to stats.
        self.j["stats"][hostname] = {"time": 1234,
                                     "status": "some status",
                                     "fluff": "asdfjalsdfjasdflk asdflkaj sdlf;jasdlfj asdlkfj"}

    def get_plays(self):
        return self.j["plays"]

    def get_stats(self):
        return self.j["stats"]


def set_logger(verbose_level):
    """
    Initialize the logger.  The verbose_level should be in [0, 1, 2].
    This won't return anything but will reconfigure the root logger.

    :param verbose_level:
    :return:
    """
    if verbose_level >= 2:
        logging_level = logging.DEBUG
    elif verbose_level == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR

    logging.basicConfig(level=logging_level,
                        stream=sys.stdout,
                        format='%(levelname)s - %(message)s')


def create_blob(display=False):
    """
    Blobs are people too.

    :param display: yeah, I did it
    :return:
    """
    blob = JsonWrapper()
    if display:
        blob.display("init")

    blob.add_play("install a thing")
    blob.add_task("install a thing", "do this1")
    blob.add_task("install a thing", "and when time permits, also do that1")
    if display:
        blob.display("add some tasks")

    blob.add_play("compile thing2")
    blob.add_task("compile thing2", "buy an apple")
    blob.add_task("compile thing2", "buy an banana")
    blob.add_task("compile thing2", "eat the foods")
    if display:
        blob.display("add second play")

    blob.add_host("host1.somewhere.com")
    if display:
        blob.display("add first host")

    blob.add_host("api2.somewhere.com")
    blob.add_host("web3.somewhere.com")
    blob.add_host("db4.somewhere.com")
    if display:
        blob.display("add three more hosts")

    return blob


def transform_blob(plays):
    """
    Search the blob for information about the given hostname.  Return a
    list of the found infos.

    We'll ignore the "stats" part of the blob because that has a
    different structure.  And the "if"s are killing me.

    For example this:
    blob["plays"][0]["tasks"][1]["hosts"]["db4.somewhere.com"] =
        {'atime': 2345, 'skipped': True}

    gets translated to:
    { "play": "install a thing",
      "task": "when the time permits, also do that1",
      "results":
        { "atime": 2345,
          "skipped": True
        },
      "hostname": "db4.somewhere.com"
    }

    :param blob:
    :return:
    """
    results = []

    for play in plays:
        playname = play["play"]["name"]
        logging.debug("Playname: {}".format(playname))

        for task in play["tasks"]:
            taskname = task["task"]["name"]
            logging.debug("  Taskname: {}".format(taskname))

            for hostname in task["hosts"]:
                logging.debug("    Hostname: {}".format(hostname))
                output = task["hosts"][hostname]
                logging.debug(output)

                result = {"play": playname, "task": taskname, "results": output,
                          "hostname": hostname}
                results.append(result)

    return results


def find_host_results(task_outputs, hostname):
    """
    Loop through the task_results list looking for hostname.
    :param task_outputs:
    :param hostname:
    :return:
    """
    host_outputs = []

    for output in task_outputs:
        if output["hostname"] == hostname:
            host_outputs.append(output)

    return host_outputs


def display_results(results):
    for result in results:
        print("-" * 40)
        print("play: {}".format(result["play"]))
        print("  task: {}".format(result["task"]))
        pprint.PrettyPrinter(indent=4).pprint(result["results"])


def main():
    parser = argparse.ArgumentParser(description="This is a stub.")
    parser.add_argument("-i", "--important",
                        help="This is the important value that we really need.")
    parser.add_argument("-v", "--verbose", help="Print info/debug.", action="count")
    args = parser.parse_args()

    set_logger(args.verbose)
    logging.debug("Here we go.")

    blob = create_blob(display=False)
    results = transform_blob(blob.get_plays())
    host_results = find_host_results(results, "api2.somewhere.com")
    display_results(host_results)

if __name__ == "__main__":
    main()







