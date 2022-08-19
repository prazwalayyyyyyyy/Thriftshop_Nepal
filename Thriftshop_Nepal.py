from app import app, db
#shell work done. we had to run imports everytime. using flask shell premports the application instances lke app which else should have been imported repeatedly using from app import db everytime we had to carry out the test.
#here we create the shell context that adds the database insatance and models to the shell session
from app.models import Goods, User, Post

#same shell work in this block
@app.shell_context_processor #registers function as shell context function.
#When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session. The reason the function returns a dictionary and not a list is that for each item you have to also provide a name under which it will be referenced in the shell, which is given by the dictionary keys.
def make_shell_context():
    return {'db': db, 'User': User, 'Goods': Goods}
    #After you add the shell context processor function you can work with database entities without having to import them
