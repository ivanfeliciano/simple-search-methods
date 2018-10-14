# encoding: utf-8

def manhattan_distance(p, q):
    """
    Calcula la norma l1 entre dos vectores.

    :param p: un vector p.
    :type p: list
    :param q: el vector q.
    :type q: list
    :return: la distancia entre los vectore p y q.
    :return type: int
    """
    if len(p) == len(q):
        return sum(map(lambda pi, qi: abs(pi - qi), p, q)) 
    raise Exception("p and q should have the same dimensions")