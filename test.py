import unittest
from main import User, SocialNetwork, Parentesco

user_1 = User(1, "aamina", "Aamina")
user_2 = User(2, "ayyub", "Ayyub")
user_3 = User(3, "eben", "Eben")
user_4 = User(4, "elis", "Elis")
user_5 = User(5, "hashim", "Hashim")
user_6 = User(6, "roshni", "Roshni")
user_7 = User(7, "simona", "Simona")
user_8 = User(8, "tanisha", "Tanisha")
user_9 = User(9, "taslima", "Taslima")
user_10 = User(10, "ty", "Ty")
user_11 = User(11, "dante", "Dante")
user_12 = User(12, "jeyry", "Jeyry")

USERS = [
    user_1,
    user_2,
    user_3,
    user_4,
    user_5,
    user_6,
    user_7,
    user_8,
    user_9,
    user_10,
    user_11,
    user_12
]


def get_social_network():
    return SocialNetwork()


class Test(unittest.TestCase):
    def test_usuario_disponible(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.insertar(user_5)
        self.assertEqual(False, sn.usuario_disponible(user_1.username))

    def test_usuario_no_disponible(self):
        sn = get_social_network()
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.insertar(user_5)
        self.assertEqual(False, sn.usuario_disponible(user_1.username))

    def test_buscar_por_nombre_found(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.insertar(user_5)
        sn.insertar(user_6)
        sn.insertar(user_7)
        sn.insertar(user_8)
        sn.insertar(user_9)
        sn.insertar(user_10)
        sn.insertar(user_11)
        sn.insertar(user_12)
        self.assertEqual(user_1.id, sn.buscar_por_nombre(user_1.name))

    def test_buscar_por_nombre_not_found(self):
        sn = get_social_network()
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.insertar(user_5)
        sn.insertar(user_6)
        sn.insertar(user_7)
        sn.insertar(user_8)
        sn.insertar(user_9)
        sn.insertar(user_10)
        self.assertEqual(None, sn.buscar_por_nombre(user_1.name))

    def test_distance_2(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.friend(user_1.id, user_2.id)
        sn.friend(user_2.id, user_3.id)
        sn.friend(user_3.id, user_1.id)
        self.assertEqual(2, sn.distancia_de_amigos(user_1.id, user_3.id))

    def test_distance_infinity(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.insertar(user_5)
        sn.insertar(user_6)
        sn.insertar(user_7)
        sn.insertar(user_8)
        sn.insertar(user_9)
        sn.insertar(user_10)
        sn.insertar(user_11)
        sn.insertar(user_12)

        sn.friend(user_1.id, user_2.id)
        sn.friend(user_2.id, user_3.id)
        sn.friend(user_3.id, user_4.id)
        sn.friend(user_4.id, user_5.id)
        sn.friend(user_5.id, user_6.id)
        sn.friend(user_6.id, user_7.id)
        sn.friend(user_7.id, user_8.id)
        sn.friend(user_8.id, user_9.id)
        sn.friend(user_9.id, user_10.id)
        sn.friend(user_10.id, user_11.id)
        sn.friend(user_11.id, user_12.id)
        sn.friend(user_12.id, user_1.id)
        self.assertEqual(float('inf'), sn.distancia_de_amigos(user_1.id, user_12.id))

    def test_distance_none(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        self.assertEqual(None, sn.distancia_de_amigos(user_1.id, user_2.id))

    def test_parentesco(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.friend(user_1.id, user_2.id)
        self.assertEqual(Parentesco.padre, sn.parentesco(user_1.id, user_2.id))

    def test_tamano_red_de_familia_eq_4(self):
        sn = get_social_network()
        sn.insertar(user_1)
        sn.insertar(user_2)
        sn.insertar(user_3)
        sn.insertar(user_4)
        sn.friend(user_1.id, user_2.id)
        sn.friend(user_2.id, user_1.id)
        sn.friend(user_2.id, user_3.id)
        sn.friend(user_2.id, user_4.id)
        self.assertEqual(4, sn.tamano_red_de_familia(user_1.id, 10))


if __name__ == '__main__':
    unittest.main()
