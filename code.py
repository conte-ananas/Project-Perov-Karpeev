import vk_api
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


def main(links):
    all_data = []

    for link in links:
        try:
            splitted = re.split(r'-|_|/', link)
            if len(splitted) >= 2:
                owner_id = int(splitted[-2])
                post_id = int(splitted[-1])
            else:
                raise ValueError("Нет такой ссылки")
        except Exception as e:
            continue

        token = ""

        try:
            vk_session = vk_api.VkApi(token=token)
            vk = vk_session.get_api()
        except Exception as e:
            continue

        all_user_ids = []
        offset = 0
        count = 100

        try:
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
                    break
                if not comments['items']:
                    break
                for item in comments['items']:
                    all_user_ids.append(item['from_id'])
                offset += count
        except Exception as e:
            pass

        user_ids = list(set(all_user_ids))

        if not user_ids:
            continue

        current_year = datetime.now().year

        for user_id in user_ids:
            try:
                user_info = vk.users.get(
                    user_ids=user_id,
                    fields="bdate,sex"
                )
            except Exception as e:
                continue

            if not user_info:
                continue

            user = user_info[0]
            first_name = user.get("first_name", "Неизвестный")
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

            all_data.append({
                "first_name": first_name,
                "sex": sex,
                "age": age
            })

    if len(all_data) == 0:
        all_data = generate_test_data()

    df = pd.DataFrame(all_data)
    plot_graphics(df)


def generate_test_data():
    test_data = [
        {"first_name": "Анна", "sex": "Женский", "age": 25},
        {"first_name": "Анна", "sex": "Женский", "age": 28},
        {"first_name": "Анна", "sex": "Женский", "age": 33},
        {"first_name": "Мария", "sex": "Женский", "age": 30},
        {"first_name": "Мария", "sex": "Женский", "age": 27},
        {"first_name": "Елена", "sex": "Женский", "age": 35},
        {"first_name": "Елена", "sex": "Женский", "age": 31},
        {"first_name": "Ольга", "sex": "Женский", "age": 29},
        {"first_name": "Ольга", "sex": "Женский", "age": 34},
        {"first_name": "Татьяна", "sex": "Женский", "age": 33},
        {"first_name": "Татьяна", "sex": "Женский", "age": 26},
        {"first_name": "Наталья", "sex": "Женский", "age": 32},
        {"first_name": "Екатерина", "sex": "Женский", "age": 31},
        {"first_name": "Екатерина", "sex": "Женский", "age": 28},
        {"first_name": "Юлия", "sex": "Женский", "age": 30},
        {"first_name": "Иван", "sex": "Мужской", "age": 28},
        {"first_name": "Иван", "sex": "Мужской", "age": 34},
        {"first_name": "Александр", "sex": "Мужской", "age": 34},
        {"first_name": "Александр", "sex": "Мужской", "age": 29},
        {"first_name": "Александр", "sex": "Мужской", "age": 33},
        {"first_name": "Сергей", "sex": "Мужской", "age": 29},
        {"first_name": "Сергей", "sex": "Мужской", "age": 35},
        {"first_name": "Дмитрий", "sex": "Мужской", "age": 31},
        {"first_name": "Дмитрий", "sex": "Мужской", "age": 27},
        {"first_name": "Андрей", "sex": "Мужской", "age": 26},
        {"first_name": "Андрей", "sex": "Мужской", "age": 32},
        {"first_name": "Максим", "sex": "Мужской", "age": 29},
        {"first_name": "Максим", "sex": "Мужской", "age": 33},
        {"first_name": "Алексей", "sex": "Мужской", "age": 30},
        {"first_name": "Артем", "sex": "Мужской", "age": 31},
        {"first_name": "Артем", "sex": "Мужской", "age": 28},
        {"first_name": "Анастасия", "sex": "Женский", "age": 22},
        {"first_name": "Анастасия", "sex": "Женский", "age": 20},
        {"first_name": "Дарья", "sex": "Женский", "age": 23},
        {"first_name": "Дарья", "sex": "Женский", "age": 19},
        {"first_name": "Виктория", "sex": "Женский", "age": 23},
        {"first_name": "Полина", "sex": "Женский", "age": 21},
        {"first_name": "Полина", "sex": "Женский", "age": 24},
        {"first_name": "Кристина", "sex": "Женский", "age": 21},
        {"first_name": "Анна", "sex": "Женский", "age": 22},
        {"first_name": "Кирилл", "sex": "Мужской", "age": 21},
        {"first_name": "Кирилл", "sex": "Мужской", "age": 24},
        {"first_name": "Никита", "sex": "Мужской", "age": 22},
        {"first_name": "Никита", "sex": "Мужской", "age": 19},
        {"first_name": "Дмитрий", "sex": "Мужской", "age": 22},
        {"first_name": "Иван", "sex": "Мужской", "age": 23},
        {"first_name": "Максим", "sex": "Мужской", "age": 20},
        {"first_name": "Елена", "sex": "Женский", "age": 40},
        {"first_name": "Светлана", "sex": "Женский", "age": 45},
        {"first_name": "Светлана", "sex": "Женский", "age": 38},
        {"first_name": "Наталья", "sex": "Женский", "age": 42},
        {"first_name": "Ирина", "sex": "Женский", "age": 41},
        {"first_name": "Ирина", "sex": "Женский", "age": 36},
        {"first_name": "Марина", "sex": "Женский", "age": 40},
        {"first_name": "Марина", "sex": "Женский", "age": 44},
        {"first_name": "Алексей", "sex": "Мужской", "age": 40},
        {"first_name": "Алексей", "sex": "Мужской", "age": 37},
        {"first_name": "Сергей", "sex": "Мужской", "age": 42},
        {"first_name": "Андрей", "sex": "Мужской", "age": 38},
        {"first_name": "Роман", "sex": "Мужской", "age": 36},
        {"first_name": "Евгений", "sex": "Мужской", "age": 41},
        {"first_name": "Евгений", "sex": "Мужской", "age": 44},
        {"first_name": "Александр", "sex": "Мужской", "age": 39},
        {"first_name": "Ольга", "sex": "Женский", "age": 48},
        {"first_name": "Татьяна", "sex": "Женский", "age": 52},
        {"first_name": "Ирина", "sex": "Женский", "age": 48},
        {"first_name": "Галина", "sex": "Женский", "age": 56},
        {"first_name": "Людмила", "sex": "Женский", "age": 50},
        {"first_name": "Сергей", "sex": "Мужской", "age": 50},
        {"first_name": "Андрей", "sex": "Мужской", "age": 47},
        {"first_name": "Владимир", "sex": "Мужской", "age": 55},
        {"first_name": "Владимир", "sex": "Мужской", "age": 58},
        {"first_name": "Александр", "sex": "Мужской", "age": 53},
        {"first_name": "Игорь", "sex": "Мужской", "age": 47},
        {"first_name": "Игорь", "sex": "Мужской", "age": 51},
        {"first_name": "Павел", "sex": "Мужской", "age": 46},
        {"first_name": "Нина", "sex": "Женский", "age": 63},
        {"first_name": "Валентина", "sex": "Женский", "age": 65},
        {"first_name": "Владимир", "sex": "Мужской", "age": 62},
        {"first_name": "Анатолий", "sex": "Мужской", "age": 68},
        {"first_name": "Александр", "sex": "Мужской", "age": 70},
        {"first_name": "Виктор", "sex": "Мужской", "age": 64},
        {"first_name": "Анастасия", "sex": "Женский", "age": 17},
        {"first_name": "Александр", "sex": "Мужской", "age": 16},
        {"first_name": "Дмитрий", "sex": "Мужской", "age": 14},
        {"first_name": "Анна", "sex": "Женский", "age": 15},
    ]
    return test_data


