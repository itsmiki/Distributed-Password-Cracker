from flask import (
    Blueprint, 
    request,
    render_template,
    redirect,
    flash
    )
import requests
from config import GeneralConfig
from utils import parse_charset, parse_dictionaries



dashboard = Blueprint('client', __name__)
api_prefix = "/api/v1/webadmin"


@dashboard.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@dashboard.route('/bruteforce-attack', methods=['GET', 'POST'])
def create_bruteforce_attack():
    if request.method == 'POST':
        _config = GeneralConfig("config.ini")
        try:
            res = requests.post(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/create-task', json={
            "attack_type": request.form['attack_type'],
            "hash": request.form['hash'],
            "hash_type": request.form['hash_type'],
            "length": request.form['password_length'],
            "charset": parse_charset(request.form.keys())
            })
            if res.status_code == 201:
                flash('Attack created successfully!', category='alert')
            elif res.status_code == 500:
                flash('Internal server error - task not created!', category='error')
            elif res.status_code == 422:
                flash('Wrong hash format - task not created!', category='error')
        except:
            return render_template("bruteforce_attack.html")
    return render_template("bruteforce_attack.html")


@dashboard.route('/dictionary-attack', methods=['GET', 'POST'])
def create_dictionary_attack():
    _config = GeneralConfig("config.ini")
    if request.method == 'POST':
        try:
            res = requests.post(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/create-task', json={
            "attack_type": request.form['attack_type'],
            "hash": request.form['hash'],
            "hash_type": request.form['hash_type'],
            "dictionaries": parse_dictionaries(request.form.keys())
            })
            if res.status_code == 201:
                flash('Attack created successfully!', category='alert')
            elif res.status_code == 500:
                flash('Internal server error - task not created!', category='error')
            elif res.status_code == 422:
                flash('Wrong hash format - task not created!', category='error')
        except:
            return render_template("bruteforce_attack.html")
        
    dictionaries = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/dictionaries')
    return render_template("dictionary_attack.html", dictionaries_list = dictionaries.json())

@dashboard.route('/mask-attack', methods=['GET', 'POST'])
def create_mask_attack():
    _config = GeneralConfig("config.ini")
    if request.method == 'POST':
        try:
            res = requests.post(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/create-task', json={
            "attack_type": request.form['attack_type'],
            "hash": request.form['hash'],
            "hash_type": request.form['hash_type'],
            "dictionaries": [request.form['dictionary']],
            "masks": [request.form['mask']]
            })
            if res.status_code == 201:
                flash('Attack created successfully!', category='alert')
            elif res.status_code == 500:
                flash('Internal server error - task not created!', category='error')
            elif res.status_code == 422:
                flash('Wrong hash format - task not created!', category='error')
        except:
            return render_template("bruteforce_attack.html")
        
    masks = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/masks')
    dictionaries = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/dictionaries')
    return render_template("mask_attack.html", mask_list = masks.json(), dictionaries_list = dictionaries.json())

@dashboard.route('/identify-hash', methods=['GET', 'POST'])
def identify_hash():
    if request.method == 'POST':
        _config = GeneralConfig("config.ini")
        try:
            res = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/identify-hash/{request.form['hash']}')
            if res.status_code == 404:
                flash('Wrong hash format or hash is not supported.', category='error')
            return render_template("identify_hash.html", hash_list = res.json())
        except:
            return render_template("identify_hash.html", visibility = "hidden")
    return render_template("identify_hash.html", visibility = "hidden")


@dashboard.route('/attacks', methods=['GET', 'POST'])
def get_attacks():
    _config = GeneralConfig("config.ini")
    if request.method == 'POST':
        requests.delete(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/remove-task/{request.form['task_id']}')
        
    res_attacks = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/tasks')
    res_hashes = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/hashes')
    print(res_attacks.json())
    return render_template("attacks_hashes.html", attacks_list = res_attacks.json(), hashes_list = res_hashes.json())





@dashboard.route('/connected-clients', methods=['GET'])
def get_workers():
    _config = GeneralConfig("config.ini")
    res = requests.get(f'http://{_config.get_config()['taskServerIp']}:{_config.get_config()['taskServerPort']}{api_prefix}/workers')
    return render_template("clients.html", clients_list = res.json())

