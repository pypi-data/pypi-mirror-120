
# Gitlab Client

## Install
To install latest version:

    pip install gitlab-v4

To install a specific version, for example: 0.0.1

    pip install gitlab-v4==0.0.1

## Usage

    from gitlab_client.gitlab_client import Gitlab
    
    client = Gitlab(
    	project_id="1234",
    	access_token="abcd1234-efgh5678",
    	gitlab_base_url="https://gitlab.com/api/v4"
    )
Once you instantiated a client instance as shown above, you can call different api methods available. 
To list all branches in project:

    client.list_branches()
Sample response:

    [
      {
    	'name': 'main',
    	'commit': {
    		'id': 'abc123d357ae0ecc2d071eg3b64l4367861840fb',
    		'short_id': 'abc123d3',
    		'created_at': '2021-08-10T06:08:11.000+00:00',
    		'parent_ids': None,
    		'title': 'Update readme file',
    		'message': 'Update readme file',
    		'author_name': 'John Doe',
    		'author_email': 'johndoe@users.noreply.gitlab.com',
    		'authored_date': '2021-08-10T06:08:11.000+00:00',
    		'committer_name': 'John Doe',
    		'committer_email': 'johndoe@users.noreply.gitlab.com',
    		'committed_date': '2021-08-10T06:08:11.000+00:00',
    		'trailers': None,
    		'web_url': 'https://gitlab.com/group_name/repo_name/-/commit/abc123d357ae0ecc2d071eg3b64l4367861840fb'
    	},
    	'merged': False,
    	'protected': True,
    	'developers_can_push': False,
    	'developers_can_merge': False,
    	'can_push': True,
    	'default': True,
    	'web_url': 'https://gitlab.com/group_name/repo_name/-/tree/main'
      },
      {
    	'name': 'stable',
    	'commit': {
    		'id': 'def456d357ae0ecc2d071eg3b64l4367861840fb',
    		'short_id': 'def456d3',
    		'created_at': '2021-08-10T07:14:35.000+00:00',
    		'parent_ids': None,
    		'title': "some title",
    		'message': "Merge branch 'main' into 'stable'",
    		'author_name': 'Jane Doe',
    		'author_email': 'janedoe@users.noreply.gitlab.com',
    		'authored_date': '2021-08-10T07:14:35.000+00:00',
    		'committer_name': 'Jane Doe',
    		'committer_email': 'janedoe@users.noreply.gitlab.com',
    		'committed_date': '2021-08-10T07:14:35.000+00:00',
    		'trailers': None,
    		'web_url': 'https://gitlab.com/group_name/repo_name/-/commit/def456d357ae0ecc2d071eg3b64l4367861840fb'
    	},
    	'merged': False,
    	'protected': True,
    	'developers_can_push': False,
    	'developers_can_merge': False,
    	'can_push': True,
    	'default': False,
    	'web_url': 'https://gitlab.com/group_name/repo_name/-/tree/stable'
      }
    ]
