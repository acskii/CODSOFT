# DATABASE (Very simple one)
from sqlalchemy.orm import declarative_base, Mapped, sessionmaker, mapped_column
from sqlalchemy import create_engine, String, select

Engine = create_engine('sqlite:///Database.db')
Base = declarative_base()

# Table that contains passwords and their 'names'
class Password(Base):
    __tablename__ = 'passwords'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    def __repr__(self):
        return f'Password(id={self.id}, password={self.password}, name={self.name})'
    
Base.metadata.create_all(bind=Engine)
Session = sessionmaker(bind=Engine)

# NOTE: Check for password existence
def PasswordExists(password):
    with Session() as session:
        stmt = select(Password).where(Password.password == password)
        response = session.scalar(stmt)
        
        return response

# NOTE: Add a new password
def AddPassword(password, name):
    with Session() as session:
        response = PasswordExists(password)
        
        if not response:
            pwd = Password(password=password, name=name)
            session.add(pwd)
            session.commit()
            print("[DATABASE] Added new password!")
        else:
            print('[DATABASE] Password already stored!')
        
# NOTE: Select an existing password
def GetPassword(id):
    with Session() as session:
        stmt = select(Password).where(Password.id == id)
        response = session.scalar(stmt)
        
        if response == None: print(f"[DATABASE] Password of id:'{id}' doesn't exist.")
        return response.first()

# NOTE: Gather all stored passwords and return them
def GetPasswords():
    with Session() as session:
        stmt = select(Password)
        response = session.scalars(stmt).all()
        
        if len(response) == 0: print("[DATABASE] No passwords were stored previously.")
        return response
    
#print(GetPasswords())
# NOTE: Will not add a delete or update, since primary keys get weird (eg. instead of 1,2,3,... -> 5,7,32,...)