from database import engine, Base, SessionLocal
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from models import User, Report
Base.metadata.create_all(bind=engine)


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Start a new SQLAlchemy session
db = SessionLocal()

#======== Create a new user object =========
new_user = User(name='John Doe', email='johndoe@example.com')

# Add the new user object to the session
db.add(new_user)

# Commit the transaction
db.commit()

# Close the session
db.close()
## Create Users


######## Query the database ti get user_id for given name ########
db = SessionLocal()
name = "John Doe"
user = db.query(User).filter(User.name == name).first()
print(user.id)

## Create a Report for the user
new_report = Report(report_name='Report1', user_id=user.id)
db.add(new_report)
db.commit()
db.close()


#### Query the database to get all reports for a given user ####
db = SessionLocal()
user = db.query(User).filter(User.name == name).first()
reports = db.query(Report).filter(Report.user_id == user.id).all()
for report in reports:
    print(report.report_name)
db.close()  


# ## ========== Create Reports ============
# # Start a new SQLAlchemy session

# # Create a new report object
# new_report = Report(report_name='Report1', user_id=new_user.id)

# # Add the new report object to the session
# db.add(new_report)

# # Commit the transaction
# db.commit()

# # Close the session


# ##### Query the database #####
# # Create a new SQLAlchemy session for querying the database

# # Get the first user
# user = db.query(User).first()

# # Print the user's name
# print(user.name)

# # Get all reports for this user
# reports = db.query(Report).filter(Report.user_id == user.id).all()

# # Print the report names
# for report in reports:
#     print(report.report_name)

