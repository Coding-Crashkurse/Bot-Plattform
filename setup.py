import requests

BASE_URL = "http://localhost:8000"

user_payload = {"email": "johndoe@gmail.com", "password": "test"}
user_response = requests.post(f"{BASE_URL}/users/", json=user_payload)
user_data = user_response.json()
print(f"Created user: {user_data}")

bot1_payload = {
    "name": "HomerBot",
    "description": "A bot that speaks like Homer Simpson.",
    "image": "https://www.horizont.net/news/media/17/Homer-Simpson-166443-detailpp.jpeg",
    "url": "http://localhost:4000/chat/",
}
bot1_response = requests.post(f"{BASE_URL}/bots/", json=bot1_payload)
print(f"Created bot 1 (ID 1): {bot1_response.json()}")

bot2_payload = {
    "name": "Jack Sparrow bot",
    "description": "A bot that speaks like Jack Sparrow.",
    "image": "test.JPG",
    "url": "http://localhost:5000/chat/",
}
bot2_response = requests.post(f"{BASE_URL}/bots/", json=bot2_payload)
print(f"Created bot 2 (ID 2): {bot2_response.json()}")

group_payload = {"name": "dfsdfsd"}
group_response = requests.post(f"{BASE_URL}/groups/", json=group_payload)
print(f"Created group (ID 1): {group_response.json()}")

assign_user_response = requests.post(
    f"{BASE_URL}/groups/1/assign-user/",
    params={"user_id": 1},
)
print(f"Assigned user 1 to group 1: {assign_user_response.json()}")

assign_bot1_response = requests.post(
    f"{BASE_URL}/groups/1/assign-bot/", params={"bot_id": 1}
)
print(f"Assigned bot 1 to group 1: {assign_bot1_response.json()}")

assign_bot2_response = requests.post(
    f"{BASE_URL}/groups/1/assign-bot/", params={"bot_id": 2}
)
print(f"Assigned bot 2 to group 1: {assign_bot2_response.json()}")
