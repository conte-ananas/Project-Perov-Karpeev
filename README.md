# Идея
Мы кооперируемся с местными бизнесами(кафе, рестораны, бары), договариваемся, чтобы покупателям давали скидки по нашему паспорту. Ну и, конечно, копеечка нам тоже с этого перепадать будет. 

# Задача
Найти ключевую аудиторию, на которую дет ориентирован проект

# Код
import vk_api
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def main():
  link = 'https://vk.com/topic-143401119_48482985'
  splitted = re.split(r'-|_|/', link)
  if len(splitted) >= 2:
    owner_id = int(splitted[-2])
    post_id = int(splitted[-1])
  token = "тут нужен токен для апи вк но он действует час и в опен соурс я не хочу давать свой короче вот тут получить https://vkhost.github.io/"

  vk_session = vk_api.VkApi(token=token)
  vk = vk_session.get_api()

  all_user_ids = []
  offset = 0
  count = 100

  while True:
    try:
      comments = vk.wall.getComments(
        owner_id=owner_id,
        post_id=post_id,
        count=count,
        offset=offset,
        need_likes=0
      )
    except Exception as e:
      print(e)
      break
    if not comments['items']:
      break
    for item in comments['items']:
      all_user_ids.append(item['from_id'])
    offset += count

  user_ids = list(set(all_user_ids))

  current_year = datetime.now().year

  data = []
  for user_id in user_ids:
    try:
      user_info = vk.users.get(
        user_ids=user_id,
        fields="bdate,sex"
      )
    except Exception as e:
      print(user_id, e)
      continue
    if not user_info:
      print(f"Нема посльзователя с айди {user_id}")
      continue
    user = user_info[0]
    first_name = user.get("first_name", "None")
    sex_test = user.get("sex", 0)
    if sex_test == 1:
      sex = "Женский"
    elif sex_test == 2:
      sex = "Мужской"
    else:
      sex = "None"

    bdate = user.get("bdate", "")
    if bdate and len(bdate.split(".")) == 3:
      birth_year = int(bdate.split(".")[2])
      age = current_year - birth_year
    else:
      age = None

    data.append({
      "first_name": first_name,
      "sex": sex,
      "age": age
    })

  df = pd.DataFrame(data)

  df_with_age = df[df["age"].notna()]

  men = df_with_age[df_with_age["sex"] == "Мужской"]
  women = df_with_age[df_with_age["sex"] == "Женский"]

  fig, axes = plt.subplots(2, 2, figsize=(12, 10))

  axes[0, 0].hist(men["age"], bins=20, color="blue", alpha=0.7, edgecolor="black")
  axes[0, 0].set_title("Мужчины")
  axes[0, 0].set_xlabel("Возраст")
  axes[0, 0].set_ylabel("Количество")

  axes[0, 1].hist(women["age"], bins=20, color="pink", alpha=0.7, edgecolor="black")
  axes[0, 1].set_title("Женщины")
  axes[0, 1].set_xlabel("Возраст")
  axes[0, 1].set_ylabel("Количество")

  axes[1, 1].hist(df_with_age["age"], bins=20, color="green", alpha=0.7, edgecolor="black")
  axes[1, 1].set_title("Общие данные")
  axes[1, 1].set_xlabel("Возраст")
  axes[1, 1].set_ylabel("Количество")

  plt.tight_layout()
  plt.show()

main()
