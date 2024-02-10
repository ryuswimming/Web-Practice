from flask import Flask, request, redirect

app = Flask(__name__)

nextId = 4

topics = [
    {'id' : 1, 'title': 'html', 'body' : 'html is ...'},
    {'id' : 2, 'title': 'css', 'body' : 'css is ...'},
    {'id' : 3, 'title': 'javascript', 'body' : 'javascript is ...'},
]

def template(contents, content, id = None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li> <a href = "/update/{id}/"> update </a> </li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1> <a href = '/'> WEB </a> </h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li> <a href = "/create/"> create </a> <li>
                {contextUI}
            <ul>
        </body>
    </html>
'''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li> <a href = "/read/{topic["id"]}/"> {topic["title"]} </a> </li>'
    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/read/<id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic["id"]:
            title = topic["title"]
            body = topic["body"]
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id = id)

@app.route("/create/", methods = ["GET", "POST"])
def create():
    print("request.method", request.method)
    if request.method == "GET":
        content = '''
            <form action = "/create/" method = "POST">
                <p> <input type = "text" name = "title" placeholder = "title"> </p>
                <p> <textarea name = "body" placeholder = "body">  </textarea> </p>
                <p> <input type = "submit" value = "create"> </p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == "POST":
        global nextId
        title = request.form["title"]
        body = request.form["body"]
        newTopic = {'id' : nextId, 'title': title, 'body' : body}
        topics.append(newTopic)
        url = "/read/" + str(nextId) + '/'
        nextId += 1
        return redirect(url)

# method에 아무것도 넣지 않으면 기본으로 GET 요청이 되어서
# submit을 눌렀을 때 action으로 지정된 경로에 들어가서 input 값을 ?parameter로 넣는다.
# method에 POST로 요청을 넣으면 URL이 변하지 않은 채로 요청이 된다.

# 정보를 읽어올 때는 GET으로 해서 URL에 정보가 묻어나오게 해도 되지만,
# 정보를 변경할 때는 URL에 정보가 드러나지 않게 하는 것이 좋다.
# 개발자 도구 -> payload에 그 은닉 정보가 들어가있다.

app.run(port = 5001, debug = True)