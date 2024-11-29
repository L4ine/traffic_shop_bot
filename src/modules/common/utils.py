def get_config_file(tg_id: int, client_id: str):
	return f'vless://{client_id}@xray.byabil.ru:443?type=tcp&security=reality&pbk=HFcWm4JvesniAtCJHD3u1bvzuM064at71KMBQJkI9lc&fp=firefox&sni=duckduckgo.com&sid=4b3fd422&spx=%2F&flow=xtls-rprx-vision#XRaybyAbil-{tg_id}'
