from io import StringIO
from flask import Flask, make_response, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class InventoryDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "<Item %r>" % self.id


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        item_content = request.form.get("item")
        new_item = InventoryDB(content=item_content)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except:
            return "Issue adding item"
    else:
        items = InventoryDB.query.order_by(InventoryDB.date_time).all()
        return render_template("index.html", items=items)


@app.route("/delete/<int:id>")
def delete(id):
    del_id = InventoryDB.query.get_or_404(id)
    InventoryDB.query
    try:
        db.session.delete(del_id)
        db.session.commit()
        return redirect("/")
    except:
        return "Issue deleting item"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    up_id = InventoryDB.query.get_or_404(id)
    if request.method == "POST":
        up_id.content = request.form.get("item")
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Issue updating item"
    else:
        return render_template("update.html", item=up_id)


@app.route("/export")
def export():
    items = db.session.query(InventoryDB.content).all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(("Your Inventory",))
    writer.writerows(items)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == "__main__":
    app.run(debug=True)
