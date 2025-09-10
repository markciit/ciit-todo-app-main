#Personal Version
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import io, csv

hong_kong_tz = ZoneInfo("Asia/Hong_Kong")

 
app = Flask(__name__)
 
# SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
 
# -- Model --
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    teacher = db.Column(db.String(255), nullable=False)
    assigned_date = db.Column(db.Boolean, nullable=False, default=False)
    subject = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False, index=True)
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
        text = (request.form.get("task") or "").strip()
        if text:
            db.session.add(Task(text=text))
            db.session.commit()
        #return redirect("/")
        return redirect(url_for("home"))
   
    #Display
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("Win_Home.html", tasks = tasks)

#Add Task
@app.route('/add_task', methods=["POST"])
def add_task():
    """
    Handles the creation of a new task with multiple fields.
    This route would be the target of a form with fields for 'text', 'teacher', and 'subject'.
    """
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        teacher = (request.form.get("teacher") or "").strip()
        subject = (request.form.get("subject") or "").strip()
        #assigned_date = False
        
        # You can add logic here to handle 'assigned_date' if it's a checkbox
        # assigned_date = 'assigned_date' in request.form
        assigned_date = request.form.get("assigned_date") == 'on'

        if text and teacher and subject:
            new_task = Task(text=text, teacher=teacher, subject=subject, assigned_date=assigned_date)
            db.session.add(new_task)
            db.session.commit()

    return redirect(url_for("home"))
 
@app.route("/delete/<int:id>", methods=["POST"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    #return redirect("/")
    return redirect(url_for("home"))
 
# # EDITING bonus
@app.route("/edit/<int:id>", methods=["POST"])
def edit_task(id):
    # Retrieve the new values from the form.
    # We use .get() to safely retrieve values that may not be present.
    new_text = (request.form.get("new_task") or "").strip()
    new_teacher = (request.form.get("new_teacher") or "").strip()
    new_subject = (request.form.get("new_subject") or "").strip()
    
    task = Task.query.get_or_404(id)

    # Update the task with the new data if the form fields were provided.
    if new_text:
        task.text = new_text
    if new_teacher:
        task.teacher = new_teacher
    if new_subject:
        task.subject = new_subject

    db.session.commit()
    return redirect(url_for("home"))
 
 
@app.route("/toggle/<int:id>", methods=["POST"])
def toggle_task(id):
    task=Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return("",204)
 
@app.route("/get_started")
def get_started():
   return render_template("Win_Core.html")

@app.route("/about")
def about():
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