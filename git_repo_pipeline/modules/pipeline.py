import requests

from .models import Commit, Repository, User


class DataPipeline():
    """
    Pipeline for processing data from the git api. 
    """
    def __init__(self):
        self.users = set()
        self.repo_id = None            
            
    def extract(self, owner, repository):
        self.process_repository(owner, repository)

        url = "https://api.github.com/repos/{}/{}/commits".format(owner, repository)
        response = requests.get(url)
        response_body = response.json()

        if response.status_code != 200:
            # return error message if response status code is not 200
            raise Exception(response_body)

        for commit in response_body:
            self.process_user(commit, 'author')
            self.process_user(commit, 'committer')
            self.process_commit(commit, self.repo_id)

    def process_repository(self, owner, repository):
        """
        Processes and stores repository details in the Repository
        table if it is not present
        """
        repo = Repository.objects.filter(owner=owner, repository=repository)
        if not repo:
            r = Repository(owner=owner, repository=repository)
            r.save()
            new_repo = Repository.objects.filter(owner=owner, repository=repository)
            self.repo_id = new_repo[0].id
        else:
            self.repo_id = repo[0].id

    
    def process_user(self, data, user):
        """
        Processes and stores all user details in the User table
        if it is not present
        """
        details = data.get(user)
        if not details:
            # ignore row if it doesn't have the required values
            return

        username = details.get('login')
        user_id = details.get('id')

        if user_id in self.users:
            # ignore row if it has already been stored
            return
        
        user_type = details.get('type')
        site_admin = details.get('site_admin')

        commit = data.get('commit')
        basic = commit.get(user)
        if not basic:
            # ignore row if it doesn't have the required values
            return
        
        name = basic.get('name')
        email = basic.get('email')

        u = User(userId=user_id, username=username, name=name, userType=user_type, siteAdmin=site_admin, email=email)
        u.save()

        self.users.add(user_id)

    def process_commit(self, data, repo_id):
        """
        Processes and stores all commit details in the Commit table
        if it is not present
        """
        sha = data.get('sha')
        commit = data.get('commit')
        if not commit:
            # ignore row if it doesn't have the required values
            return

        author = data.get('author')
        if not author:
            # ignore row if it doesn't have the required values
            return

        author_id = author.get('id')
        committer = data.get('committer')
        if not committer:
            # ignore row if it doesn't have the required values
            return
        committer_id = committer.get('id')
        author_details = commit.get('author')
        if not author_details:
            # ignore row if it doesn't have the required values
            return
        date = author_details.get('date')
        comment_count = commit.get('comment_count')

        c = Commit(repoId=repo_id, sha=sha, authorId=author_id, committerId=committer_id, commitDate=date, commentCount=comment_count)
        c.save()
