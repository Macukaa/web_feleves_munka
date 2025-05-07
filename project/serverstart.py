import project

app = project.app
app.run(host='localhost', port=8080, debug=False, reloader=True)