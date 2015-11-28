#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import github3 as github
import os
import argparse
from time import sleep


gh_user = os.getenv('GH_USER', None)
gh_pass = os.getenv('GH_PWD', None)
gh_token = os.getenv('GH_TOKEN', None)
gh_dorks_file = "github-dorks.txt"

gh = github.GitHub(username=gh_user, password=gh_pass, token=gh_token)


def search(repo_to_search=None, user_to_search=None):
    found = False
    with open(gh_dorks_file, 'r') as dork_file:
        for dork in dork_file:
            dork = dork.strip()
            addendum = ''
            if repo_to_search is not None:
                addendum = ' repo:' + repo_to_search
            elif user_to_search is not None:
                addendum = ' user:' + user_to_search

            dork = dork + addendum
            search_results = gh.search_code(dork)
            try:
                for search_result in search_results:
                    found = True
                    fmt_args = {
                        'dork': dork,
                        'text_matches': search_result.text_matches,
                        'path': search_result.path,
                        'score': search_result.score,
                        'url': search_result.html_url
                    }
                    print(
                        '''Found result for {dork}
Text matches: {text_matches}
File path: {path}
Score/Relevance: {score}
URL of File: {url}
                    '''.format(**fmt_args)
                    )
            except github.exceptions.ForbiddenError as e:
                print(e)
                # need to retry in case of API rate limit reached
                # note done yet
            except github.exceptions.GitHubError as e:
                print('GitHubError encountered on search of dork: ' + dork)
                print(e)
            except Exception as e:
                print('Error encountered on search of dork: ' + dork)

    if not found:
        print('No results for your dork search' + addendum + '. Hurray!')


def main():
    parser = argparse.ArgumentParser(
        description='Search github for github dorks',
        epilog='Use responsibly, Enjoy pentesting'
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-u',
        '--user',
        dest='user_to_search',
        action='store',
        help='Github user/org to search within. Eg: techgaun'
    )
    group.add_argument(
        '-r',
        '--repo',
        dest='repo_to_search',
        action='store',
        help='Github repo to search within. Eg: techgaun/github-dorks'
    )

    args = parser.parse_args()
    search(
        repo_to_search=args.repo_to_search,
        user_to_search=args.user_to_search
    )

if __name__ == '__main__':
    main()
