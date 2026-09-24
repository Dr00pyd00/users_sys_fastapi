
"""
Ici on met juste les type pour postgres, on s'en fiche du 'mail type' par exemple
"""

from datetime import date as datetime_date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from app.core.database import Base 




class User(Base):
    """
    User Model.   
    Assuming the main data for the auth systeme is `email`.

    Required attributs: 
        - `id`: int -> autogenerate
        - `email`: str 
        - `hashed_password`: str 

    Optional attributs: 
        - `username`: str 
        - `first_name`: str 
        - `last_name`: str 
        - `birth`: datetime.date 
        - `phone_number`: str 

    """
    
    # Required ---------------------------------------
    id: Mapped[int] = mapped_column(
            primary_key=True,
            )

    email: Mapped[str] = mapped_column(
            String,
            nullable=False,
            unique=True,
            )

    hashed_password: Mapped[str] = mapped_column(
            String,
            nullable=False,
            )


    # Optional ----------------------------------------
    username: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )

    first_name: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )

    last_name: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )

    birth: Mapped[datetime_date | None] = mapped_column(
            Date,
            nullable=True,
            )

    phone_number: Mapped[str | None] = mapped_column(
            String,
            nullable=True,
            )


    # Foreigns Keys ======================================
        # add here









