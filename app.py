from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy()

POSTGRES = {
    'user': 'postgres',
    'password': '11881199',
    'db': 'postgres',
    'host': 'database-2.c9puqxutsvit.us-east-1.rds.amazonaws.com',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String(255), nullable=False)
    choices = db.Column(JSON, nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    def __init__(self, description, choices, answer):
        # self.id = id
        self.description = description
        self.choices = choices
        self.answer = answer
        # self.insert_time = insert_time
        # self.update_time = update_time
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/')
def index():
    # Create data
    db.create_all()
    return "Hello My demo!"

@app.route("/questions", methods=['post'])
def create_question():
    contentType = request.headers.get('Content-Type')

    if (contentType == 'application/json'):
        try: 
            myBody = request.json
            questionList = []
            
            for question in myBody["data"]:
                choicesLength = len(question["choices"].keys())
                if (choicesLength<1  or choicesLength>4): 
                    return {
                        "statusCode": 400,
                        "result": "some error happen"
                    }
                questionList.append(Questions(question['description'], question['choices'], question['answer']))
            db.session.add_all(questionList)
            db.session.commit()
            return {
                "statusCode": 200,
                "result": "ok"
            }
        except:
            return {
                "statusCode": 400,
                "result": "some error happen"
            }
    else:
        return 'Content-Type not supported!'

@app.route("/questions", methods=['PUT'])
def update_question():
    contentType = request.headers.get('Content-Type')
    listUpdated = []
    if (contentType == 'application/json'):
        try: 
            myBody = request.json
            for question in myBody["data"]:
                myId = question["id"]
                query = Questions.query.filter_by(id=myId).first()
                for col in question:
                    if (col == "id"):
                        continue
                    setattr(query, col, question[col])
                    db.session.commit()
                listUpdated.append(myId)
            return {
                "statusCode": 200,
                "result": "ok",
                "listUpdated": listUpdated
            }
        except:
            return {
                "statusCode": 400,
                "result": "some error happen",
                "listUpdated": listUpdated
            }
    else:
        return 'Content-Type not supported!'

@app.route("/questions", methods=['GET'])
def get_question():
    contentType = request.headers.get('Content-Type')

    if (contentType == 'application/json'):
        try: 
            myBody = request.json
            currentPage = myBody["page"]
            perPage = myBody["perPageLength"]
            handledResult = []
            if (perPage>20):
                perPage = 20
            elif(currentPage<0):
                return {
                    "statusCode": 400,
                    "result": "some error happen",
                }
            elif(perPage<0):
                return {
                    "statusCode": 400,
                    "result": "some error happen",
                }
            queryResults = Questions.query.paginate(page=currentPage, per_page=perPage)
            for question in queryResults:
                handledResult.append({
                    "id": question.__dict__["id"],
                    "description": question.__dict__["description"],
                    "choices": question.__dict__["choices"],
                    "answer": question.__dict__["answer"]
                })

            return {
                "statusCode": 200,
                "result": handledResult
            }
        except:
            return {
                "statusCode": 400,
                "result": "some error happen"
            }
    else:
        return 'Content-Type not supported!'

@app.route("/questions", methods=['DELETE'])
def delete_question():
    contentType = request.headers.get('Content-Type')

    if (contentType == 'application/json'):
        listDeleted = []
        try: 
            myBody = request.json
            
            for id in myBody["deleteId"]:
                queryResult = Questions.query.filter_by(id=id).first()
                db.session.delete(queryResult)
                db.session.commit()
                listDeleted.append(id)
            return {
                "statusCode": 200,
                "result": "ok",
                "listDeleted": listDeleted
            }
        except:
            return {
                "statusCode": 400,
                "result": "some error happen",
                "listDeleted": listDeleted
            }
    else:
        return 'Content-Type not supported!'
if __name__ == "__main__":
    app.run(debug=True)