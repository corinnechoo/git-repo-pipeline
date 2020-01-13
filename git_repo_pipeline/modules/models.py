from django.db import models
from jsonfield import JSONField


class Repository(models.Model):
    """
    Defines the repository model. It is assumed that all cards must have organization
    and repository. The primary key should be automatically generated.
    """
    # repoId = models.CharField(max_length=200, primary_key=True)
    organization = models.CharField(max_length=200)  # TODO: cannot have null
    repository = models.CharField(
        max_length=200, db_index=True)  # TODO: cannot have null


class User(models.Model):
    """
    Defines the user model. It is assumed that all users must have an id, 
    username and email. As the user id is unique, it is used as the primary key.
    """
    userId = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)  # TODO: cannot have null
    nodeId = models.CharField(max_length=200)  # TODO: don't need to store
    userType = models.CharField(max_length=200)
    siteAdmin = models.BooleanField(default=False)
    email = models.CharField(max_length=200)  # TODO: cannot have null


class Commit(models.Model):
    """
    Defines the commit model. It is assumed that all commits belong to a 
    repository, and so have a repo_id. The sha key is unique, 
     must have an id, 

    """
    repoId = models.CharField(max_length=200)
    sha = models.CharField(max_length=200, primary_key=True)
    nodeId = models.CharField(max_length=200)  # TODO: don't need to store
    authorId = models.CharField(max_length=200)
    committerId = models.CharField(max_length=200)
    commitDate = models.DateTimeField()
    # TODO: don't need to store
    message = models.CharField(max_length=200, blank=True, null=True)
    commitCount = models.IntegerField(blank=True, null=True)
