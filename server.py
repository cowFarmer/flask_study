from flask import Flask, request, redirect

app = Flask(__name__)

topics = [
    {'id': 1, 'title': 'html', 'body': 'html is'},
    {'id': 2, 'title': 'css', 'body': 'css is'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is'}
]

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        print(id)
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
            </ul>
        </body>
    </html>
    '''
    
def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/read/<id>/')
def read(id):
    title = ''
    body = ''
    
    for topic in topics:
        if int(id) == topic["id"]:
            title = topic['title']
            body = topic['body']
            break
          
    return template(getContents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': len(topics) + 1, 'title': title, 'body': body}
        topics.append(newTopic)
        url = f'/read/{len(topics)+1}/'
        return redirect(url)
    return template(getContents(), content)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
    
        for topic in topics:
            if id == topic["id"]:
                print(id)
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value={title}></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if int(id) == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = f'/read/{id}/'
        return redirect(url)

app.run(port = 5000, debug = True)