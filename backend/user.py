class User:
    def __init__(self, db, username, password, email, phone_number, country, state, city, is_org):
        self.__connections = {}
        with db.cursor() as cursor:
            if self._not_in(db, 'users', ('username', f"'{username}'")):
                cursor.execute("""
                INSERT INTO users (username, password, email, phone_number, country_name, state_name, city_name, is_org) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s); 
                """, (username, password, email, phone_number, country, state, city, is_org))
                db.commit()
                self.__id = cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]
            else:
                self.__id = cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]
                for org in self._get_connection(db, 'clientsorganizations', 'uni', 'client_user', ('org_user')):
                    self.add_connection(org, 'cliente')
            self.__username = username

    def __repr__(self):
        return f'{self.__id}'

    def _not_in(self, db, table, tag1, tag2=None):
        with db.cursor() as cursor:
            if tag2:
                if not cursor.execute(
                        f"SELECT * FROM {table} WHERE {tag1[0]}={tag1[1]} and {tag2[0]}={tag2[1]}").fetchone():
                    return True
            else:
                if not cursor.execute(f"SELECT * FROM {table} WHERE {tag1[0]}={tag1[1]}").fetchone():
                    return True

    def _get_connection(self, db, table, direction, user, other_user):
        with db.cursor() as cursor:
            if direction == 'bi':
                where = f'WHERE {user}={self.get_id()} or {other_user}={self.get_id()}'
            else:
                where = f'WHERE {user}={self.get_id()}'

            cursor.execute(f"SELECT {user}, {other_user} FROM {table} {where}")

            relation = []
            for cursor_row in cursor.fetchall():
                if cursor_row[1] != self.get_id():
                    relation.append(cursor_row[1])
                elif cursor_row[0] != self.get_id():
                    relation.append(cursor_row[0])
            return relation

    def become_client(self, db, organization):
        with db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO clientsorganizations (client_user, org_user) 
            VALUES(%s, %s)
            """, (self.get_id(), organization))
            cursor.execute(f'SELECT total_clients FROM organizations WHERE id={organization}')
            clients = cursor.fetchone()[0] + 1
            cursor.execute(f"UPDATE organizations SET total_clients={clients} WHERE id={organization}")
            db.commit()

    def unclient(self, db, organization):
        with db.cursor() as cursor:
            if not self._not_in(db, 'clientsorganizations', ('org_user', organization), ('client_user', self.__id)):
                cursor.execute(
                    f"DELETE FROM clientsorganizations WHERE client_user={self.get_id()} and org_user={organization}")
                cursor.execute(f'SELECT total_clients FROM organizations WHERE id={organization}')
                clients = cursor.fetchone()[0] - 1
                cursor.execute(f"UPDATE organizations SET total_clients={clients} WHERE id={organization}")
                db.commit()

    def get_username(self):
        return self.__username

    def get_id(self):
        return self.__id

    def get_attribute(self, db, attribute):
        with db.cursor() as cursor:
            return cursor.execute(f"SELECT {attribute} from peoples WHERE id={self.get_id()}").fetchone()[0]

    def get_connections(self):
        return self.__connections

    def add_connection(self, user, connect_type):
        self.__connections[user] = connect_type


class Person(User):
    def __init__(self, db, username, password, email, phone_number, country, state, city,
                 firstname, lastname, birthday):
        super().__init__(db, username, password, email, phone_number, country, state, city, False)
        with db.cursor() as cursor:
            if super()._not_in(db, 'peoples', ('id', self.get_id())):
                cursor.execute(
                    f"INSERT INTO peoples (id, firstname, lastname, birthday) VALUES ({self.get_id()}, '{firstname}', '{lastname}', '{birthday}')")
                db.commit()
            else:
                for friend in self.get_friends(db):
                    self.add_connection(friend, connect_type='friends')
                for friend in self.get_family(db):
                    self.add_connection(friend, connect_type='family')
                for friend in self.get_following(db):
                    self.add_connection(friend, connect_type='following')

    def add_friend(self, db, request_id, username):
        with db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO friendships (friendship_id, user_1, user_2, bestfriends) 
            VALUES (%s ,%s, %s, %s)
            """, (request_id, self.get_id(), username, False))
            db.commit()

    def add_following(self, db, user_id):
        with db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO followers (follower_user, follower_of) 
            VALUES(%s, %s) 
            """, (self.get_id(), user_id))
            db.commit()
            self.add_connection(user_id, 'following')

    def add_family(self, db, user_id):
        with db.cursor() as cursor:
            cursor.execute("""
            INSERT INTO familyrelations (user_id, relative_id) 
            VALUES(%s, %s) 
            """, (self.get_id(), user_id))
            db.commit()

    def get_friends(self, db):
        return self._get_connection(db, 'friendships', 'bi', 'user_1', 'user_2')

    def get_followers(self, db):
        return self._get_connection(db, 'followers', 'uni', 'follower_of', 'follower_user')

    def get_following(self, db):
        return self._get_connection(db, 'followers', 'uni', 'follower_user', 'follower_of')

    def get_family(self, db):
        return self._get_connection(db, 'familyrelations', 'bi', 'user_id', 'relative_id')

    def _get_connection(self, db, table, direction, user, other_user):
        with db.cursor() as cursor:
            if direction == 'bi':
                where = f'WHERE {user}={self.get_id()} or {other_user}={self.get_id()}'
            else:
                where = f'WHERE {user}={self.get_id()}'

            cursor.execute(f"SELECT {user}, {other_user} FROM {table} {where}")

            relation = []
            for cursor_row in cursor.fetchall():
                if cursor_row[1] != self.get_id():
                    relation.append(cursor_row[1])
                elif cursor_row[0] != self.get_id():
                    relation.append(cursor_row[0])
            return relation


class Organization(User):
    def __init__(self, db, username, password, email, phone_number, country, state, city,
                 org_name, org_type, org_area, org_site, total_clients=0):
        super().__init__(db, username, password, email, phone_number, country, state, city, True)
        with db.cursor() as cursor:
            if super()._not_in(db, 'organizations', ('id', self.get_id())):
                cursor.execute("""
                        INSERT INTO organizations (id, org_name, org_area, org_type, org_site, total_clients)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """, (self.get_id(), org_name, org_type, org_area, org_site, total_clients))
                db.commit()