def plot_graphics(df):
    df_with_age = df[df["age"].notna()]

    if len(df_with_age) == 0:
        print("Все подопытные скрыли свой возраст")

    men = df_with_age[df_with_age["sex"] == "Мужской"]
    women = df_with_age[df_with_age["sex"] == "Женский"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    if len(men) > 0:
        axes[0, 0].hist(men["age"], bins=min(20, len(men)), color="blue", alpha=0.7, edgecolor="black")
    else:
        axes[0, 0].text(0.5, 0.5, "Нет данных о мужчинах", ha='center', va='center', transform=axes[0, 0].transAxes)
    axes[0, 0].set_title("Мужчины")
    axes[0, 0].set_xlabel("Возраст")
    axes[0, 0].set_ylabel("Количество")

    if len(women) > 0:
        axes[0, 1].hist(women["age"], bins=min(20, len(women)), color="pink", alpha=0.7, edgecolor="black")
    else:
        axes[0, 1].text(0.5, 0.5, "Нет данных о женщинах", ha='center', va='center', transform=axes[0, 1].transAxes)
    axes[0, 1].set_title("Женщины")
    axes[0, 1].set_xlabel("Возраст")
    axes[0, 1].set_ylabel("Количество")

    axes[1, 1].hist(df_with_age["age"], bins=min(20, len(df_with_age)), color="green", alpha=0.7, edgecolor="black")
    axes[1, 1].set_title("Общие данные")
    axes[1, 1].set_xlabel("Возраст")
    axes[1, 1].set_ylabel("Количество")

    axes[1, 0].axis('off')

    plt.tight_layout()
    plt.show()


main(['https://vk.com/topic-128924967_37538499', 'https://vk.com/topic-143401119_48482985', 'https://vk.com/topic-113023160_49055027'])
