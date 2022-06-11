import json
from json import JSONDecodeError

from bp_posts.dao.post import Post
from exception import DataError, DataNameError


class PostDAO:

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """
        Загружает данные из JSON и возвращает список словарей
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataError(f'Файл поврежден {self.path}')
        return posts

    def _load_posts(self):
        """
        Возвращает список экземпляров Post
        """
        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts

    def get_all_posts(self):
        """
        Возвращает все посты
        """
        posts = self._load_posts()
        return posts

    def get_posts_by_user(self, user_name):
        """
        Возвращаем список постов определенного пользователя
        """
        try:
            posts = self.get_all_posts()
            user_posts = []
            for post in posts:
                if post.poster_name == user_name:
                    user_posts.append(post)
        except ValueError:
            raise DataNameError('Такого пользователя нет или пустой список, если у пользователя нет постов')
        return user_posts

    def search_in_contents(self, query):
        """
        Возвращает список постов по ключевому слову
        """
        query_posts = []
        posts = self.get_all_posts()
        for post in posts:
            if query.lower() in post.content.lower():
                query_posts.append(post)
        return query_posts

    def get_post_by_pk(self, pk):
        """
        Возвращает один пост по его идентификатору (pk)
        """
        posts = self.get_all_posts()
        for post in posts:
            if post.pk == pk:
                return post
