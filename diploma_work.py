import requests
import time

TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


class User:

    def __init__(self, token):
        self.token = token

    def _request_get(self, url, request_parameters, number_of_attempts=3):
        if 'access_token' not in request_parameters.keys():
            request_parameters['access_token'] = self.token
        for i in range(number_of_attempts):
            try:
                response = requests.get(url, request_parameters)
                response_json = response.json()
                return response_json['response']
            except KeyError:
                print("Не удалось получить ответ от АПИ, всего попыток: %s." % i)
                if 'error' in response_json.keys():
                    print(response_json['error']['error_msg'])
                    return response_json['error']['error_msg']
                time.sleep(1)

    def get_num_id(self, user_id):
        if not user_id.isdigit():
            params = {
                'v': '5.92',
                'user_ids': user_id
            }
            id_res = self._request_get('https://api.vk.com/method/users.get', params)
            user_id = int(id_res[0]['id'])
        print('Проверяем ID пользователя')
        return user_id

    def profile_is_closed(self, user_id):
        params = {
            'v': '5.92',
            'user_ids': user_id
        }
        status = self._request_get('https://api.vk.com/method/users.get', params)
        if_is_closed = status[0]['is_closed']
        print('Проверяем статус аккаунта')
        return if_is_closed

    def get_user_friends(self, user_id):
        params = {
            'user_id': user_id,
            'v': '5.92'
        }
        friends = self._request_get('https://api.vk.com/method/friends.get', params)
        friends_list = friends['items']
        print('Получен список друзей пользователя')
        return friends_list

    def get_user_groups(self, user_id):
        params = {
            'user_id': user_id,
            'v': '5.92'
        }
        user_groups = self._request_get('https://api.vk.com/method/groups.get', params)
        user_groups_list = user_groups['items']

        print('Получен список групп пользователя')
        return user_groups_list

    def friends_groups(self, friends_list):
        try:

            friends_groups_list = []

            for friend in friends_list:
                params = {
                    'user_id': friend,
                    'v': '5.92'
                }

                response = self._request_get('https://api.vk.com/method/groups.get', params)
                temp = list(response[0])
                friends_groups_list = friends_groups_list + temp
        except KeyError:
            print('Информация о друге не доступна')

        print('Получен список групп друзей пользователя')
        return friends_groups_list

    def exclusive_groups(self, user_groups_list, friends_groups_list):
        user_groups_set = set(user_groups_list)
        friends_groups_set = set(friends_groups_list)
        exclusive_groups_set = user_groups_set.difference(friends_groups_set)

        print('Получен список групп, в которых есть пользователь, но нет его друзей')
        return exclusive_groups_set

    def get_groups_info(self, exclusive_groups_set):

        group_fields = ['name', 'id', 'members_count']
        groups_string = [str(s) for s in exclusive_groups_set]

        params = {
            'group_ids': ','.join(groups_string),
            'fields': ','.join(group_fields),
            'v': '5.92'
        }

        response = self._request_get('https://api.vk.com/method/groups.getById', params)

        groups_info = response

        with open('secret_groups.json', 'w', encoding='utf-8') as f:
            secret_groups = [
                '{"name": "%s","gid": "%s","members_count": %d }' % (group['name'], group['id'], group['members_count'])
                for group in groups_info]
            f.write(','.join(secret_groups))

        print('Создан файл secret_groups.json с информацией о группах\n\n')
        return groups_info

    def api_call(self):

        close_status = self.profile_is_closed(user_id)

        if close_status == False:
            friends_list = self.get_user_friends(user_id)
            user_groups_list = self.get_user_groups(user_id)
            friends_groups_list = self.friends_groups(friends_list)
            exclusive_groups_set = self.exclusive_groups(user_groups_list, friends_groups_list)
            self.get_groups_info(exclusive_groups_set)
        else:
            print('Закрытый аккаунт, информация не доступна')


if __name__ == '__main__':
    user = User(TOKEN)
    while True:

        try:
            user_id = user.get_num_id(input(
                'По ID пользователя программа выводит в файл список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.\nВведите ID пользователя: '))
        except KeyError:
            print('Пользователь не найден')
            user_id = user.get_num_id(input('Введите валидный ID пользователя: '))
        except IndexError:
            print('Пользователь не найден')
            user_id = user.get_num_id(input('Введите валидный ID пользователя: '))
        except TypeError:
            print('Пользователь не найден')
            user_id = user.get_num_id(input('Введите валидный ID пользователя: '))
        user.api_call()

