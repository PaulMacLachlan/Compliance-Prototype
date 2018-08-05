from flask import Flask, request, redirect, url_for, render_template
from audit import Audit
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

audits = [Audit('FedRAMP', '2018')]

def find_audit(audit_id):
    return [audit for audit in audits if audit.id == audit_id][0]

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/audits', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        new_audit = Audit(request.form['title'], request.form['year'])
        audits.append(new_audit)
        return redirect(url_for('index'))
    return render_template('index.html', audits=audits)

@app.route('/audits/new')
def new():
    return render_template('new.html')

@app.route('/audits/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    found_audit = find_audit(id)
    if request.method == b'PATCH': # 'b' is related to "byte string" in flask_modus, and is how were accepting the 'PATCH' method
        found_audit.title = request.form['title']
        found_audit.year = request.form['year']
        return render_template('show.html', audit=found_audit)
    if request.method == b'DELETE':
        audits.remove(found_audit)
        return redirect(url_for('index'))
    return render_template('show.html', audit=found_audit)

@app.route('/audits/<int:id>/edit', methods=["GET", "PATCH"])
def edit(id):
    found_audit = find_audit(id)
    return render_template('edit.html', audit=found_audit)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
