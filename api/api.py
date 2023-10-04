import traceback
from flask import Flask,request,Response,make_response,jsonify
import os
from pexpect import pxssh

from flask_cors import CORS , cross_origin
import pathlib
from os.path import abspath
import os.path, time
import datetime

#import requests
import logging
import threading

app = Flask(__name__)
CORS(app)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return http 500 status code"""
    return make_response(jsonify({'error' : 'Internal Server Error'}),500)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return http 404 status code"""
    return make_response(jsonify({'error' : 'The requested URL was not found on the server'}),404)


def run_tests(hostname, user):
    try:
        jsondata = request.get_json()
        app.logger.info(jsondata)
        s = pxssh.pxssh(timeout=600);
        app.logger.info("trying to login..")
        s.login(hostname, user)
        app.logger.info("login successful. executing command: mkdir -p /mnt/cdp/"+jsondata["testName"])
        s.sendline("pwd")
        s.prompt()
        print(s.before)
        s.sendline("./test_runner.sh "+jsondata["testName"]+ " " +jsondata["nThreads"]+" "+jsondata["nOptions"]+ " "+jsondata["pathLength"]+" "+ jsondata["testBlockLength"])
        s.prompt()
        app.logger.info("command executed successfully.. trying to print output")
        app.logger.info(s.before.decode('utf-8', 'ignore'))
        s.logout()
        app.logger.info("logged out successully")
    except:
        traceback.print_exc()

@app.route("/testcase/start",methods=['POST'])
def run_threads():
    try:
        t1=threading.Thread(target=run_tests,args=('cdp-mc-cvm','ubuntu'))
        t2=threading.Thread(target=run_tests,args=('cdp-mc-svm','ubuntu'))
        t1.run()
        t2.run()
        return Response('Tests triggered successfully', status=200, mimetype='application/json')
    except Exception as e:
        traceback.print_exc()
        return Response("{'message':" + str(e) + "}", status=500, mimetype='application/json')


def get_result(hostname,user):
    s = pxssh.pxssh(timeout=300)
    s.login(hostname, user)
    s.sendline("pwd")
    s.prompt()
    print(s.before)
    s.sendline("python3 get_results.py")
    s.prompt()
    data = s.before
    return data


def str_to_list(data):
    string_data = data.split("python3 get_results.py")
    res = []
    for sub in string_data:
        res.append(sub.replace("\n", " "))
    var_2 = (res[1].strip())
    output_list = (eval(var_2))
    print(output_list)
    return output_list

@app.route("/testcase/list",methods=['GET'])
def get_list():
    try:
        final_list = list()
        data_svm=get_result('cdp-mc-svm','ubuntu')
        data_cvm=get_result('cdp-mc-cvm','ubuntu')
        data_cvm1 = str_to_list(data_cvm)
        data_svm1 = str_to_list(data_svm)
        for i in data_cvm1:
            for j in data_svm1:
            	if i["testname"] == j["testname"]:
                    res_dict = i.copy()
                    res_dict.update(j)
                    final_list.append(res_dict)
        return jsonify({"data":final_list})
    except Exception as e:
        return jsonify({"error":str(e)})
