import json
import uuid

from urllib.parse import urlencode
from datetime import datetime, timedelta

import aiohttp

from data.config import XRAY_URL, COOKIE


async def xray_client_exists(tg_id: int) -> str | bool:
	tg_id = str(tg_id)

	url = f"{XRAY_URL}/panel/inbound/list"

	headers = {
		"Cookie": COOKIE
	}

	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=headers) as response:
			res = await response.json()
			data = json.loads(res['obj'][0]['settings'])['clients']

	for user in data:
		if user['email'] == tg_id:
			return user


async def add_xray_client(tg_id: int, days: int):
	tg_id = str(tg_id)

	url = f"{XRAY_URL}/panel/inbound/addClient"

	headers = {
		"Cookie": COOKIE,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	current_date = datetime.now()
	new_date = current_date + timedelta(days=days)
	timestamp = int(new_date.timestamp() * 1000)

	data = {
		"id": "1",
		"settings": {
			"clients": [
				{
					"id": str(uuid.uuid4()),
					"flow": "xtls-rprx-vision",
					"email": tg_id,
					"limitIp": 0,
					"totalGB": 0,
					"expiryTime": timestamp,
					"enable": True,
					"tgId": tg_id,
					"subId": tg_id,
					"reset": 0
				}
			]
		}
	}

	data['settings'] = json.dumps(data['settings'])
	encoded_data = urlencode(data)

	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=headers, data=encoded_data) as response:
			if response.status == 200:
				client = await xray_client_exists(tg_id)
				return client


async def update_xray_duration(tg_id: int, client: dict, days: int):
	tg_id = str(tg_id)

	url = f"{XRAY_URL}/panel/inbound/updateClient/{client['id']}"

	headers = {
		"Cookie": COOKIE,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	current_date = datetime.now()

	if current_date.timestamp() * 1000 < client['expiryTime']:
		timestamp = int(client['expiryTime'] + (days * 86_400_000))
	else:
		new_date = current_date + timedelta(days=days)
		timestamp = int(new_date.timestamp() * 1000)

	data = {
		"id": "1",
		"settings": {
			"clients": [
				{
					"id": client['id'],
					"flow": "xtls-rprx-vision",
					"email": tg_id,
					"limitIp": 0,
					"totalGB": 0,
					"expiryTime": timestamp,
					"enable": True,
					"tgId": tg_id,
					"subId": tg_id,
					"reset": 0
				}
			]
		}
	}

	data['settings'] = json.dumps(data['settings'])
	encoded_data = urlencode(data)

	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=headers, data=encoded_data) as response:
			return response.status
