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
