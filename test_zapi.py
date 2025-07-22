import requests

zapi_url = "https://api.z-api.io/instances/3E495433683AD00A6FCD1A7661EB964A/token/C92E63EFCA9BD50AC4270CC4/send-text"

payload = {
    "phone": "5531994296619",
    "message": "Testando Z-API diretamente"
}

res = requests.post(zapi_url, json=payload)
print(res.status_code)
print(res.text)
