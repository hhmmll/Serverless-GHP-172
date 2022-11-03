# Serverless-GHP-172
Provide to GHP members for Backend Task
# Functional Requirements
Using Flask create a quiz manager application. You are to create APIs that will create, retrieve, update, and delete (CRUD) quiz items. You will use [Postman](https://www.postman.com/) to do the DEMO.

* APIs should return JSON data (if there is any return data).
* Use PostgreSQL Database.
* A quiz item should have:
 * Question or description
 * Multiple choices (Maximum 4 and minimum 2)
 * One correct answer
* Can browse through quiz items with pagination.
 * At max 20 items per page
 * API response should include:
     *  Quiz questions
     *  Quiz answer choices
     *  Quiz correct answers
* Can create, update, delete quiz items 1 at a time


# Tooltiips
* Candidate need to fork a repo to keep the changes
* Use Flask-RESTX to create views
* Use Flask Accepts and Flask Marshmallow for request validation and response marshalling
* Use Flask-SQLAlchemy to make DB queries with ORM and form DB Schema
* Showcase DB schema and data migration with Flask-Migrate
* Use Dev Container to host flask application locally
* PostgreSQL database is hosted using docker
* Showcase Swagger API documentation using Flask-RESTX
* Prepopulate database with at least 5 quiz items using Flask-Migrate

# Grading Criteria
* Completion rate of functional and non-functional requirements
* API design
 * Resource naming
 * Use of HTTP verbs
 * Propriety of API request and response (e.g. response code and response body)
* Database design
 * Normalization of tables
 * DB unit (e.g. tables, fields) naming
 * Table relationships
