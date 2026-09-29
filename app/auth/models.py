
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, ForeignKey, DateTime

from app.core.database import Base


class RefreshToken(Base):
    """
    RefreshToken Object.
    Here for check if the refresh otken exist AND if he is acitve.

    Attributs:
        - `id`: int autogenerate 
        - `jti`: str -> uuid4 ( the refreshtoken name ) 
        - `is_active`: bool
        - `expire_at`: datetime 
        - `user_id`: int ( ForeignKey ) 

    """

    __tablename__ = 'refreshtokens'

    id: Mapped[int] = mapped_column(
            primary_key=True,
            )

    jti: Mapped[str] = mapped_column(
            String,
            nullable=False,
            unique=True,
            index=True,          
            )

    is_active: Mapped[bool] = mapped_column(
            Boolean,
            nullable=False,
            default=True,
            )

    expire_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            nullable=False,
            )

    # foreigne keys 
    user_id: Mapped[int] = mapped_column(
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
            index=True, 
            )



            



