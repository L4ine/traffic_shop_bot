from typing import Optional

import logging
from datetime import datetime, timedelta

from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from data.config import DATABASE_URL

from db.models import User, Payment


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)


async def get_user(tg_id: int) -> Optional[User]:
	async with async_session() as session:
		query = select(User).where(User.tg_id == tg_id)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)


async def user_exists(tg_id: int) -> bool:
	return not not await get_user(tg_id)


async def add_user(
	tg_id: int,
	username: str,
	first_name: str,
	last_name: str,
) -> None:
	async with async_session() as session:
		new_user = User(
			tg_id=tg_id,
			username=username,
			first_name=first_name,
			last_name=last_name,
		)

		session.add(new_user)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def update_user_rent_expired(tg_id: int, days: int):
	async with async_session() as session:
		query = select(User).where(User.tg_id == tg_id)

		try:
			result = await session.execute(query)
			user: User = result.scalars().first()

			if user is None:
				return

			current_date = datetime.now()

			if user.rent_expired_at:
				if current_date < user.rent_expired_at:
					user.rent_expired_at += timedelta(days=days)
				else:
					new_date = current_date + timedelta(days=days)
					user.rent_expired_at = new_date
			else:
				new_date = current_date + timedelta(days=days)
				user.rent_expired_at = new_date

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
			raise exc


async def get_payment(payment_id: int) -> Optional[Payment]:
	async with async_session() as session:
		query = select(Payment).where(Payment.payment_id == payment_id)

		try:
			res = await session.execute(query)
			return res.scalars().first()
		except Exception as exc:
			logging.error(exc)


async def add_payment(
	tg_id: int,
	payment_id: str,
	amount: int,
	period: int,
) -> None:
	async with async_session() as session:
		new_payment = Payment(
			tg_id=tg_id,
			payment_id=payment_id,
			amount=amount,
			period=period,
		)

		session.add(new_payment)

		try:
			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)


async def update_payment_status(payment_id: str, status: bool):
	async with async_session() as session:
		query = select(Payment).where(
			Payment.payment_id == payment_id,
			Payment.is_successfully == False
		).order_by(desc(Payment.created_at))

		try:
			result = await session.execute(query)
			payment: Payment = result.scalars().first()

			if payment is None:
				return

			payment.is_successfully = status

			await session.commit()
		except Exception as exc:
			await session.rollback()
			logging.error(exc)
			raise exc
