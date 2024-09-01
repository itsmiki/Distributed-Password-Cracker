
import uuid
from utils import HashType, AttackType
from server import db



class Tasks(db.Model):
    task_id = db.Column(db.String(150), primary_key = True)
    attack_type = db.Column(db.Integer)
    hash_type = db.Column(db.Integer)
    hash = db.Column(db.String(1000))
    number_of_subtasks = db.Column(db.Integer)
    subtasks_done = db.Column(db.Integer)
    config = db.Column(db.String(10000))
    time_started = db.Column(db.String(150))
    time_finished = db.Column(db.String(150))
    hash_found = db.Column(db.Boolean)
    is_deleted = db.Column(db.Boolean)


class SubTasks(db.Model):
    subtask_id = db.Column(db.String(150), primary_key = True)
    parent_id= db.Column(db.String(150), db.ForeignKey('tasks.task_id'))
    config = db.Column(db.String(10000))
    client_id = db.Column(db.String(150), db.ForeignKey('clients.client_id'))


class Hashes(db.Model):
    hash_id = db.Column(db.String(150), primary_key = True)
    task_id = db.Column(db.String(150), db.ForeignKey('tasks.task_id'))
    hash = db.Column(db.String(1000))
    plaintext = db.Column(db.String(1000))


class Clients(db.Model):
    client_id = db.Column(db.String(150), primary_key = True)
    name = db.Column(db.String(1000))
    client_ip = db.Column(db.String(150))