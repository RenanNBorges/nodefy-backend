from flask import Flask, request, jsonify
from flask_cors import CORS  # Adicionei CORS para permitir solicitações entre origens

app = Flask(__name__)
CORS(app)  # Ativando CORS

class Graph:
    def __init__(self):
        self.vertices = {}  # Dicionário para mapear IDs de usuários para objetos Usuario
        self.edges = []     # Lista para armazenar as arestas do grafo

    def add_vertex(self, usuario):
        self.vertices[usuario.id] = usuario

    def add_edge(self, usuario1, usuario2, relationship_type):
        self.edges.append({
            'user_1': usuario1.id,
            'user_2': usuario2.id,
            'relationship_type': relationship_type
        })

class Usuario:
    def __init__(self, id, username, password, email, phone_number, is_org, country_name, state_name, city_name, created_date):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.is_org = is_org
        self.country_name = country_name
        self.state_name = state_name
        self.city_name = city_name
        self.created_date = created_date

        if is_org:
            self.profile = Organizacao()
        else:
            self.profile = Pessoa()

class Pessoa:
    def __init__(self, id, firstname, lastname, birth_date, privacy_settings, friends_total, family_total, followers_total, following_total):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.birth_date = birth_date
        self.privacy_settings = privacy_settings
        self.friends_total = friends_total
        self.family_total = family_total
        self.followers_total = followers_total
        self.following_total = following_total

class Organizacao:
    def __init__(self, id, organization_name, organization_type, organization_area, organization_site, total_clients):
        self.id = id
        self.organization_name = organization_name
        self.organization_type = organization_type
        self.organization_area = organization_area
        self.organization_site = organization_site
        self.total_clients = total_clients


graph = Graph()


# ... Código da classe Graph e definições de classes Usuario, Pessoa, Organizacao ...

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = Usuario(id=data['id'], username=data['username'], password=data['password'], email=data['email'],
                   phone_number=data['phone_number'], is_org=data['is_org'], country_name=data['country_name'],
                   state_name=data['state_name'], city_name=data['city_name'], created_date=data['created_date'])

    graph.add_vertex(user)

    if user.is_org:
        user.profile = Organizacao(id=user.id, organization_name=data['organization_name'],
                                   organization_type=data['organization_type'],
                                   organization_area=data['organization_area'],
                                   organization_site=data['organization_site'], total_clients=data['total_clients'])
    else:
        user.profile = Pessoa(id=user.id, firstname=data['firstname'], lastname=data['lastname'],
                              birth_date=data['birth_date'], privacy_settings=data['privacy_settings'],
                              friends_total=data['friends_total'], family_total=data['family_total'],
                              followers_total=data['followers_total'], following_total=data['following_total'])

    return jsonify({"success": True})


@app.route('/get_users', methods=['GET'])
def get_users():
    users_data = []
    for user in graph.vertices.values():
        user_data = {
            'id': user.id,
            'username': user.username,
            'is_org': user.is_org,
            'profile': vars(user.profile)
        }
        users_data.append(user_data)

    return jsonify({"users": users_data})


if __name__ == '__main__':
    app.run(debug=True)

