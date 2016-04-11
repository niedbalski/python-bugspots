#!/usr/bin/env python
# coding: utf-8
#-----------------------------------------------------------------------------
#  Copyright (c) Jorge Niedbalski R. <jnr@metaklass.org>
#
#  Tool for calculate Bug Prediction Algorithm suggested by
#  google. References:
#   - http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html
#
#  How to install:
#  ===============
#
#  $ pip install bug-spots
#
#  How to use:
#  ==========
#
#  $ mv to repo_director7
#  $ bugspots ( --help for other options )
#
#  License:
#  ========
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING.BSD, distributed as part of this software.
#-----------------------------------------------------------------------------

from __future__ import print_function

import argparse
import datetime
import math
import re
import sys

from vcstools import vcs_abstraction

description_regex = re.compile(
    "^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?).*$")


def to_seconds_float(timedelta):
    return (timedelta.seconds + timedelta.microseconds / 1E6)


def time_diff(from_t, to):
    return to_seconds_float(from_t - to)


def print_summary(uri, branch, fix_count, days):
    print("""\n\nScanning %s repo, branch:%s\n"""
          """Found %d bugfix commits on the last %d days"""
          % (uri, branch, fix_count, days))


def get_current_vcs(path="."):
    for vcs_type in vcs_abstraction.get_registered_vcs_types():
        vcs = vcs_abstraction.get_vcs(vcs_type)
        if vcs.static_detect_presence(path):
            return vcs(path)
    raise Exception("Not found a valid VCS repository")


def get_fix_commits(branch, days):
    vcs = get_current_vcs()

    def get_changesets(days_ago):
        current_branch = vcs.get_current_version_label()

        if current_branch != branch:
            vcs._do_checkout(branch)

        for log in vcs.get_log():
            (date, message, id) = (log['date'], log['message'],
                                   log['id'])

            commit_date = date.replace(tzinfo=None)
            if commit_date >= days_ago and \
               description_regex.search(message):
                yield((message, commit_date, vcs.get_affected_files(id)))

    days_ago = (datetime.datetime.now() - datetime.timedelta(days=days))

    fixes = []
    for change in get_changesets(days_ago):
        fixes.append(change)
    return fixes


def get_code_hotspots(options):
    commits = get_fix_commits(options.branch, options.days)

    if not commits:
        print("Not found commits matching search criteria")
        sys.exit(-1)

    print_summary(".", options.branch, len(commits), options.days)

    (last_message, last_date, last_files) = commits[-1]
    current_dt = datetime.datetime.now()

    print("\nFixes\n%s" % ('-' * 80))

    hotspots = {}

    for message, date, files in commits:
        this_commit_diff = time_diff(current_dt, date)
        last_commit_diff = time_diff(current_dt, last_date)

        factor = this_commit_diff / last_commit_diff

        factor = 1 - factor

        for filename in files:
            if filename not in hotspots:
                hotspots[filename] = 0
            try:
                hotspot_factor = 1/(1+math.exp((-12 * factor) + 12))
            except:
                pass

            hotspots[filename] += hotspot_factor

    print("      -%s" % message)

    sorted_hotspots = sorted(hotspots, key=hotspots.get, reverse=True)

    print("\nHotspots\n%s" % ('-' * 80))
    for k in sorted_hotspots[:options.limit]:
        yield (hotspots[k], k)


def print_code_hotspots(options):
    for factor, filename in get_code_hotspots(options):
        print("      %.2f = %s" % (factor, filename))
    print("\n")


def parse_options():
    parser = argparse.ArgumentParser(
        description="""A Python based implementation of the bug"""
        """prediction algorithm proposed by Google""")

    parser.add_argument("--days",
                        default=30,
                        help='Days ago to compute bug factor',
                        type=int,
                        metavar='days')

    parser.add_argument("--limit",
                        default=10,
                        help='Max amount of results to show',
                        type=int,
                        metavar='limit')

    parser.add_argument("--branch",
                        default='master',
                        help='Use a specific branch',
                        type=str,
                        metavar='branch')

    args = parser.parse_args()
    return args


def main():
    options = parse_options()
    print_code_hotspots(options)

if __name__ == '__main__':
    main()
