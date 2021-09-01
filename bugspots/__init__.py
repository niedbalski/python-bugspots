from __future__ import print_function
from vcstools import vcs_abstraction

import argparse
import datetime
import math
import re
import sys
import csv

description_regex = re.compile(
    r"^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?)|(([Q|q][F|f])-\d?).*$")


def read_from_file(file_path):
    bugs_string = ''
    with open(file_path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            if bugs_string == '':
                bugs_string = f'({row[0]})'
            else:
                bugs_string = f'{bugs_string}|({row[0]})'
    return bugs_string

def to_seconds_float(timedelta):
    return (timedelta.seconds + timedelta.microseconds / 1E6)


def time_diff(from_t, to):
    return to_seconds_float(from_t - to)


def print_summary(uri, branch, fix_count, days):
    print("""\n\nScanning %s repo, branch:%s\n"""
          """Found %d bugfix commits in the last %d days"""
          % (uri, branch, fix_count, days))


def get_current_vcs(path):
    if path is None:
        path = '.'
    for vcs_type in vcs_abstraction.get_registered_vcs_types():
        vcs = vcs_abstraction.get_vcs(vcs_type)
        if vcs.static_detect_presence(path):
            return vcs(path)
    raise Exception("Not found a valid VCS repository")


def get_fix_commits(branch, days, path='.'):
    vcs = get_current_vcs(path)

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
    commits = get_fix_commits(options.branch, options.days, options.path)

    if not commits:
        print(
            f"Did not find commits matching search criteria for repo at: {options.path} branch: {options.branch}")
        return None

    print_summary(options.path, options.branch, len(commits), options.days)

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
    code_hotspots = get_code_hotspots(options)
    if code_hotspots is not None:
        for factor, filename in code_hotspots:
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

    parser.add_argument("--bugsFile",
                        help='Use a file with list of bugs',
                        type=str,
                        metavar="file")

    parser.add_argument("--paths",
                        help='Provide repository paths to look into',
                        type=str,
                        nargs="*",
                        metavar="paths")

    return parser.parse_args()


def main():
    options = parse_options()
    if options.bugsFile is not None:
        bugs_list = read_from_file(options.bugsFile)
        global description_regex
        description_regex = re.compile(f'^.*({bugs_list}).*$')
    for path in options.paths:
        option = options
        option.path = path
        print_code_hotspots(option)


if __name__ == '__main__':
    main()
