from app import db

class Employee(db.Model):
    __tablename__ = "Employee"
    employeeId = db.Column(db.String(144), nullable=False, primary_key=True)
    contactNo = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(144), nullable=False)

    def __init__(self, employeeId, contactNo, email):
        self.employeeId = employeeId
        self.contactNo = contactNo
        self.email = email
    
    def json(self):
        return {"employeeId": self.employeeId, "contactNo": self.contactNo}
