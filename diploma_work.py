import requests


def get_num_id(id):

    if id.isdigit():
        id = id
    else:
        params = {
            'access_token': token,
            'v': '5.92',
            'user_ids': id
        }
        id_res = requests.get('https://api.vk.com/method/users.get', params)
        id = id_res.json()['response'][0]['id']
    return id


def get_user_friends():

    params = {
        'access_token': token,
        'user_id': user_id,
        'v': '5.92'
    }
    try:

        friends = requests.get('https://api.vk.com/method/friends.get', params)
        friends_list = friends.json()['response']['items']

        print('Друзья пользователя: ', friends_list)
        return friends_list

    except KeyError:
        print('KeyError')


def get_user_groups():

    params = {
        'access_token': token,
        'user_id': user_id,
        'v': '5.92'
    }

    user_groups = requests.get('https://api.vk.com/method/groups.get', params)
    user_groups_list = user_groups.json()['response']['items']

    print('Группы пользователя: ', user_groups_list)
    return user_groups_list


def friends_groups(friends_list):

    for friend in friends_list:

        # friends_groups_list = []

        params = {
            'access_token': token,
            'user_id': friends_list,
            # 'extended': 1,
            # 'fields': 'members_count', #лучше потом getByID
            'v': '5.92'
        }

        try:

            response = requests.get('https://api.vk.com/method/groups.get', params)
            friends_groups_list = response.json()['response']['items']
            # friends_groups_list.append(friend_groups_list) # все равно только один друг обрабатывается

            print('Группы друзей: ', friends_groups_list)
            return friends_groups_list

        except KeyError:
            print('KeyError')


def exclusive_groups(user_groups_list, friends_groups_list):

    user_groups_set = set(user_groups_list)
    friends_groups_set = set(friends_groups_list)
    exclusive_groups_set = friends_groups_set.difference(user_groups_set)

    print('Группы друзей, в которых нет пользователя: ', exclusive_groups_set)
    return exclusive_groups_set


def get_groups_info(exclusive_groups_set):

    group_fields = ['name', 'id', 'members_count']

    params = {
        'access_token': token,
        'group_ids': exclusive_groups_set,
        'fields': group_fields,
        'v': '5.92'
    }

    response = requests.get('https://api.vk.com/method/groups.getById', params)
    groups_info = {
        'name': response.json()[response][group_fields[0]],
        'gid': response.json()[response][group_fields[1]],
        'members_count': response.json()[response][group_fields[2]]
    }

    # groups_info = response.json()['response']['items']

    print(groups_info)
    return groups_info


if __name__ == '__main__':

    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    user_id = get_num_id(input('Введите ID пользователя: ')) # работает для 55288484, 5528848
    friends_list = get_user_friends()
    user_groups_list = get_user_groups()
    friends_groups_list = friends_groups(friends_list)
    exclusive_groups_set = exclusive_groups(user_groups_list, friends_groups_list)
    groups_info = get_groups_info(exclusive_groups_set)
