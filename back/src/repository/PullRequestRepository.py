import os
import json
import pg8000

class PullRequestRepository:
    def _get_db_connection(self, kind):
        if not kind:
            raise ValueError("kind is mandatory for DB connection - 'write' or 'read'")
        if kind == "write":
            db_host = os.environ['AURORA_POSTGRES__WRITER_ENDPOINT']
        else:
            db_host = os.environ['AURORA_POSTGRES__READER_ENDPOINT']

        db_user = os.environ['AURORA_POSTGRES__USERNAME']
        db_password = os.environ['AURORA_POSTGRES__PASSWORD']
        db_name = os.environ['AURORA_POSTGRES__DATABASE']
        db_port = int(os.environ['AURORA_POSTGRES__PORT'])

        connection = pg8000.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return connection

    def _perform_query(self, kind, query, args=None):
        connection = self._get_db_connection(kind)
        try:
            cursor = connection.cursor()
            cursor.execute(query, args)
            if query.strip().lower().startswith('select'):
                rows = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]
                result = [dict(zip(colnames, row)) for row in rows]
                return result
            else:
                connection.commit()
                return None
        except Exception as e:
            print(f"Database query failed: {e}")
            raise e
        finally:
            cursor.close()
            connection.close()

    def store_pr_event(self, pr_event):
        print("entered store function")
        pr_number = pr_event.get('number', 12345)
        pr_title = pr_event['head_commit']['message']
        author = pr_event['pusher']['name']
        state = pr_event.get('state', "open") 
        source_branch = pr_event['ref'].split('/')[-1]
        target_branch = pr_event.get('base', {}).get('ref', "master")
        pr_url = pr_event['repository']['html_url']
        created_at = pr_event['head_commit']['timestamp']
        raw_event = json.dumps(pr_event)
        print("finished collecting data")

        args = (
            pr_number, pr_title, author, state,
            source_branch, target_branch, pr_url,
            created_at, raw_event
        )

        query = """
            INSERT INTO pull_requests 
            (pr_number, pr_title, author, state, source_branch, target_branch, pr_url, created_at, raw_event)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        self._perform_query("write", query, args)

    def list_pr_events(self, limit, offset):
        try:
            query = """
                SELECT
                    id,
                    pr_number,
                    pr_title,
                    author,
                    state,
                    source_branch,
                    target_branch,
                    pr_url,
                    created_at,
                    COUNT(*) OVER() AS total_count
                FROM pull_requests
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;
            """
            args = (limit, offset)
            rows = self._perform_query("read", query, args)

            if not rows:
                return {"items": [], "total": 0}

            total = rows[0].get('total_count', 0) # extracts the total of all entries from the first row.
            items = [{k: v for k, v in row.items() if k != 'total_count'} for row in rows] # removes total from items

            return {"items": items, "total": total}

        except Exception as e:
            print(f"Error in list_pr_events: {e}")
            raise e

    
    
# {
#   "ref": "refs/heads/test-branch",
#   "before": "0000000000000000000000000000000000000000",
#   "after": "53466e6163eaeb84e288cd05238359de25669584",
#   "repository": {
#     "id": 123456789,
#     "name": "sample_repo",
#     "full_name": "user/sample_repo",
#     "private": false,
#     "owner": {
#       "login": "user",
#       "id": 1001
#     },
#     "html_url": "https://github.com/user/sample_repo"
#   },
#   "pusher": {
#     "name": "user",
#     "email": "user@example.com"
#   },
#   "sender": {
#     "login": "user",
#     "id": 1001
#   },
#   "created": true,
#   "deleted": false,
#   "forced": false,
#   "compare": "https://github.com/user/sample_repo/compare/commit1...commit2",
#   "commits": [
#     {
#       "id": "8eb19ef1075d84829f2c8220a77b7f9e7f5e10ee",
#       "message": "Initial commit",
#       "timestamp": "2024-10-10T21:43:45+03:00",
#       "author": {
#         "name": "user",
#         "email": "user@example.com"
#       }
#     },
#     {
#       "id": "53466e6163eaeb84e288cd05238359de25669584",
#       "message": "Second commit",
#       "timestamp": "2024-10-10T21:44:20+03:00",
#       "author": {
#         "name": "user",
#         "email": "user@example.com"
#       }
#     }
#   ],
#   "head_commit": {
#     "id": "53466e6163eaeb84e288cd05238359de25669584",
#     "message": "Second commit",
#     "timestamp": "2024-10-10T21:44:20+03:00",
#     "author": {
#       "name": "user",
#       "email": "user@example.com"
#     }
#   }
# }
