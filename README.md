# Plagiarism Detection

1. Plagiarism detection using TF-IDF and cosine similarity.
2. Input text will be matched against all the documents present in the DB(`document` table) to get the maximum similarity score.

### Requirements
Python 3.x, pip3, MySQL

### How to run?

1. Move to ```<project-dir>```, create virual environment and then activate it as

```sh
$ cd <project-dir>
$ virtualenv .environment
$ source .environment/bin/activate
```

2. Edit configuration under ```settings.py```. i.e. provide configuration/settings related to DB and other constants.

> If you are using PyCharm then environment variables can be specified under `run configuration`.

3. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

4. Under ```<project-dir>``` install requirements/dependencies as 

```sh 
$ pip3 install -r requirements.txt
```

5. Then run test cases as -

```sh
$ python -m unittest discover -s 'tests' -p '*.py'
```

6. Run server as - 
```sh
$ python app.py 
```
> Now you can access the application by visiting ```{protocol}://{host}:{port}```. For localhost it is ```http://localhost:5000```.


### Applications & Endpoints

There are following three APIs -

#### 1. Adding a new document - 

> POST ```{host}:{port}/api/v1/plagiarism/documents```.

*Request body*

```javascript
{
      "content": "Sachin Ramesh Tendulkar is a former Indian international cricketer and a former captain of the Indian national team, regarded as one of the greatest batsmen of all time. He is the highest run scorer of all time in International cricket.",
      "title": "Sachin Tendulkar",
      "author": "James neshley",
      "description": "About the legacy of the great Sachin Tendulkar"
}
```

*Response*

```javascript
{
     "success": true,
     "message": "Document added successfully!",
     "data": null,
     "errors": []
}
```

#### 2. Detecting plagiarism - 

> POST ```{host}:{port}/api/v1/plagiarism/detect```.

*Request body*

```javascript
{
    "text": "Sachin Tendulkar is the great cricketer.",
}
```

*Response*

```javascript
{
    "success": true,
    "message": "Input text is 25.5% similar to the doc `Sachin Tendulkar` with similarity score of 0.25499620385104793",
    "data": {
        "similarity_score": 0.25499620385104793,
        "similarity_percentage": 25.5,
        "doc": {
            "id": "4855f11b-78d2-4e08-a070-169965cb6c11",
            "author": "James neshley",
            "title": "Sachin Tendulkar",
            "description": "About the legacy of the great Sachin Tendulkar",
            "content": "Sachin Ramesh Tendulkar is a former Indian international cricketer and a former captain of the Indian national team, regarded as one of the greatest batsmen of all time. He is the highest run scorer of all time in International cricket."
        }
    },
    "errors": []
}
```

#### 3. Fetch all documents - 

> GET ```{host}:{port}/api/v1/plagiarism/documents?page=1&per_page=10```.

*Response*

```javascript
{
    "success": true,
    "message": "",
    "data": {
        "data": [
            {
                "id": "4855f11b-78d2-4e08-a070-169965cb6c11",
                "author": "James neshley",
                "title": "Sachin Tendulkar",
                "description": "About the legacy of the great Sachin Tendulkar",
                "content": "Sachin Ramesh Tendulkar is a former Indian international cricketer and a former captain of the Indian national team, regarded as one of the greatest batsmen of all time. He is the highest run scorer of all time in International cricket."
            },
            {
                "id": "e7b4e65b-1ff0-4f1c-98b5-fc6ca5f9cda3",
                "author": "test_author_aa45d441-0a57-45b7-b995-c804620ef427",
                "title": "test_title_f0eba63b-2e10-47c6-b869-fbb91cb6c385",
                "description": "test_description_2283a1a6-da0e-45e7-82a5-eb380f778739",
                "content": "test_content_de8fedf2-170d-4f91-a1b7-c7345cddac46"
            },
            {......},
            {......}
         ],
         "count": 72
      }
}
```

### Links -
 - [Postmant API dump](https://github.com/suyash248/plagiarism_detection/blob/master/output/Plag.postman_collection.json)
 - [Screenshots](https://github.com/suyash248/plagiarism_detection/blob/master/output)

### TODO - 
1. Use a wsgi server like Gunicorn.
2. Centralized logging.
