#GET retrieve
#POST  write new data
#DELETE delete junk
#PUT write update data

#to add object to table - db.session.add(post)
#then db.session.commit


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



#NO TREALLY NEEDED TO MEORISE MUCH
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

#connecting to datbase, creating model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(80), unique=True, nullable=False)#wont allow blank answers)
    category = db.Column(db.String(120))
    tags = db.Column(db.String(120))



    def __repr__(self):
        return f"{self.title} - {self.content} - {self.category} - {self.tags}"


#table created using db.create_all



@app.route("/")
def index():
    return("hi there")

#GET (basically means print it out)
@app.route("/posts/", methods=["GET"])# i now get it, these parameters are what ypu type in at the end of the link for it to show on the web
def get_all_post():
    posts = Post.query.all()
    output = []
    for post in posts:
        post_data = {"id": post.id, "title": post.title, "content": post.content, "category": post.category, "tags": post.tags}
        output.append(post_data)
    return {"posts": output}
    
    
  
@app.route("/posts/<id>")#getting posts with id, returns a post based on the id inputted
def get_post_by_id(id):   
    post = Post.query.get_or_404(id)
    return({"id": post.id, "title": post.title, "content": post.content, "category": post.category, "tags": post.tags})
        
#creating new data requested by users
@app.route("/posts/", methods=["POST"])
def add_post():
    data = request.json
    if not data or "title" not in data or "content" not in data:
        return({"error": "missing fields required"}), 400
    
    post = Post(title=request.json["title"], content=request.json["content"], category=request.json["category"], tags=request.json["tags"])
    db.session.add(post)
    db.session.commit()
    return("succesfully added requested data."), 201

#delete 
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    
    if post is None:
        return("error detected")
    
    db.session.delete(post)
    db.session.commit()

    
    return("succesfully deleted")
    

