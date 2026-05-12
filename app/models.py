from app import db

roadmap_assignments = db.Table(
    "roadmap_assignments",

    db.Column("roadmap_id", db.Integer, db.ForeignKey("road_maps.id", ondelete="CASCADE"), primary_key=True),
    db.Column("authentication_id", db.Integer, db.ForeignKey("authentications.id", ondelete="CASCADE"), primary_key=True))

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    administrator_id = db.Column(db.Integer, db.ForeignKey("administrators.id", ondelete="SET NULL"), nullable=True)

    administrator = db.relationship("Administrator", back_populates="departments")
    employees = db.relationship("Employee", back_populates="department", cascade="all")

class EmployeeEmail(db.Model):
    __tablename__ = "employee_emails"

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    department = db.Column(db.String(150), nullable=False)

class Authentication(db.Model):
    __tablename__ = "authentications"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50))

    employee = db.relationship("Employee", back_populates="authentication", uselist=False)
    administrator = db.relationship("Administrator", back_populates="authentication", uselist=False)

    road_maps = db.relationship("RoadMap", secondary=roadmap_assignments, back_populates="assigned_to")

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    authentication_id = db.Column(db.Integer, db.ForeignKey("authentications.id", ondelete="CASCADE"), unique=True, nullable=False)

    department = db.relationship("Department", back_populates="employees")
    authentication = db.relationship("Authentication", back_populates="employee")

class Administrator(db.Model):
    __tablename__ = "administrators"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    departments = db.relationship("Department", back_populates="administrator")

    authentication_id = db.Column(db.Integer, db.ForeignKey("authentications.id", ondelete="CASCADE"), unique=True, nullable=False)
    authentication = db.relationship("Authentication", back_populates="administrator")
    
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String, nullable=False)
    road_map_id = db.Column(db.Integer, db.ForeignKey("road_maps.id", ondelete="CASCADE"))
    road_map = db.relationship("RoadMap",back_populates="comments")

class RoadMap(db.Model):
    __tablename__ = "road_maps"

    id = db.Column(db.Integer, primary_key=True)
    firm = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(200), nullable=False)
    modules = db.Column(db.JSON, default=list)
    reffered_by = db.Column(db.String(200), nullable=True, default="")
    deal_size = db.Column(db.Integer, nullable=True, default=0)
    opportunity_stage = db.Column(db.String(200), nullable=False, default="Lead")
    exp_closure_date = db.Column(db.DateTime, nullable=True, default=None)
    customer_party = db.Column(db.String(200), nullable=True, default="")
    status = db.Column(db.String(200), nullable=True, default="Lead")

    assigned_to = db.relationship("Authentication", secondary=roadmap_assignments, back_populates="road_maps")

    comments = db.relationship("Comment", back_populates="road_map")