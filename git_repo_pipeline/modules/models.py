from django.db import models
from jsonfield import JSONField


class Repository(models.Model):
    """
    Defines the repository model. It is assumed that all cards must have owner
    and repository. The primary key should be automatically generated.
    """
    owner = models.CharField(max_length=200, blank=False)
    repository = models.CharField(max_length=200, blank=False)


class User(models.Model):
    """
    Defines the user model. It is assumed that all users must have an id, 
    username and email. As the user id is unique, it is used as the primary key.
    """
    userId = models.CharField(max_length=200, primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, blank=False)
    userType = models.CharField(max_length=200)
    siteAdmin = models.BooleanField(default=False)
    email = models.CharField(max_length=200, blank=False)


class Commit(models.Model):
    """
    Defines the commit model. It is assumed that all commits belong to a 
    repository, and so have a repo_id. As the sha key is unique, it is used 
    as the primary key. 
    """
    repoId = models.CharField(max_length=200)
    sha = models.CharField(max_length=200, primary_key=True)
    authorId = models.CharField(max_length=200)
    committerId = models.CharField(max_length=200)
    commitDate = models.DateTimeField()
    commentCount = models.IntegerField(null=True)
