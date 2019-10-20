from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

app = Flask(__name__)
# os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


# Model

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(80), unique=False)
    uri = db.Column(db.String(255), unique=True)
    tasks = db.relationship('Task', backref='task', lazy=True)
    results = db.relationship('Result', backref='result', lazy=True)

    def __init__(self, hostname, uri):
        self.hostname = hostname
        self.uri = uri

    def __repr__(self):
        return '<Host %r %r>' % (self.hostname, self.uri)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'uri': self.uri,
            'tasks': [i.serialize for i in self.tasks],
            'results': [j.serialize for j in self.results],
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    method = db.Column(db.String(255))
    value = db.Column(db.String(255))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))

    def __init__(self, order, method, value, host_id):
        self.order = order
        self.method = method
        self.value = value
        self.host_id = host_id

    def __repr__(self):
        return '<Task %d %r %r %d>' % (self.order, self.method, self.value, self.host_id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'order': self.order,
            'method': self.method,
            'value': self.value,
            'host_id': self.host_id,
        }


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_datetime = db.Column(db.DateTime, default=datetime.now())
    status_code = db.Column(db.Integer)
    image_filepath = db.Column(db.String(255))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))

    # def __init__(self, check_datetime, status_code, image_filepath, host_id):
    def __init__(self, status_code, image_filepath, host_id):
        # self.check_datetime = check_datetime
        self.status_code = status_code
        self.image_filepath = image_filepath
        self.host_id = host_id

    def __repr__(self):
        return '<Result %r %d %r %d>' % (self.check_datetime.isoformat(), self.status_code, self.image_filepath, self.host_id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'check_datetime': self.check_datetime.isoformat(),
            'status_code': self.status_code,
            'image_filepath': self.image_filepath,
            'host_id': self.host_id,
        }

@app.route('/')
def read():
    # return "Hello World!"
    if request.method == 'GET':
        hosts = Host.query.all()
        # return jsonify([i.serialize for i in hosts])
        return render_template('readall.html', hosts=hosts)


@app.route("/", methods=['POST'])
def create():
    if request.method == 'POST':
        try:
            hostname = request.form['hostname']
            uri = request.form['uri']
            if url_validator(uri):
                if not db.session.query(Host).filter(Host.uri == uri).count():
                    db.session.add(Host(hostname, uri))
                    db.session.commit()

                try:
                    order = request.form['order']
                    method = request.form['method']
                    value = request.form['value']
                    host_id = Host.query.filter_by(uri=uri).first().id
                    db.session.add(Task(order, method, value, host_id))
                    db.session.commit()

                    return jsonify({'message': 'Added'})
                except:
                    pass
        except:
            pass

    return jsonify({'message': 'Not added'})


if __name__ == '__main__':
    app.run(debug=True)
