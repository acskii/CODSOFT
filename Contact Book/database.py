from sqlalchemy import create_engine, String, ForeignKey, select, or_
from sqlalchemy.orm import Session, sessionmaker, mapped_column, Mapped, relationship, declarative_base
from typing import List, Optional
#import re

ENGINE = create_engine("sqlite:///contacts.db")
Base = declarative_base()

# Contact Table
class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    comment: Mapped[Optional[str]]

    numbers: Mapped[List["Number"]] = relationship(back_populates='contact')

    @property
    def full_name(self):
        return f"{self.first_name}{'' if self.middle_name == None else f' {self.middle_name}'}{'' if self.last_name == None else f' {self.last_name}'}"

    def __repr__(self):
        return f'Contact(id={self.id}, first_name={self.first_name}, middle_name={self.middle_name}, last_name={self.last_name}, email={self.email}, address={self.address}, comment={self.comment}, numbers={self.numbers})'
    
    def __str__(self):
        return f'<Contact id={self.id} name={self.full_name} email={self.email} address={self.address} comment={self.comment} numbers({len(self.numbers)})>'

# Numbers Table
class Number(Base):
    __tablename__ = 'numbers'

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id = mapped_column(ForeignKey("contacts.id"))
    number: Mapped[str] = mapped_column(String(18))

    contact: Mapped["Contact"] = relationship(back_populates='numbers')

    def __repr__(self):
        return f"Number(id={self.id}, contact_id={self.contact_id}, number={self.number}, contact={self.contact})"

# Session Initialiser
Base.metadata.create_all(bind=ENGINE)   
Session = sessionmaker(bind=ENGINE)

# Database Methods
def gather_all_contacts():
    """Selects all contacts stored within database file and returns them as Contact instances."""
    contacts = list()

    session = Session()

    for row in session.execute(select(Contact)):
        contacts.append(row[0])
        
    return contacts

def add_contact(first_name, number):
    """Adds one contact using first name and one number as a base.
       Inputs:
         first_name: Contact's First Name
         number: Contact's First Number
    """
    session = Session()
    con = Contact(first_name=first_name)
    num = Number(number=number, contact=con)
    session.add(num)
    session.commit()

def search_for(pattern):
    """Filters out all contact records using pattern given according to:
       = first_name
       = middle_name
       = last_name
       = numbers 
         - if 'pattern' was only digits

       Inputs:
        pattern: Pattern to search for.
    """
    response = []
    session = Session()

    if not pattern.isdigit():
        stmt = select(Contact).filter(
            or_(
                Contact.first_name.like(f'%{pattern}%'),
                Contact.middle_name.like(f'%{pattern}%'),
                Contact.last_name.like(f'%{pattern}%')
            )
        ).order_by(Contact.first_name)

        response = session.scalars(stmt).all()

    else:
        response = set(session.scalars(select(Contact, Number).join(Contact.numbers).where(Number.number.like(f'%{pattern}%'))).all())
            
    return response

def get_contact_from_id(id):
    """Returns a specified contact according to 'id' inputted."""
    session = Session()
    contact = session.scalars(select(Contact).where(Contact.id == id)).first()
    numbers = contact.numbers
    return (contact, numbers)

def update_contact_value(id, column, new_value):
    """Updates a chosen property of a specified contact.
       Inputs:
         id: Contact's ID
         column: Property to be changed
         new_value: New value assigned to property
    """
    session = Session()
    contact = session.scalar(select(Contact).where(Contact.id == id))

    if contact:
        if column != 'numbers':
            match (column):
                case 'first_name':
                    contact.first_name = new_value
                case 'middle_name':
                    contact.middle_name = new_value
                case 'last_name':
                    contact.last_name = new_value
                case 'email':
                    contact.email = new_value
                case 'comment':
                    contact.comment = new_value
                case 'address':
                    contact.address = new_value
        else:
            if type(new_value) == list and len(new_value) > 0:
                contact.numbers = []

                for value in new_value:
                    num = Number(number=value.strip(), contact=contact)
                    session.add(num)
                    
            else:
                print("[DATABASE]: Requested update, got no new value for 'numbers'")

        session.add(contact)
        session.commit()
        session.close()
    else:
        print(f"[DATABASE: No contact with such ID '{id}'")

def delete_contact(id):
    """Removes a specific contact from the database according to its 'id'"""
    session = Session()
    session.delete(session.scalar(select(Contact).where(Contact.id == id)))
    session.commit()