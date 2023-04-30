from database.database import engine, Base, SessionLocal
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from database.models import User, Report
from typing import List
Base.metadata.create_all(bind=engine)

def create_user(name, email)-> None:
    db = SessionLocal()
    new_user = User(name=name, email=email)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        print(e)
    db.close()

def get_user_id(name) -> int:
    db = SessionLocal()
    user = db.query(User).filter(User.name == name).first()
    db.close()
    return user.id

def get_user_name(user_id) -> str:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user.name

def create_report(report_name, user_id, summary, date, img_path, score ) -> None:
    db = SessionLocal()
    new_report = Report(report_name=report_name, user_id=user_id, summary=summary, date=date, img_path=img_path, score = score)
    try:
        db.add(new_report)
        db.commit()
    except Exception as e:
        print(e)
    db.close()

def get_reports(user_id) -> List[Report]:
    db = SessionLocal()
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    db.close()
    return reports

def get_all_users() -> List[User]:
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def test_functions():
    ## Test Functions
    # Create 3 different users
    create_user("Bob Baumeister", "john.doe@gmail.com")
    create_user("Dora Entdecker", "jane.doe)@gmail.com")
    create_user("John Smith", "john@gmail.com")

    ## Create 2 reports per user
    user_ids = [1,2,3]
    for user_id in user_ids:
        create_report("Report1", user_id, "This is a very nice report /n", "2021-01-01", "img_path1", score = 1)
        create_report("Report2", user_id, "This is another very nice report /n", "2021-01-02", "img_path2", score =10)

    ## Get all reports for a given user
    reports = get_reports(1)
    for report in reports:
        print("Report: ",report.summary)

    # Print all users
    users = get_all_users()
    for user in users:
        print("User: ", user.name)
