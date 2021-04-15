"""
Proyecto 2 (10%)
En GRUPOS de 3 personas
    - Hacer una librería que implemente los métodos encontrados en
    https://github.com/itactuk/estructura2021ene/tree/master/codigo_python_estruct/proyecto2redsocial de una red social
    (como Facebook). (63%)
        o [*] Usuario No Disponible: En tiempo menor a O(n), se pueden aceptar falsos positivos.
        o [*] Parentesco entre 2 personas (incluidos primos segundos, terceros, etc.)
        o [*] Distancia de amigos entre dos personas
        o [*] Tamaño de la red de familia a cierta distancia de parentesco
        o [*] Buscar una persona por nombre: En tiempo menor a O(n)
    - Explicar en los comentarios del código porque eligieron dicha implementación e incluir ventajas y desventajas. (20%)
    - Incluir unittest (15%)
    - Presentación (2%)
"""

import enum
from utilities.bloomfilter import BloomFilter
from utilities.graph import Graph
from utilities.quicksort import quick_sort
from utilities.binarysearch import binary_search
from faker import Faker
fake = Faker()

WARNING = '\033[93m'
END = '\033[0m'


class User:
    def __init__(self, id=0, username=None, name=None):
        self.username = username
        self.name = name
        self.id = id

    def __gt__(self, other):
        return other is not None and self.name < other.name

    def __lt__(self, other):
        return other is not None and self.name > other.name

    def __ge__(self, other):
        return other is not None and self.name >= other.name

    def __le__(self, other):
        return other is not None and self.name <= other.name

    def __eq__(self, other):
        return other is not None and self.name == other.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.id}, {self.name}, {self.username}"

    def __hash__(self):
        return hash(self.username)


class Parentesco(enum.Enum):
    padre = 1  # ó madre
    hijo = 2  # ó hija
    hermano = 3  # ó hermana
    tio = 4  # ó tía
    sobrino = 5  # ó sobrina
    primo_primero = 6
    primo_segundo = 7
    primo_tercero = 8
    primo_cuarto = 9
    no_contemplado = 10


class SocialNetwork:
    userSequence: int
    usernameDb: BloomFilter
    userDb = None
    graph: Graph

    def __init__(self):
        self.userDb = []
        self.graph = Graph()
        self._init_sequence()
        self._re_init_username_db()

    def _init_sequence(self):
        self.userSequence = 0

    def _get_next_seq_val(self):
        self.userSequence += 1
        return self.userSequence

    def _re_init_username_db(self):
        self.usernameDb = BloomFilter(1000000)
        for user in self.userDb:
            self.usernameDb.insert(user.username)

    def insertar(self, user: User):
        user.id = self._get_next_seq_val()
        self.userDb.append(user)
        quick_sort(self.userDb, 0, len(self.userDb) - 1)
        self._re_init_username_db()
        return user

    def friend(self, user1_id: int, user2_id: int):
        self.graph.add_edge(user1_id, user2_id)

    def usuario_disponible(self, nombre_usario: str) -> bool:
        """
        Puede permitir falsos positivos.
        Tomar en cuenta que la cantidad de usarios es muy grande y podría ser que no quepa en la RAM
        :param nombre_usario:
        :return:
        :explanation:
            Se eligio esta implementación porque nos permite una velocidad mayor a las de una búsqueda simple y nos
            permita tener un O(k)
            - pros: tiene una velocidad menor a otros tipo de búsqueda.
            - cons: puede darnos falso positivo o sea que nos indica que el usuario existe cuando no es cierto, consume
                mucho mas memoria y tiene que crearse cada vez se inserte un nuevo elemento.
        """
        result = self.usernameDb.search(nombre_usario)
        return not result

    def parentesco(self, id_persona1: int, id_persona2: int) -> Parentesco:
        """
        Determina el parentesco de persona1 con persona2.
        Si se retorna tío, se indica que la persona1 es tía de la persona2
        Si no es uno de los parentescos listados en la clase Parentesco, retornar Parentesco.no_contemplado
        :param id_persona1:
        :param id_persona2:
        :return:
        :explanation:
            Se utiliza DFS para poder hacer un análisis de la red
            - pros: Solo se recorre hasta encontrar el path que une a los dos nodos.
            - cons: Este necesita recorrer toda la red partiendo de un nodo asi que siempre tendría una velocidad
                O(V + E)
                Almacenamos informaciones no utilizadas para identificar el parentesco como por ejemplo los vertices
                visitados
        """
        result = self.graph.distance(id_persona1, id_persona2)
        if result is not None and result <= Parentesco.primo_cuarto.value:
            return Parentesco(self.graph.distance(id_persona1, id_persona2))
        return Parentesco.no_contemplado

    def distancia_de_amigos(self, id_persona1: int, id_persona2: int) -> int:
        """
        Indica la ruta más corta entre dos personas saltando entre los amigos de las personas.
        Por ej.: Si A es solamente amigo de B y B es solamanente amigo de C,
        entonces la distancia entre A y C es 1, porque tenemos que pasar por B para llegar a C
        Si la distancia es mayor que 10, retornar infinito
        :param id_persona1:
        :param id_persona2:
        :return:
        :explanation:
            Se utiliza DFS para poder hacer un análisis de la red
            - pros: Solo se recorre hasta encontrar el path que une a los dos nodos.
            - cons: Este necesita recorrer toda la red partiendo de un nodo asi que siempre tendría una velocidad
                O(V + E), tenemos que recorrer todos los vertices y almacenar los mismo para no tomarlo en cuenta por lo tanto
            consume muchos espacio para grandes reeds O(V)
        """
        return self.graph.distance(id_persona1, id_persona2)

    def tamano_red_de_familia(self, id_persona, distancia_maxima: int) -> int:
        """
        Cuenta la cantidad de miembros de la familia que tengan una distancia menor igual a distancia_maxima
        :param id_persona:
        :param distancia_maxima: la cantidad de nodos que se deben brincar para llegar a otro nodo
        :return:
        :explanation:
            Se utiliza DFS para poder hacer un análisis de la red
            - pros: tenemos que recorrer todos los vertices y almacenar los mismo para no tomarlo en cuenta por lo tanto
            consume muchos espacio para grandes reeds O(V)
            - cons: Este necesita recorrer toda la red partiendo de un nodo asi que siempre tendría una velocidad
                O(V + E)
        """
        return self.graph.network_count(id_persona, distancia_maxima)

    def buscar_por_nombre(self, nombre: str) -> int:
        """
        Buscar una persona por nombre y retornar su id
        :param nombre:
        :return: id_persona
        :explanation:
            Se utiliza binary search para poder asegurar un tiempo menor a O(n)
            - pros: este es el search mas rápida que podemos hacer por nombre asegurando un tiempo O(log n)
            - cons: para poder hacer un binary search debemos organizar el listado en inserción dándonos un tiempo de
                O(n^2) en el peor de los casos
        """
        user = binary_search(self.userDb, 0, len(self.userDb) - 1, nombre, 'name')
        if user is not None:
            return user.id
        return None


