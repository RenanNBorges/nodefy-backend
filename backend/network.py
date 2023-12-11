import psycopg
from queue_structure import Queue
from list_structure import Lista_Enc
from user import Person, Organization

class Network:
    def __init__(self, database):
        self.__users = {}
        self.__db = database
        self.__load_users()

    def __contains__(self, username):
        if username in self.__users.keys():
            return True

    def create_user(self, username, fields):
        user_id = self.__users.get(username)
        if not user_id:
            if fields["is_org"] is False:
                self.create_person(username,
                                   "renan",
                                   "renan@email.com",
                                   "51 99999-9999",
                                   1,
                                   21,
                                   10,
                                   "Renan",
                                   "Borges",
                                   "2003-11-06")
            else:
                self.create_organization(username,
                                         "furg",
                                         "furg@email.com",
                                         "53 99999-9999",
                                         1,
                                         21,
                                         17,
                                         "Univeridade Federal do Rio Grande",
                                         "Univerisade",
                                         "Educação",
                                         "furg.br")

        else:
            return print("User already exists")
        pass

    def create_person(self,
                      username,
                      password,
                      email,
                      phone_number,
                      country,
                      state,
                      city,
                      firstname,
                      lastname,
                      birthday
                      ):
        self.__users[username] = Person(self.__db,
                                        username,
                                        password,
                                        email,
                                        phone_number,
                                        country,
                                        state,
                                        city,
                                        firstname,
                                        lastname,
                                        birthday)
        print("Sucessfully created")

    def create_organization(self,
                            username,
                            password,
                            email,
                            phone_number,
                            country,
                            state,
                            city,
                            org_name,
                            org_type,
                            org_area,
                            org_site
                            ):
        self.__users[username] = Organization(self.__db,
                                              username,
                                              password,
                                              email,
                                              phone_number,
                                              country,
                                              state,
                                              city,
                                              org_name,
                                              org_type,
                                              org_area,
                                              org_site)
        print("Sucessfully created")

    def request_relationship(self, username1, username2, relation_type):
        user_id_1 = self.get_user_id(username1)
        user_id_2 = self.get_user_id(username2)
        if (user_id_1 and user_id_2) and (user_id_1 not in self.__users[username2].get_friends(self.__db)):
            with self.__db.cursor() as cursor:
                cursor.execute("""
                INSERT INTO relationshiprequest (user_1, user_2, relationship_type, status)
                VALUES (%s, %s, %s, %s)
                """, (user_id_1, user_id_2, relation_type, 'pending'))
                self.__db.commit()

    def new_friendship(self, username1, username2):
        user_id_1 = self.get_user_id(username1)
        user_id_2 = self.get_user_id(username2)
        if (user_id_1 and user_id_2) and (user_id_1 not in self.__users[username2].get_friends(self.__db)):
            with self.__db.cursor() as cursor:
                request = cursor.execute(f"""
                SELECT request_id, user_2 FROM relationshiprequest WHERE user_1={user_id_1} AND user_2={user_id_2} AND relationship_type='friends'
                """).fetchone()
                self.__users[username1].add_friend(self.__db, request[0], request[1])
                self.__users[username1].add_connection(user_id_1, 'friend')
                self.__users[username2].add_connection(user_id_2, 'friend')
                return True

    def new_follower(self, username1, username2):
        user_id_1 = self.get_user_id(username1)
        user_id_2 = self.get_user_id(username2)
        if (user_id_1 and user_id_2) and (user_id_1 not in self.__users[username2].get_followers(self.__db)):
            self.__users[username1].add_following(self.__db, user_id_2)
            return True

    def new_familiar(self, username1, username2):
        user_id_1 = self.get_user_id(username1)
        user_id_2 = self.get_user_id(username2)
        if (user_id_1 and user_id_2) and (user_id_2 not in self.__users[username1].get_family(self.__db)):
            self.__users[username1].add_family(self.__db, user_id_2)
            self.__users[username1].add_connection(user_id_1, 'family')
            self.__users[username2].add_connection(user_id_2, 'family')
            return True

    def new_client(self, username1, username2):
        user_id_1 = self.get_user_id(username1)
        user_id_2 = self.get_user_id(username2)
        if (user_id_1 and user_id_2) and (isinstance(self.__users[username2], Organization)):
            self.__users[username1].become_client(self.__db, user_id_2)
            print("Yes")
        else:
            print('NO')

    def remove_client(self, username, org_username):
        user_id = self.get_user_id(username)
        org_id = self.get_user_id(org_username)
        if user_id and org_id:
            self.__users[username].unclient(self.__db, org_id)

    def get_user_id(self, username):
        if username in self.__users.keys():
            return self.__users[username].get_id()

    def get_user(self, username):
        if username in self.__users.keys():
            return self.__users[username]

    def __load_users(self):
        with self.__db.cursor() as cursor:
            cursor.execute("""
            SELECT users.username, users.password, users.email, users.phone_number, users.country_name, users.state_name, users.city_name, users.created_date, peoples.firstname, peoples.lastname, peoples.birthday, peoples.privacy_settings
            From users
            INNER JOIN peoples
            ON users.is_org = FALSE""")
            for users in cursor.fetchall():
                self.__users[users[0]] = Person(self.__db, users[0], users[1], users[2], users[3],
                                                users[4], users[5], users[6], users[7],
                                                users[8], users[9])
            cursor.execute("""
                        SELECT users.username, users.password, users.email, users.phone_number, users.country_name, users.state_name, users.city_name, users.created_date, organizations.org_name,organizations.org_type, organizations.org_area, organizations.org_site, organizations.total_clients 
                        From users
                        INNER JOIN organizations
                        ON users.is_org = TRUE""")
            for users in cursor.fetchall():
                self.__users[users[0]] = Organization(self.__db, users[0], users[1], users[2], users[3],
                                                      users[4], users[5], users[6], users[7],
                                                      users[8], users[9], users[10], users[11])

    def find_user(self, username_init, username_dest):
        user_init = self.__users.get(username_init)
        user_dest = self.__users.get(username_dest)
        if user_init:
            visited = Lista_Enc()
            queue = Queue()
            queue.push(user_init)
            while queue.size > 0:
                node = queue.pop()
                for user in node.get_connections().keys():
                    if visited.find_value(user) is False:
                        if user == user_dest.get_id():
                            return user_dest
                        queue.push(self.__users.get(user))
                        visited.insert(user.get_attribute(self.__db, 'username'), visited.size + 1)




    def close(self):
        return self.__db.close()


if __name__ == '__main__':
    db = psycopg.connect("dbname=nodefy user=postgres password=devborges host=localhost port=5432")
    rede = Network(db)
    rede.create_user('renan', {"is_org": False})
    rede.create_user('furg', {"is_org": True})
    rede.create_user('renan2', {"is_org": False})
    rede.create_user('renan3', {"is_org": False})
    rede.request_relationship('renan', 'renan2', 'friends')
    rede.new_friendship('renan', 'renan2')
    rede.request_relationship('renan', 'renan3', 'friends')
    rede.new_friendship('renan', 'renan3')
    print(rede.find_user('0', '44'))
    rede.close()
