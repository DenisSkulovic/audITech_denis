import os
import json
import psycopg2

class PullRequestRepository():
        
    def _get_db_connection():
        DB_HOST = os.environ['DB_HOST']
        DB_USER = os.environ['DB_USER']
        DB_PASSWORD = os.environ['DB_PASSWORD']
        DB_NAME = os.environ['DB_NAME']
        return psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
    def _perform_query(self, query, args=None):
        connection = self._get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, args)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    
    def store_pr_event(self, pr_event):
        pr_title = pr_event['pull_request']['title']
        author = pr_event['pull_request']['user']['login']
        state = pr_event['pull_request']['state']
        source_branch = pr_event['pull_request']['head']['ref']
        target_branch = pr_event['pull_request']['base']['ref']
        pr_url = pr_event['pull_request']['html_url']
        created_at = pr_event['pull_request']['created_at']
        raw_event = json.dumps(pr_event)
        
        args = (pr_title, author, state, source_branch, target_branch, pr_url, created_at, raw_event)
        query = """
                    INSERT INTO pull_requests 
                    (pr_number, pr_title, author, state, source_branch, target_branch, pr_url, created_at, raw_event)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        query_result = self._perform_query(query, args)
        return query_result
    
    def list_pr_events(self, limit, offset):
        args = (limit, offset)
        query = """
                    SELECT id, pr_title, author, state, source_branch, target_branch, pr_url, created_at
                    FROM pull-request-details
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s;
                """
        query_result = self._perform_query(query, args)
        return query_result
    
        
# {
#   "action": "opened",  // The action performed (e.g., opened, closed, reopened)
#   "number": 42,        // The pull request number
#   "pull_request": {
#     "id": 12345678,            // The pull request ID
#     "url": "https://api.github.com/repos/username/repo/pulls/42",
#     "html_url": "https://github.com/username/repo/pull/42",
#     "diff_url": "https://github.com/username/repo/pull/42.diff",
#     "patch_url": "https://github.com/username/repo/pull/42.patch",
#     "issue_url": "https://api.github.com/repos/username/repo/issues/42",
#     "commits_url": "https://api.github.com/repos/username/repo/pulls/42/commits",
#     "review_comments_url": "https://api.github.com/repos/username/repo/pulls/42/comments",
#     "review_comment_url": "https://api.github.com/repos/username/repo/pulls/comments{/number}",
#     "statuses_url": "https://api.github.com/repos/username/repo/statuses/abcdefg",
#     "number": 42,              // Pull request number
#     "state": "open",           // The current state of the pull request (e.g., open, closed)
#     "locked": false,           // Whether the pull request is locked
#     "title": "Update README",  // The pull request title
#     "user": {                  // The user who created the pull request
#       "login": "octocat",
#       "id": 1,
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "type": "User"
#     },
#     "body": "Please pull these awesome changes",  // The pull request description
#     "created_at": "2021-01-01T12:34:56Z",
#     "updated_at": "2021-01-01T12:45:56Z",
#     "closed_at": null,
#     "merged_at": null,
#     "merge_commit_sha": "abcdefg",     // SHA of the merge commit (if merged)
#     "assignees": [],                   // Users assigned to the PR
#     "requested_reviewers": [],         // Reviewers requested
#     "head": {                          // The source branch information (where changes are coming from)
#       "label": "username:feature-branch",
#       "ref": "feature-branch",         // The branch name
#       "sha": "abcdefg",                // Latest commit SHA in the source branch
#       "user": {
#         "login": "octocat",
#         "id": 1,
#         "avatar_url": "https://github.com/images/error/octocat_happy.gif"
#       },
#       "repo": {                        // The repository of the source branch
#         "id": 123456,
#         "name": "repo",
#         "full_name": "username/repo",
#         "private": false,
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif"
#         }
#       }
#     },
#     "base": {                          // The target branch information (where changes will be merged into)
#       "label": "username:main",
#       "ref": "main",                   // The target branch name
#       "sha": "xyz123",                 // Latest commit SHA in the target branch
#       "user": {
#         "login": "octocat",
#         "id": 1,
#         "avatar_url": "https://github.com/images/error/octocat_happy.gif"
#       },
#       "repo": {                        // The repository of the target branch
#         "id": 123456,
#         "name": "repo",
#         "full_name": "username/repo",
#         "private": false,
#         "owner": {
#           "login": "octocat",
#           "id": 1,
#           "avatar_url": "https://github.com/images/error/octocat_happy.gif"
#         }
#       }
#     },
#     "mergeable": true,          // Whether the pull request is mergeable
#     "rebaseable": true,         // Whether the pull request can be rebased
#     "merged": false,            // Whether the pull request has been merged
#     "comments": 10,             // Number of comments on the pull request
#     "review_comments": 2,       // Number of review comments
#     "commits": 5,               // Number of commits in the pull request
#     "additions": 100,           // Number of additions made in the pull request
#     "deletions": 50,            // Number of deletions made in the pull request
#     "changed_files": 3          // Number of changed files
#   },
#   "repository": {
#     "id": 123456,
#     "name": "repo",
#     "full_name": "username/repo",
#     "owner": {
#       "login": "octocat",
#       "id": 1,
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif"
#     },
#     "private": false,
#     "html_url": "https://github.com/username/repo",
#     "description": "This is a repository",
#     "fork": false,
#     "created_at": "2020-12-25T12:34:56Z",
#     "updated_at": "2021-01-01T12:34:56Z",
#     "pushed_at": "2021-01-01T12:45:56Z",
#     "default_branch": "main",
#     "stargazers_count": 42,
#     "forks_count": 10,
#     "open_issues_count": 5
#   },
#   "sender": {
#     "login": "octocat",
#     "id": 1,
#     "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#     "url": "https://api.github.com/users/octocat",
#     "html_url": "https://github.com/octocat",
#     "type": "User"
#   }
# }