from flask import Flask
from flask import request
from flask import session
#from os import environ

from flask import Flask, abort, redirect, url_for, json, jsonify, request
app = Flask(__name__)
app.secret_key = b'99999xxxxx'


import requests
import os
import xmltodict
 
@app.route('/')
def healthcheck():
    return "Serviço Online"

@app.route('/calc',methods = ['POST', 'GET'])
def calc():
   if request.method == 'POST':
       #abort(400)
       reqCorpo = request.get_json()
       reqCorpo = json.dumps(reqCorpo)
       reqCorpo = json.loads(reqCorpo)
       print(reqCorpo)
       a = reqCorpo["a"]
       b = reqCorpo["b"]
       op = reqCorpo["op"]

   else:
       a = request.args.get('operand1')
       b = request.args.get('operand2')
       op = request.args.get('operator')

   if op == '+':
    c = int(a) + int(b)
   elif op == '-':
    c = int(a) - int(b)
   elif op == '*':
    c = int(a) * int(b)
   elif op == '/':
    c = int(a) / int(b)

   msg = {
            "a": int(a),
            "b": int(b),
            "op": op,
            "Resultado": c
        }
   mensagem = json.dumps(msg)
   print(mensagem)
   return json.loads(mensagem)

#teste2 de branch novo



if __name__ == '__main__':
   #app.run(debug = True)
   app.run(host='0.0.0.0',debug=True)

    #, ssl_context=('caminho do .cer')

    
