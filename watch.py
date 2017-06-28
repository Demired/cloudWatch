# # all the imports
import json
import sqlite3
import time
from flask import Flask, g, request

app = Flask(__name__)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/watch', methods={'POST'})
def add_entry():
    ip = request.remote_addr

    now_time = int(time.time())

    insert = g.db.execute("INSERT INTO agent ("
                          "'ip','cpu_idle','cpu_count','cpu_user','cpu_nice','cpu_logical_count','cpu_system'"
                          ",'nginx_ok','fpm_ok','boot_time','php_version','nginx_version','memory_total',"
                          "'memory_used','memory_free','create_time') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                          [ip, request.form['cpu_idle'], request.form['cpu_count'], request.form['cpu_user'],
                           request.form['cpu_nice'], request.form['cpu_logical_count'], request.form['cpu_system'],
                           0 if 'nginx_ok' in request.form.keys() else 1, 0 if 'fpm_ok' in request.form.keys() else 1,
                           request.form['boot_time'], 0, 0,
                           request.form['memory_total'], request.form['memory_used'], request.form['memory_free'],
                           now_time])

    g.db.commit()
    agent_id = insert.lastrowid
    disk = json.loads(request.form['disk'])
    for disk_name in disk:
        g.db.execute("INSERT INTO disk ('agent_id','disk_name','total','used','percent','fstype','create_time')"
                     " VALUES (?,?,?,?,?,?,?)",
                     [agent_id, disk_name, disk[disk_name]['total'], disk[disk_name]['used'],
                      disk[disk_name]['percent'],
                      disk[disk_name]['fstype'], now_time]
                     )
        g.db.commit()

    return 'ok'


if __name__ == '__main__':
    app.config['DATABASE'] = './watch.db'
    # app.debug = True
    app.run(host='0.0.0.0')
