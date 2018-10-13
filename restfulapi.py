# -*- coding: utf-8 -*-
# @Time    : 18-10-12 下午5:45
# @Author  : allen.you

from flask import Flask, url_for, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal

app = Flask(__name__)
api = Api(app)


tasks = [
    {
        'task_id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'task_id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}


class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        # return jsonify({'tasks': map(make_public_task, tasks)})
        # return jsonify({'tasks': tasks})
        return jsonify({'tasks': marshal(tasks, task_fields)})


class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, task_id):
        task = list(filter(lambda t: t['task_id'] == task_id, tasks))
        if len(task) == 0:
            abort(404)
        # return jsonify({'task': task[0]})
        return jsonify({'task': marshal(task[0], task_fields)})

    def put(self, task_id):
        task = filter(lambda t: t['task_id'] == task_id, tasks)
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v is not None:
                task[k] = v
        # return jsonify({'task': make_public_task(task)})
        return jsonify({'task': marshal(task, task_fields)})


api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:task_id>', endpoint='task')


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run()
