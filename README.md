# Git Repository Pipeline

This pipeline extracts information from the git API commits endpoint. It has 4 basic functions - store the data if it doesn't exist, generate the top 3 authors in a given time period, generate the author with the longest contribution period within a given time period and generates a heatmap of commits.

The 4 endpoints are as follows:
- /store/
- /authors/top/
- /authors/contribution/
- /heatmap/

For the purpose of this assignment, the database schema is designed to best answer the 3 questions, so data that is not necessary for the 3 questions was not stored. In addition, since the git API used does not require any token, no authentication is set up. 


Steps:

First, create a virtual environment and install the requirements for the code.
```
$ pipenv shell
$ pip install -r requirements.txt
```

## 1. Storing the data
For the store endpoint, as it is storing raw data from the git API, it doesn't require dates as an input. To create the database, run the following on the command line: 

```
$ python manage.py makemigrations modules
$ python manage.py migrate
```

Then, start the server:
```
$ cd git_repo_pipeline
$ python manage.py runserver
```

To store the data, send a POST request to the /store/ endpoint. An example is as follows: 
```
POST http://localhost:8000/store/

Accept: application/json
Content-Type: application/json

{
	"owner": "apache",
	"repository": "spark"
}
```

For the next 3 endpoints, end_date can be specified as null, but all other fields must have a value.

## 2. List the top 3 authors in the given time period

```
POST http://localhost:8000/authors/top/

Accept: application/json
Content-Type: application/json

{
	"owner": "apache",
	"repository": "spark",
	"start_date": "2019-09-12",
	"end_date": "2020-1-20"
}
```

## 3. Find the author with the longest contribution window within the time period

```
POST http://localhost:8000/authors/contribution/

Accept: application/json
Content-Type: application/json

{
	"owner": "apache",
	"repository": "spark",
	"start_date": "2019-09-12",
	"end_date": null
}
```

## 4. Produce a heatmap of commits

```
POST http://localhost:8000/heatmap/

Accept: application/json
Content-Type: application/json

{
	"owner": "apache",
	"repository": "spark",
	"start_date": "2019-09-12",
	"end_date": null
}
```

## To run tests locally
```
$ DJANGO_SETTINGS_MODULE="modules.settings_test" python manage.py test modules -- 
```

## Improvements
For 2., the endpoint selects the top 3 authors without any randomness. As a result, if there are many authors with the same number of commits, the author returned may always be the same. Instead, the SQL query could be written doing a group by number of commits and randomly selecting the authors in the top 3 groups.

For the 3 endpoints other than 1., the data is queried directly without considering the owner/repository. Thus, for example, the top 3 authors being returned would be the top 3 authors regardless of which repository they made commits in. If this should be a consideration, a query can be made to the repository database to identify the repository id, which can be used to filter the Commit table.  