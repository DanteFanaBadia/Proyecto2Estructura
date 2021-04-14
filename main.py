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
        return hash((self.id, self.username, self.name))


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
        self.usernameDb = BloomFilter(len(self.userDb))
        for user in self.userDb:
            self.usernameDb.insert(user.username)

    def insertar(self, user: User):
        user.id = self._get_next_seq_val()
        self.userDb.append(user)
        quick_sort(self.userDb, 0, len(self.userDb) - 1)
        self._re_init_username_db()

    def friend(self, user1: User, user2: User):
        self.graph.add_edge(user1.id, user2.id)

    def usuario_disponible(self, nombre_usario: str) -> bool:
        """
        Puede permitir falsos positivos.
        Tomar en cuenta que la cantidad de usarios es muy grande y podría ser que no quepa en la RAM
        :param nombre_usario:
        :return:
        """
        return not self.usernameDb.search(nombre_usario)

    def parentesco(self, id_persona1: int, id_persona2: int) -> Parentesco:
        """
        Determina el parentesco de persona1 con persona2.
        Si se retorna tío, se indica que la persona1 es tía de la persona2
        Si no es uno de los parentescos listados en la clase Parentesco, retornar Parentesco.no_contemplado
        :param id_persona1:
        :param id_persona2:
        :return:
        """
        result = self.graph.distance(id_persona1, id_persona2)
        if result is not None or result > Parentesco.primo_cuarto:
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
        """
        return self.graph.distance(id_persona1, id_persona2)

    def tamano_red_de_familia(self, id_persona, distancia_maxima: int) -> int:
        """
        Cuenta la cantidad de miembros de la familia que tengan una distancia menor igual a distancia_maxima
        :param id_persona:
        :param distancia_maxima: la cantidad de nodos que se deben brincar para llegar a otro nodo
        :return:
        """
        return self.graph.network_count(id_persona, distancia_maxima)

    def buscar_por_nombre(self, nombre: str) -> int:
        """
        Buscar una persona por nombre y retornar su id
        :param nombre:
        :return: id_persona
        """
        user = binary_search(self.userDb, 0, len(self.userDb) - 1, nombre, 'name')
        if user is not None:
            return user.id
        return None


def main():
    sn = SocialNetwork()
    option = None
    while option is None or option != 7:
        print("""
    1. Agregar usuario
    2. Buscar usuario (por nombre)
    3. Obtener tamaño de la red (id usuario)
    4. Obtener distancia entre amigos (id usuario 1,id usuario 2)
    5. Obtener parentesco entre amigos (id usuario 1,id usuario 2)
    6. Validar nombre de usuario (nombre de usuario)
    7. Salir 
        """)
        raw_option = input("Elegir una opción: ")

        if not raw_option.isdigit() or int(raw_option) not in (1, 2, 3, 4, 5, 6, 7):
            print(f"{WARNING}Error: opción inválida{END}")
            continue

        option = int(raw_option)

        if option == 1:
            name, username = str(input("Ingrese nombre y nombre de usuario (nombre,nombre de usuario): ")).split(',')
            if not sn.usuario_disponible(username):
                print(f"{WARNING}Error: usuario no disponible{END}")
                continue
            sn.insertar(User(username=username, name=name))

        if option == 2:
            term = str(input("Ingresar nombre: "))
            user = sn.buscar_por_nombre(term)
            print(f"Usuario: {user}")

        if option == 3:
            id_user, max_distance = str(input("Ingrese id y maxima distancia(id,maxima distancia): "))
            print(f"Tamaño de la red: {sn.tamano_red_de_familia(int(id_user), int(max_distance))}")

        if option == 4:
            id_user1, id_user2 = str(input("Ingrese id de usuarios (id1,id2): ")).split(',')
            print(f"Distancia entre amigos: {sn.distancia_de_amigos(int(id_user1), int(id_user2))}")

        if option == 5:
            id_user1, id_user2 = str(input("Ingrese id de usuarios (id1,id2): ")).split(',')
            print(f"Parentesco de usuario: {sn.parentesco(int(id_user1), int(id_user2))}")

        if option == 6:
            username = str(input("Ingrese nombre de usuario: "))
            if sn.usuario_disponible(username):
                print(f"El usuario {username} esta disponible")
            else:
                print(f"El usuario {username} no esta disponible")


if __name__ == "__main__":
    main()
