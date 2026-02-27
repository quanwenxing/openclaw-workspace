import csv
import os
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, g, jsonify, redirect, render_template, request, session, send_file, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

ROLE_LEVEL = {"viewer": 1, "agent": 2, "manager": 3, "admin": 4}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


def now_iso():
    return datetime.utcnow().isoformat(timespec="seconds")


def audit(action, entity, entity_id=None, details=None):
    user_id = session.get("user_id")
    db = get_db()
    db.execute(
        """
        INSERT INTO audit_logs(user_id, action, entity, entity_id, details, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, action, entity, str(entity_id) if entity_id else None, details, now_iso()),
    )
    db.commit()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_type TEXT NOT NULL DEFAULT 'individual',
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            notes TEXT,
            owner_user_id INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(owner_user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            policy_number TEXT,
            insurer TEXT,
            product_name TEXT,
            premium REAL,
            start_date TEXT,
            end_date TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            renewal_reminder_days INTEGER NOT NULL DEFAULT 60,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );

        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            stage TEXT NOT NULL,
            amount REAL,
            expected_close_date TEXT,
            assignee_user_id INTEGER,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(assignee_user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            reminder_date TEXT NOT NULL,
            reminder_type TEXT NOT NULL DEFAULT 'renewal',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY(contract_id) REFERENCES contracts(id)
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            entity_id TEXT,
            details TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    db.commit()

    # seed admin
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute(
            "INSERT INTO users(username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
            ("admin", generate_password_hash("admin1234", method="pbkdf2:sha256"), "admin", now_iso()),
        )
        db.commit()


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapped


def require_role(min_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role = session.get("role", "viewer")
            if ROLE_LEVEL.get(role, 0) < ROLE_LEVEL[min_role]:
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)

        return wrapped

    return decorator


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND active=1", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            audit("login", "users", user["id"], "login success")
            return redirect(url_for("dashboard"))
        flash("ログイン失敗")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    audit("logout", "users", session.get("user_id"), "logout")
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    counts = {
        "customers": db.execute("SELECT COUNT(*) c FROM customers").fetchone()["c"],
        "contracts": db.execute("SELECT COUNT(*) c FROM contracts").fetchone()["c"],
        "opportunities": db.execute("SELECT COUNT(*) c FROM opportunities").fetchone()["c"],
    }
    stage_stats = db.execute(
        "SELECT stage, COUNT(*) cnt FROM opportunities GROUP BY stage ORDER BY cnt DESC"
    ).fetchall()
    upcoming = db.execute(
        """
        SELECT c.id, c.policy_number, c.end_date, cu.name AS customer_name
        FROM contracts c
        JOIN customers cu ON cu.id = c.customer_id
        WHERE c.end_date IS NOT NULL
          AND date(c.end_date) <= date('now', '+60 day')
          AND c.status='active'
        ORDER BY date(c.end_date) ASC
        LIMIT 10
        """
    ).fetchall()
    return render_template("dashboard.html", counts=counts, stage_stats=stage_stats, upcoming=upcoming)


@app.route("/customers", methods=["GET"])
@login_required
def list_customers():
    db = get_db()
    rows = db.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/customers", methods=["POST"])
@login_required
@require_role("agent")
def create_customer():
    data = request.get_json(force=True)
    now = now_iso()
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO customers(customer_type, name, email, phone, address, notes, owner_user_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("customer_type", "individual"),
            data["name"],
            data.get("email"),
            data.get("phone"),
            data.get("address"),
            data.get("notes"),
            session.get("user_id"),
            now,
            now,
        ),
    )
    db.commit()
    audit("create", "customers", cur.lastrowid, f"name={data.get('name')}")
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/customers/<int:customer_id>", methods=["PUT"])
@login_required
@require_role("agent")
def update_customer(customer_id):
    data = request.get_json(force=True)
    db = get_db()
    db.execute(
        """
        UPDATE customers
        SET customer_type=?, name=?, email=?, phone=?, address=?, notes=?, updated_at=?
        WHERE id=?
        """,
        (
            data.get("customer_type", "individual"),
            data["name"],
            data.get("email"),
            data.get("phone"),
            data.get("address"),
            data.get("notes"),
            now_iso(),
            customer_id,
        ),
    )
    db.commit()
    audit("update", "customers", customer_id, "customer updated")
    return jsonify({"ok": True})


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
@login_required
@require_role("manager")
def delete_customer(customer_id):
    db = get_db()
    db.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    db.commit()
    audit("delete", "customers", customer_id, "customer deleted")
    return jsonify({"ok": True})


@app.route("/contracts", methods=["GET"])
@login_required
def list_contracts():
    db = get_db()
    rows = db.execute(
        """
        SELECT c.*, cu.name AS customer_name
        FROM contracts c
        JOIN customers cu ON cu.id = c.customer_id
        ORDER BY c.id DESC
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/contracts", methods=["POST"])
@login_required
@require_role("agent")
def create_contract():
    data = request.get_json(force=True)
    now = now_iso()
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO contracts(customer_id, policy_number, insurer, product_name, premium, start_date, end_date, status, renewal_reminder_days, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["customer_id"],
            data.get("policy_number"),
            data.get("insurer"),
            data.get("product_name"),
            data.get("premium"),
            data.get("start_date"),
            data.get("end_date"),
            data.get("status", "active"),
            int(data.get("renewal_reminder_days", 60)),
            now,
            now,
        ),
    )
    db.commit()
    create_renewal_reminder(cur.lastrowid)
    audit("create", "contracts", cur.lastrowid, f"policy={data.get('policy_number')}")
    return jsonify({"id": cur.lastrowid}), 201


