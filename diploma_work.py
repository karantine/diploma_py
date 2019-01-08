import requests
import time


class User:

    def get_num_id(self, user_id):
        if not user_id.isdigit():
            params = {
                'access_token': token,
                'v': '5.92',
                'user_ids': user_id
            }
            id_res = requests.get('https://api.vk.com/method/users.get', params)
            time.sleep(0.33)
            user_id = id_res.json()['response'][0]['id']
        print('-')
        return user_id

    def profile_is_closed(self, user_id):
        params = {
            'access_token': token,
            'v': '5.92',
            'user_ids': user_id
        }
        status = requests.get('https://api.vk.com/method/users.get', params)
        time.sleep(0.33)
        if_is_closed = status.json()['response'][0]['is_closed']
        print('-')
        return if_is_closed

    def get_user_friends(self, user_id):
        params = {
            'access_token': token,
            'user_id': user_id,
            'v': '5.92'
        }
        try:

            friends = requests.get('https://api.vk.com/method/friends.get', params)
            time.sleep(0.33)
            friends_list = friends.json()['response']['items']

        except KeyError:
            print('Страница друга удалена или заблокирована')

        print('-')
        return friends_list

    def get_user_groups(self, user_id):
        params = {
            'access_token': token,
            'user_id': user_id,
            'v': '5.92'
        }

        try:

            user_groups = requests.get('https://api.vk.com/method/groups.get', params)
            time.sleep(0.33)
            user_groups_list = user_groups.json()['response']['items']

        except KeyError:
            print('Информация о пользователе не доступна')

        print('-')
        return user_groups_list

    def friends_groups(self, friends_list):
        friends_groups_list = []

        for friend in friends_list:
            params = {
                'access_token': token,
                'user_id': friend,
                'v': '5.92'
            }

            try:

                response = requests.get('https://api.vk.com/method/groups.get', params)
                time.sleep(0.33)
                temp = response.json()['response']['items']
                friends_groups_list = friends_groups_list + temp

            except KeyError:
                print('Информация о друге не доступна')

            print('-')
            return friends_groups_list

    def exclusive_groups(self, user_groups_list, friends_groups_list):
        user_groups_set = set(user_groups_list)
        friends_groups_set = set(friends_groups_list)
        exclusive_groups_set = user_groups_set.difference(friends_groups_set)

        print('-')
        return exclusive_groups_set

    def get_groups_info(self, exclusive_groups_set):
        group_fields = ['name', 'id', 'members_count']

        groups_string = [str(s) for s in exclusive_groups_set]

        params = {
            'access_token': token,
            'group_ids': ','.join(groups_string),
            'fields': ','.join(group_fields),
            'v': '5.92'
        }

        try:
            response = requests.get('https://api.vk.com/method/groups.getById', params)

            groups_info = response.json()['response']

            with open('secret_groups.json', 'w', encoding = 'utf-8') as f:
                secret_groups = [
                    '{"name": "%s","gid": "%s","members_count": %d }' % (group['name'], group['id'], group['members_count'])
                    for group in groups_info]
                f.write(','.join(secret_groups))

        except KeyError:
            print('Информация о группе не доступна')

        print('-')
        return groups_info

    def api_call(self):

        while True:

            try:
                user_id = self.get_num_id(input('По ID пользователя рограмма выводит в файл список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.\n\nВведите ID пользователя: '))
            except KeyError:
                print('Пользователь не найден')
                user_id = self.get_num_id(input('Введите валидный ID пользователя: '))
            except IndexError:
                print('Пользователь не найден')
                user_id = self.get_num_id(input('Введите валидный ID пользователя: '))

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
    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    user = User()
    user.api_call()