def main():
    sn = SocialNetwork()
    for name in range(1, 100):
        name = fake.name()
        username = name.replace(" ", "_").lower()
        sn.insertar(User(username=username, name=name))

    option = None
    while option is None or option != 8:
        try:
            print("""
        1. Agregar usuario
        2. Hacer amigos dos usuarios (id usuario 1,id usuario 2) 
        3. Buscar usuario (por nombre)
        4. Obtener tamaño de la red (id usuario)
        5. Obtener distancia entre amigos (id usuario 1,id usuario 2)
        6. Obtener parentesco entre amigos (id usuario 1,id usuario 2)
        7. Validar nombre de usuario (nombre de usuario)
        8. Salir 
            """)
            raw_option = input("Elegir una opción: ")

            if not raw_option.isdigit() or int(raw_option) not in (1, 2, 3, 4, 5, 6, 7, 8):
                print(f"{WARNING}Error: opción inválida{END}")
                continue

            option = int(raw_option)

            if option == 1:
                name, username = input("Ingrese nombre y nombre de usuario (nombre,nombre de usuario): ").split(',')
                user = sn.insertar(User(username=username, name=name))
                print(f"Usuario creado: {user}")

            if option == 2:
                raw_input = input("Ingrese id de usuarios (id1,id2): ")
                id_user1, id_user2 = raw_input.split(',')
                sn.friend(int(id_user1), int(id_user2))
                print(f"Usuarios fueron relacionados: {id_user1}, {id_user2}")

            if option == 3:
                term = input("Ingresar nombre: ")
                user = sn.buscar_por_nombre(term)
                print(f"Id del usuario: {user}")

            if option == 4:
                raw_input = input("Ingrese id y maxima distancia(id,maxima distancia): ")
                id_user, max_distance = raw_input.split(',')
                print(f"Tamaño de la red: {sn.tamano_red_de_familia(int(id_user), int(max_distance))}")

            if option == 5:
                raw_input = input("Ingrese id de usuarios (id1,id2): ")
                id_user1, id_user2 = raw_input.split(',')
                print(f"Distancia entre amigos: {sn.distancia_de_amigos(int(id_user1), int(id_user2))}")

            if option == 6:
                raw_input = input("Ingrese id de usuarios (id1,id2): ")
                id_user1, id_user2 = raw_input.split(',')
                print(f"Parentesco de usuario: {sn.parentesco(int(id_user1), int(id_user2))}")

            if option == 7:
                username = input("Ingrese nombre de usuario: ")
                if sn.usuario_disponible(username):
                    print(f"El usuario {username} esta disponible")
                else:
                    print(f"El usuario {username} no esta disponible")
        except Exception as error:
            print(f"{error}")
            continue


if __name__ == "__main__":
    main()
