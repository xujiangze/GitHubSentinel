# src/github_client.py

import requests
import datetime
import json


class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}
        self.per_page = 5

    def fetch_updates(self, repo, since=None, until=None):
        # 获取特定 repo 的更新（commits, issues, pull requests）
        updates = {
            'commits': self.fetch_commits(repo, since, until),
            'issues': self.fetch_issues(repo),
            'pull_requests': self.fetch_pull_requests(repo)
        }
        return updates

    def fetch_commits(self, repo, since, until):
        commits = []
        page = 1
        until = datetime.datetime.strptime(until, '%Y-%m-%dT%H:%M:%SZ')
        while True:
            # 支持since和until
            response = self._fetch_commits(repo, since=since, until=until, page=page, per_page=self.per_page)
            for commit in response:
                commits.append(commit)
            page += 1
            if len(response) < self.per_page:
                break

        return commits

    def _fetch_commits(self, repo, since=None, until=None, page=None, per_page=None):
        # 文档: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
        # 支持until
        url = f'https://api.github.com/repos/{repo}/commits'
        params = self.get_params(since=since, page=page, per_page=per_page, until=until)
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_params(self, since=None, page=None, per_page=None, sort="", until=None):
        params = {
            "direction": "asc",
        }
        if since:
            params['since'] = since
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page
        if until:
            params['until'] = until

        if sort:
            params['sort'] = sort
        return params

    def fetch_issues(self, repo, since, until):
        # 获取特定 repo 的 issues
        issues = []
        page = 1
        until = datetime.datetime.strptime(until, '%Y-%m-%dT%H:%M:%SZ')
        while True:
            print(f"Fetching issues for page {page}")
            response = self._fetch_issues(repo, since=since, page=page, per_page=self.per_page, sort="updated")
            for issue in response:
                # 排序字段是updated_at
                date = issue['updated_at']
                date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
                if date > until:
                    # 携带排序, 可以用break
                    break
                issues.append(issue)
            page += 1
            if len(response) < self.per_page:
                break

        return issues

    def _fetch_issues(self, repo, since=None, page=None, per_page=None, sort=""):
        # 文档: https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues
        # 不支持until
        url = f'https://api.github.com/repos/{repo}/issues'
        params = self.get_params(since, page=page, per_page=per_page, sort=sort)
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_pull_requests(self, repo):
        # 文档: https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-pull-requests
        # 不支持since, until
        url = f'https://api.github.com/repos/{repo}/pulls'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def export_daily_progress(self, repo):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        since = f'{date_str}T00:00:00Z'
        until = f'{date_str}T23:59:59Z'
        issues = self.fetch_issues(repo, since, until)
        pull_requests = self.fetch_pull_requests(repo)
        filename = f'daily_progress/{repo.replace("/", "_")}_{date_str}.md'
        with open(filename, 'w') as f:
            f.write(f"# {repo} Daily Progress - {date_str}\n\n")
            f.write("## Issues\n")
            for issue in issues:
                f.write(f"- {issue['title']} #{issue['number']}\n")
            f.write("\n## Pull Requests\n")
            for pr in pull_requests:
                f.write(f"- {pr['title']} #{pr['number']}\n")

        print(f"Exported daily progress to {filename}")

        return filename


if __name__ == '__main__':
    client = GitHubClient(
        '你的token')
    since = '2024-10-18T00:06:37Z'
    until = '2024-10-19T10:45:58Z'
    commits = client.fetch_commits('langchain-ai/langchain', since, until)
    for commit in commits:
        print(commit)

    # issues = client.fetch_issues('langchain-ai/langchain', since, until)
    # for issue in issues:
    #     print(issue['updated_at'])
    #
    # pull_requests = client.fetch_pull_requests('langchain-ai/langchain', since, until)
    # for pr in pull_requests:
    #     print(pr['updated_at'])
