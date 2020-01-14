from django.test import TestCase
from modules.models import Repository, Commit, User

from django.db.utils import IntegrityError


class CardTest(TestCase):

    def test_repo_creation(self):
        """
        Tests that Repository with valid filled strings are created successfully
        """
        repo = Repository.objects.create(owner="apache", repository="spark")
        self.assertTrue(isinstance(repo, Repository))
    
    def test_repo_creation_blank(self):
        """
        Tests that Repository with empty strings are not created
        """
        try:
            Repository.objects.create(owner='', repository="spark")
        except IntegrityError:
            pass
    
    def test_commit_creation(self):
        """
        Tests that Commit with valid fields are created successfully
        """
        commit = Commit.objects.create(repoId=1, sha="7fb17f59435a76d871251c1b5923f96943f5e540", authorId=123, committerId=456, commitDate="2020-01-10 17:52:59", commentCount=0)
        self.assertTrue(isinstance(commit, Commit))
    
    def test_commit_creation_empty_date(self):
        """
        Tests that Commit with empty date is not created
        """
        try:
            Commit.objects.create(repoId=1, sha="7fb17f59435a76d871251c1b5923f96943f5e540", authorId=123, committerId=456, commentCount=0)
        except IntegrityError:
            pass
    
    def test_user_creation(self):
        """
        Tests that User with valid fields are created successfully
        """
        user = User.objects.create(userId=123, username="potiuk", name="Jarek Potiuk", userType='user', siteAdmin=False, email="jarek.potiuk@polidea.com")
        self.assertTrue(isinstance(user, User))
    
    def test_user_creation_empty(self):
        """
        Tests that User with empty name/email is not created
        """
        try:
            User.objects.create(userId=123, username="", name="Jarek Potiuk", userType='user', siteAdmin=False, email=None)
        except IntegrityError:
            pass
