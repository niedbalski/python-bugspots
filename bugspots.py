#!/usr/bin/env python
# coding: utf-8

#-----------------------------------------------------------------------------
#  Copyright (c) Jorge Niedbalski R. <jnr@pyrosome.org>
#
#  Mercurial extension for get the Bug Prediction Algorithm suggested by
#  google. References:
#   - http://google-engtools.blogspot.com/2011/12/bug-prediction-at-google.html
#
#  How to install:
#  ===============
#  Add the following lines to your .hgrc file into your extensions section:
#  [extensions]
#  bugspots=/path/to/this/file
#
#  How to use:
#  ==========
#
#  hg bugspots repo_path
#
#  License:
#  ========
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING.BSD, distributed as part of this software.
#-----------------------------------------------------------------------------

import datetime
import math
import re
import sys

_desc_regex = re.compile("^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?).*$")


def get_fixes(repo, days, branch):

    def changelogs(days):
        changelogs = repo.changelog

        for change in changelogs:
            ctx = repo.changectx(change)

            if ctx.branch() == branch and \
                    _desc_regex.search(ctx.description()):
                date = datetime.datetime.fromtimestamp(ctx.date()[0])

                if date >= days_ago:
                    yield((ctx.description(), ctx.date(), ctx.files()))

    days_ago = (datetime.datetime.now() - datetime.timedelta(days=days))

    fixes = []
    for change in changelogs(days_ago):
        fixes.append(change)

    return fixes


def to_seconds_float(timedelta):
    return (timedelta.seconds + timedelta.microseconds / 1E6)


def time_diff(from_t, to):
    return to_seconds_float(from_t - datetime.datetime.fromtimestamp(to))


def print_summary(url, branch, fixes, days):
    print >> sys.stdout, """\n\nScanning %s repo, branch:%s\n""" \
                         """Found %d bugfix commits on the last %d days""" \
                         % (url, branch, fixes, days)


def generate_hotspots(repo, opts):

    (limit, days, branch) = opts.values()
    fixes = get_fixes(repo, days, branch)
    last_fix_date = fixes[-1][1][0]

    now = datetime.datetime.now()

    #show the summary of this repo scan
    print_summary(repo.url(), branch, len(fixes), days)
    print >> sys.stdout, "\nFixes\n%s" % ('-' * 80)

    hotspots = {}
    for description, date, files in fixes:
        fix_diff = time_diff(now, date[0])
        las_diff = time_diff(now, last_fix_date)

        factor = fix_diff / las_diff

        for filename in files:
            factor = 1 - factor

            if not filename in hotspots:
                hotspots[filename] = 0
            try:
                hotspot_factor = 1 / (1 + math.exp(-12 * factor) + 12)
            except:
                pass

            hotspots[filename] += hotspot_factor

        print >> sys.stdout, "      -%s" % description

    sorted_hotspots = sorted(hotspots, key=hotspots.get, reverse=True)

    print >> sys.stdout, "\nHotspots\n%s" % ('-' * 80)

    for k in sorted_hotspots[:int(opts['limit'])]:
        yield (hotspots[k], k)


def print_hotspots(ui, repo, node, **opts):
    for factor, filename in generate_hotspots(repo, opts):
        print >> sys.stdout, "      %.2f = %s" % (factor, filename)
    print '\n'


cmdtable = {
    'bugspots': (
        print_hotspots, [('d', 'days', 30, 'Days ago to calculate'),
                         ('b', 'branch', 'default', 'Specify branch'),
                         ('l', 'limit', 10, 'Amount of hotspots to return')],
        '[options] REV')
}

testedwith = '2.0.2'
