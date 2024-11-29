import asyncio
import logging

from modules.common.loader import dp, bot

from modules.start import router as start_router
from modules.profile import router as profile_router
from modules.buy import router as buy_router


if __name__ == "__main__":
	try:
		logging.basicConfig(
			format=u'%(filename)s [LINE:%(lineno)d] \
				#%(levelname)-8s [%(asctime)s]  %(message)s',
			level=logging.INFO,
		)

		loop = asyncio.new_event_loop()

		dp.include_router(start_router)
		dp.include_router(profile_router)
		dp.include_router(buy_router)

		loop.create_task(dp.start_polling(bot))
		logging.info('The bot is running...')

		loop.run_forever()

	except (KeyboardInterrupt, SystemExit):
		logging.error('Bot stopped!')
	except Exception as exc:
		logging.error(exc)
