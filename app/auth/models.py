
from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, ForeignKey, DateTime, Uuid

from app.core.database import Base


class RefreshToken(Base):
    """
    RefreshToken Object.
    Here for check if the refresh otken exist AND if he is acitve.

    Attributs:
        - `id`: int autogenerate 
        - `refresh_token_hash`: str 
        - `is_active`: bool
        - `expires_at`: datetime 
        - `user_id`: int ( ForeignKey ) 
        - `family_id`: UUID   -> represente a session 
        - `family_expires_at`: datetime 

    """

    __tablename__ = 'refreshtokens'

    id: Mapped[int] = mapped_column(
            primary_key=True,
            )

    refresh_token_hash : Mapped[str] = mapped_column(
            String(64),  # because .hexadigest() of SHA256 is exactly 64 bytes 
            nullable=False,
            unique=True,
            index=True,          
            )

    is_active: Mapped[bool] = mapped_column(
            Boolean,
            nullable=False,
            default=True,
            )

    expires_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            nullable=False,
            )

    family_id: Mapped[uuid.UUID] = mapped_column(
            Uuid,
            nullable=False,
            index=True,
            )

    family_expires_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            nullable=False,
            )

    # foreigne keys 
    user_id: Mapped[int] = mapped_column(
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
            index=True, 
            )



            



