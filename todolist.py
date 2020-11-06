from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()
running = True
while running:
    rows = session.query(Table).all()
    choice = input("1) Today's tasks\n2) Week's tasks\n3) All Tasks\n4) Missed tasks\n5) Add task\n6) Delete "
                   "task\n0) Exit\n")
    if choice == '1':
        print("Today:")
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            for row in rows:
                print(f"{row.id}. {row.task}")
        else:
            print("Nothing to do!")

    elif choice == '2':
        for i in range(7):
            day = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == day.date()).all()
            print(day.date().strftime(f"\n%A {day.day} %b:"))
            if rows:
                for row in rows:
                    print(f"{row.id}. {row.task}")
            else:
                print("Nothing to do!")
            print()

    elif choice == '3':
        rows = session.query(Table).order_by(Table.deadline).all()
        print("\nAll tasks:")
        for row in rows:
            date = row.deadline.strftime(f"{row.deadline.day} %b")
            print(f"{row.id}. {row.task}. {date}")
        print()

    elif choice == '4':
        print("\nMissed tasks:")
#        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < today.date()).all()
        if rows:
            for row in rows:
                date = row.deadline.strftime(f"{row.deadline.day} %b")
                print(f"{row.id}. {row.task}. {date}")
        else:
            print("Nothing is missed!")
        print()

    elif choice == '5':
        new_task = input("Enter task\n")
        deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
        new_row = Table(task=new_task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    elif choice == '6':
        print("\nChoose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        for row in rows:
            date = row.deadline.strftime(f"{row.deadline.day} %b")
            print(f"{row.id}. {row.task}. {date}")
        chosen_task = int(input())
        session.query(Table).filter(Table.id == chosen_task).delete()
        session.commit()
        print("The task has been deleted!\n")

    elif choice == '0':
        running = False
