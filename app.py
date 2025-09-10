#Original Version
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import io, csv

hong_kong_tz = ZoneInfo("Asia/Hong_Kong")

 
app = Flask(__name__)
 
# SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
 
# -- Model --
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(hong_kong_tz), onupdate=lambda: datetime.now(hong_kong_tz), index=True)
    
with app.app_context():
    db.create_all()
 
# CRUD
# Create, Remove, Update, Display
 
@app.route('/', methods=["GET", "POST"]) #landing page
# Commenting any code in VS Code  Ctrl K C
def home():
 
    if request.method == "POST": # Create
       
        # task = request.form.get("task")
        text = (request.form.get("task") or "").strip()
       
        # if task:
        if text:
            # write_task(task)
            db.session.add(Task(text=text))
            db.session.commit()
           
        #return redirect("/")
        return redirect(url_for("home"))
   
    #Display
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks = tasks)
    

@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    # task_to_delete = request.form.get("task_to_delete")
    # tasks = read_tasks()
    # updated_tasks = [task for task in tasks if task != task_to_delete]
   
    # with open(TASK_FILE,"w") as file:
    #     for task in updated_tasks:
    #         file.write(task + "\n")
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    #return redirect("/")
    return redirect(url_for("home"))
 
# # EDITING bonus
@app.route("/edit/<int:id>", methods=["POST"])
def edit_task(id):
    # old_task = request.form.get("old_task")
    # new_task = request.form.get("new_task")
    # tasks = read_tasks()
 
    # updated_tasks = []
    # found = False
    # for task in tasks:
    #     if task == old_task and not found:
    #         updated_tasks.append(new_task)
    #         found = True
    #     else:
    #         updated_tasks.append(task)
 
    # with open(TASK_FILE, "w") as f:
    #     for task in updated_tasks:
    #         f.write(task + "\n")
   
    new_text = (request.form.get("new_task") or "").strip()
    if new_text:
        task=Task.query.get_or_404(id)
        task.text=new_text
        db.session.commit()
    #return redirect("/")
    return redirect(url_for("home"))
 
 
@app.route("/toggle/<int:id>", methods=["POST"])
def toggle_task(id):
    task=Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return("",204)

@app.route("/about")
def about():
    #return render_template("about.html")
    return render_template("Win_About.html")

#CSV Upload
@app.route("/download_csv", methods=["GET"])
def download_csv():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
   
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Task", "Completed", "Created At", "Updated At"])
   
    for task in tasks:
        writer.writerow([task.id,
                         task.text,
                         bool(task.done),
                         task.created_at.isoformat(),
                         task.updated_at.isoformat()])
       
    output.seek(0)
   
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition":"attachment; filename=list_of_tasks.csv"}
    )
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files.get("csv_file")
   
    if not file or file.filename == "":
        return redirect(url_for('home'))
   
    batch_created_at = datetime.now(hong_kong_tz)
   
    raw=file.read()
   
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
       
    new_tasks = []
    reader = csv.reader(io.StringIO(text))
   
    for item, row in enumerate(reader):
        if not row:
            continue
        first_col = (row[0] or "").strip()
        if not first_col:
            continue
       
        if item == 0 and first_col.lower() == "text" and len(row) == 1:
            continue
       
        new_tasks.append(Task(text=first_col, done=False, created_at=batch_created_at))
       
    if new_tasks:
        db.session.add_all(new_tasks)
        db.session.commit()
           
    return redirect(url_for('home'))
 
 
if __name__ == '__main__':
    # app.run(port=8080, debug=True)
    app.run(debug=True)