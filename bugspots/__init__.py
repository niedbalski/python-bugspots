from __future__ import print_function
from vcstools import vcs_abstraction

import argparse
import datetime
import math
import re
import csv

description_regex = re.compile(
    r"^.*([B|b]ug)s?|([f|F]ix(es|ed)?|[c|C]lose(s|d)?)|(([Q|q][F|f])-\d?).*$")

markdown_output = str(
    f'# Bughotspots Report\n### Generated at {datetime.datetime.now()}\n```console')


def output_report(content):
    print(content)
    global markdown_output
    if markdown_output is not None:
        markdown_output += f'\n{content}'


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
    output_report(f"""\n\nScanning {uri} repo, branch:{branch}\n"""
                  f"""Found {fix_count} bugfix commits in the last {days} days""")


def get_current_vcs(path):
    if path is None:
        path = '.'
    for vcs_type in vcs_abstraction.get_registered_vcs_types():
        vcs = vcs_abstraction.get_vcs(vcs_type)
        if vcs.static_detect_presence(path):
            return vcs(path)
    raise Exception("Did not find a valid VCS repository")


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
                yield(message, commit_date, vcs.get_affected_files(id))

    days_ago = (datetime.datetime.now() - datetime.timedelta(days=days))

    fixes = []
    for change in get_changesets(days_ago):
        fixes.append(change)
    return fixes


def get_code_hotspots(options):
    commits = get_fix_commits(options.branch, options.days, options.path)

    if not commits:
        output_report(
            f"No commits found with matching search criteria at: {options.path} branch: {options.branch}")

        return None

    print_summary(options.path, options.branch, len(commits), options.days)

    (last_message, last_date, last_files) = commits[-1]
    current_dt = datetime.datetime.now()

    output_report(f"\nFixes\n{('-' * 80)}")

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
            except ArithmeticError:
                pass

            hotspots[filename] += hotspot_factor

        output_report(f"      -{message}")

    sorted_hotspots = sorted(hotspots, key=hotspots.get, reverse=True)

    output_report(f"\nHotspots\n{('-' * 80)}")
    for k in sorted_hotspots[:options.limit]:
        yield (hotspots[k], k)


def print_code_hotspots(options):
    code_hotspots = get_code_hotspots(options)
    if code_hotspots is not None:
        for factor, filename in code_hotspots:
            output_report(f"      {factor:.2f} = {filename}")
        output_report("\n")


def write_to_markdown_file(markdown_filepath):
    output_filepath = f'{markdown_filepath}_{datetime.datetime.now()}.md'
    global markdown_output
    markdown_output += "```"
    with open(output_filepath, 'w') as file_writer:
        file_writer.writelines(markdown_output)


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
                        metavar="bugsFilePath")

    parser.add_argument("--paths",
                        help='Provide repository paths to look into',
                        type=str,
                        nargs="*",
                        metavar="paths")

    parser.add_argument("--markdown",
                        help='Provide a filename for output in markdown',
                        type=str,
                        metavar='markdownOutputFilePath'
                        )

    return parser.parse_args()


def main():
    options = parse_options()
    if options.bugsFile is not None:
        bugs_list = read_from_file(options.bugsFile)
        global description_regex
        description_regex = re.compile(f'^.*({bugs_list}).*$')
    if options.markdown is None:
        global markdown_output
        markdown_output = None
    for path in options.paths:
        option = options
        option.path = path
        print_code_hotspots(option)
    if options.markdown is not None:
        write_to_markdown_file(options.markdown)


if __name__ == '__main__':
    main()
