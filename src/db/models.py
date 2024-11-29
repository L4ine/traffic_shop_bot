from sqlalchemy import Column, Integer, BigInteger, \
	String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)

	username = Column(String, nullable=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=True)

	rent_expired_at = Column(DateTime, nullable=True, default=None)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Payment(Base):
	__tablename__ = 'payments'

	id = Column(Integer, primary_key=True, autoincrement=True)
	tg_id = Column(BigInteger, nullable=False)
	payment_id = Column(String, nullable=False)

	amount = Column(String, nullable=False)
	period = Column(Integer, nullable=False)
	is_successfully = Column(Boolean, nullable=True)

	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
