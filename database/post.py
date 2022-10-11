from database.dao import DAO
import database.user as user

class Post:
    def __init__(self, user_id, title, created, last_edit = None) -> None:
        self.user_id = user_id
        self.title = title
        self.created = created
        self.last_edit = last_edit or created

class ImagePost(Post):
    def __init__(self, user_id, title, created, image_path, last_edit=None) -> None:
        super().__init__(user_id, title, created, last_edit)
        self.image_path = image_path

class TextPost(Post):
    def __init__(self, user_id, title, created, contents, last_edit=None) -> None:
        super().__init__(user_id, title, created, last_edit)
        self.contents = contents

class PostDisplayInfo:
    def __init__(self, post: Post, author: user.User) -> None:
        self.post = post
        self.author = author

class PostDAO(DAO):
    def _get_table_name(self):
        return 'posts'

    def _data(self, post: Post):
        if isinstance(post, ImagePost):
            return (post.user_id, 0, post.title, post.image_path, post.created, post.last_edit)
        else: # post is a TextPost
            return (post.user_id, 1, post.title, post.contents, post.created, post.last_edit)

    def _store_sql(self):
        return f'''INSERT INTO {self._get_table_name()}
                    VALUES (:author, :post_type, :title, :contents, :created, :edited)'''

    def create_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self._get_table_name()}
                        (author int, post_type int, title text, contents text,
                         created date, edited date)'''
        self.cursor.execute(sql)

    def fetch_all(self):
        tname = self._get_table_name()
        entries = []
        for entry in self.cursor.execute(f'''SELECT rowid, * FROM {tname}
                                             ORDER BY created DESC'''):
            entries.append(entry)

        def mkPost(tup):
            if tup[2] == 0: # image post
                return ImagePost(tup[1], tup[3], tup[5], tup[4], tup[6])
            else: # text post
                return TextPost(tup[1], tup[3], tup[5], tup[4], tup[6])

        return list(map(mkPost, entries))

    def fetch_all_display(self):
        posts = self.fetch_all()
        dposts = []
        userDAO = user.UserDAO()
        for p in posts:
            author_id = p.user_id
            usr = userDAO.get_user_by_id(author_id)
            dposts.append(PostDisplayInfo(p, usr))
        return dposts
    
    def fetch_by_user(self, username: str):
        user_table = 'users'
        post_table = self._get_table_name()
        sql = f'''SELECT {user_table}.username,
                         {user_table}.key,
                         {user_table}.salt,
                         {post_table}.author,
                         {post_table}.post_type,
                         {post_table}.title,
                         {post_table}.created,
                         {post_table}.edited,
                         {post_table}.contents
                  FROM {user_table} INNER JOIN {post_table}
                  ON {user_table}.rowid = {post_table}.author
                  WHERE {user_table}.username = :username
                  ORDER BY {post_table}.created DESC'''
        res = self.cursor.execute(sql, (username,))
        dposts = []
        for row in res:
            username = row[0]
            key = row[1]
            salt = row[2]
            author_id = row[3]
            post_type = row[4]
            title = row[5]
            created = row[6]
            edited = row[7]
            contents = row[8]
            if post_type == 0: # image post
                dposts.append(PostDisplayInfo(
                    ImagePost(author_id, title, created, contents, edited),
                    user.User(username, key, salt)))
            else: # text post
                dposts.append(PostDisplayInfo(
                    TextPost(author_id, title, created, contents, edited),
                    user.User(username, key, salt)))
        return dposts