def create_renewal_reminder(contract_id):
    db = get_db()
    row = db.execute("SELECT * FROM contracts WHERE id=?", (contract_id,)).fetchone()
    if not row or not row["end_date"]:
        return
    try:
        end_dt = datetime.fromisoformat(row["end_date"])
    except ValueError:
        return
    reminder_dt = end_dt - timedelta(days=row["renewal_reminder_days"])
    db.execute("DELETE FROM reminders WHERE contract_id=?", (contract_id,))
    db.execute(
        "INSERT INTO reminders(contract_id, reminder_date, reminder_type, status, created_at) VALUES (?, ?, 'renewal', 'pending', ?)",
        (contract_id, reminder_dt.date().isoformat(), now_iso()),
    )
    db.commit()


@app.route("/opportunities", methods=["GET"])
@login_required
def list_opportunities():
    db = get_db()
    rows = db.execute(
        """
        SELECT o.*, c.name AS customer_name, u.username AS assignee_name
        FROM opportunities o
        JOIN customers c ON c.id=o.customer_id
        LEFT JOIN users u ON u.id=o.assignee_user_id
        ORDER BY o.id DESC
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/opportunities", methods=["POST"])
@login_required
@require_role("agent")
def create_opportunity():
    data = request.get_json(force=True)
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO opportunities(customer_id, title, stage, amount, expected_close_date, assignee_user_id, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["customer_id"],
            data["title"],
            data.get("stage", "lead"),
            data.get("amount"),
            data.get("expected_close_date"),
            data.get("assignee_user_id", session.get("user_id")),
            data.get("notes"),
            now_iso(),
            now_iso(),
        ),
    )
    db.commit()
    audit("create", "opportunities", cur.lastrowid, f"title={data.get('title')}")
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/reminders", methods=["GET"])
@login_required
def list_reminders():
    db = get_db()
    rows = db.execute(
        """
        SELECT r.*, c.policy_number, c.end_date, cu.name AS customer_name
        FROM reminders r
        JOIN contracts c ON c.id=r.contract_id
        JOIN customers cu ON cu.id=c.customer_id
        WHERE r.status='pending'
        ORDER BY date(r.reminder_date) ASC
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/reminders/<int:reminder_id>/done", methods=["POST"])
@login_required
@require_role("agent")
def reminder_done(reminder_id):
    db = get_db()
    db.execute("UPDATE reminders SET status='done' WHERE id=?", (reminder_id,))
    db.commit()
    audit("update", "reminders", reminder_id, "marked done")
    return jsonify({"ok": True})


@app.route("/users", methods=["GET"])
@login_required
@require_role("admin")
def list_users():
    db = get_db()
    rows = db.execute("SELECT id, username, role, active, created_at FROM users ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/users", methods=["POST"])
@login_required
@require_role("admin")
def create_user():
    data = request.get_json(force=True)
    db = get_db()
    cur = db.execute(
        "INSERT INTO users(username, password_hash, role, active, created_at) VALUES (?, ?, ?, 1, ?)",
        (data["username"], generate_password_hash(data["password"], method="pbkdf2:sha256"), data.get("role", "agent"), now_iso()),
    )
    db.commit()
    audit("create", "users", cur.lastrowid, f"username={data.get('username')}")
    return jsonify({"id": cur.lastrowid}), 201


@app.route("/audit-logs", methods=["GET"])
@login_required
@require_role("manager")
def audit_logs():
    db = get_db()
    rows = db.execute(
        """
        SELECT a.*, u.username
        FROM audit_logs a
        LEFT JOIN users u ON u.id = a.user_id
        ORDER BY a.id DESC
        LIMIT 500
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/csv/export/<string:entity>")
@login_required
@require_role("manager")
def export_csv(entity):
    db = get_db()
    if entity not in {"customers", "contracts", "opportunities"}:
        return jsonify({"error": "unsupported"}), 400
    rows = db.execute(f"SELECT * FROM {entity}").fetchall()
    out_path = os.path.join(EXPORT_DIR, f"{entity}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if rows:
            writer.writerow(rows[0].keys())
            for r in rows:
                writer.writerow([r[k] for k in r.keys()])
    audit("export", entity, details=f"rows={len(rows)}")
    return send_file(out_path, as_attachment=True)


@app.route("/csv/import/<string:entity>", methods=["POST"])
@login_required
@require_role("manager")
def import_csv(entity):
    if entity not in {"customers", "contracts"}:
        return jsonify({"error": "unsupported"}), 400
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 400

    f = request.files["file"]
    reader = csv.DictReader(f.stream.read().decode("utf-8-sig").splitlines())
    db = get_db()
    count = 0

    if entity == "customers":
        for row in reader:
            db.execute(
                """
                INSERT INTO customers(customer_type, name, email, phone, address, notes, owner_user_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.get("customer_type", "individual"),
                    row.get("name"),
                    row.get("email"),
                    row.get("phone"),
                    row.get("address"),
                    row.get("notes"),
                    session.get("user_id"),
                    now_iso(),
                    now_iso(),
                ),
            )
            count += 1

    if entity == "contracts":
        for row in reader:
            db.execute(
                """
                INSERT INTO contracts(customer_id, policy_number, insurer, product_name, premium, start_date, end_date, status, renewal_reminder_days, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(row.get("customer_id")),
                    row.get("policy_number"),
                    row.get("insurer"),
                    row.get("product_name"),
                    float(row["premium"]) if row.get("premium") else None,
                    row.get("start_date"),
                    row.get("end_date"),
                    row.get("status", "active"),
                    int(row.get("renewal_reminder_days") or 60),
                    now_iso(),
                    now_iso(),
                ),
            )
            count += 1

    db.commit()
    if entity == "contracts":
        rows = db.execute("SELECT id FROM contracts ORDER BY id DESC LIMIT ?", (count,)).fetchall()
        for r in rows:
            create_renewal_reminder(r["id"])

    audit("import", entity, details=f"rows={count}")
    return jsonify({"imported": count})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
