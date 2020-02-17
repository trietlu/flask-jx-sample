#!/usr/local/bin/python3


from flask import Flask, send_file, request, make_response


app = Flask(__name__)


@app.route('/')
def hello():
    return send_file("butler.png", mimetype='image/png')


@app.route('/xss', methods =['GET'])
def XSS1():
    param = request.args.get('param', 'not set')

    html = open('xss.html').read()
    # check param
    # param = 'hello'
    resp = make_response(html.replace('{{ param }}', param))
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

