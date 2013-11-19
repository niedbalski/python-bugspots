#!/usr/bin/env python
# coding: utf-8

#-----------------------------------------------------------------------------
#  Copyright (c) Jorge Niedbalski R. <jnr@pyrosome.org>
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

import argparse
import vcs.cli
import datetime
import math
import re
import sys

_desc_regex = re.compile("^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?).*$")


def to_seconds_float(timedelta):
    return (timedelta.seconds + timedelta.microseconds / 1E6)


def time_diff(from_t, to):
    return to_seconds_float(from_t - to)


def print_summary(uri, branch, fix_count, days):
    print >> sys.stdout, """\n\nScanning %s repo, branch:%s\n""" \
                         """Found %d bugfix commits on the last %d days""" \
                         % (uri, branch, fix_count, days)


def get_fix_commits(client, branch, days):

    def changelogs(days_ago):
        """
        """
        changelogs = [change for change in client.get_changesets(client.repo)]

        for change in changelogs:
            if change.branch == branch and \
                    _desc_regex.search(change.message):
                if change.date >= days_ago:
                    yield((change.message, change.date, change.affected_files))

    days_ago = (datetime.datetime.now() - datetime.timedelta(days=days))

    fixes = []
    for change in changelogs(days_ago):
        fixes.append(change)
    return fixes


def get_code_hotspots(options):
    """
    """
    client = vcs.cli.ChangesetCommand()
    commits = get_fix_commits(client, options.branch, options.days)

    if not commits:
        print >> sys.stdout, "Not found commits matching search criteria"
        sys.exit(-1)

    #show the summary of this repo scan
    print_summary(client.repo.path, options.branch, len(commits), options.days)

    (last_message, last_date, last_files) = commits[-1]
    current_dt = datetime.datetime.now()

    print >> sys.stdout, "\nFixes\n%s" % ('-' * 80)

    hotspots = {}

    for message, date, files in commits:
        this_commit_diff = time_diff(current_dt, date)
        last_commit_diff = time_diff(current_dt, last_date)

        factor = this_commit_diff / last_commit_diff

        factor = 1 - factor

        for filename in files:
            if not filename in hotspots:
                hotspots[filename] = 0
            try:
                hotspot_factor = 1 / (1 + math.exp((-12 * factor) + 12))
            except:
                pass

            hotspots[filename] += hotspot_factor

        print >> sys.stdout, "      -%s" % message

    sorted_hotspots = sorted(hotspots, key=hotspots.get, reverse=True)

    print >> sys.stdout, "\nHotspots\n%s" % ('-' * 80)

    for k in sorted_hotspots[:options.limit]:
        yield (hotspots[k], k)


def print_code_hotspots(options):
    for factor, filename in get_code_hotspots(options):
        print >> sys.stdout, "      %.2f = %s" % (factor, filename)
    print '\n'


def parse_options():
    parser = argparse.ArgumentParser(description=
            'A Python based implementation of the bug' \
            'prediction algorithm proposed by Google')

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
                      default='default',
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

