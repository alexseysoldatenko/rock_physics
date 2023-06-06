import numpy as np
import itertools

class rock():

    def __init__(self, type_add_tensor, composition_part, f_param = 1, concentration = 0, a1 = 1, a2 = 1, a3 = 1000 , k=160, mu = 82, tensor = np.zeros((6,6)), eulerian = [[0,0,0],[0,0,0]]):
        self.composition_part = composition_part
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        if composition_part == "inclusion":
            self.concentration = concentration
            self.f_param = f_param
            self.eulerian = eulerian       

        if type_add_tensor == "isotropic":
            self.k_rock = k
            self.mu_rock = mu
            self.__get_Cklmn_from_k_mu__()
        elif type_add_tensor == "anisotropic":
            self.Ckmln = rock.full_3x3x3x3_to_Voigt_6x6(tensor)

    def __str__(self):
        a = self.__dict__
        res = ""
        for key, value in a.items():
            res += str(key) + ": " + str(value) + "\n"
        return res

         

    def from_6x6_to_3x3x3x3(data: np.ndarray):
        result = np.zeros((3,3,3,3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for m in range(3):
                        if i == 0 and j == 0:
                            x = 0
                        elif i == 1 and j == 1:
                            x = 1
                        elif i == 2 and j == 2:
                            x = 2
                        elif (i == 1 and j == 2) or (i == 2 and j == 1):
                            x = 3
                        elif (i == 0 and j == 2) or (i == 2 and j == 0):
                            x = 4
                        elif (i == 0 and j == 1) or (i == 1 and j == 0):
                            x = 5


                        if k == 0 and m == 0:
                            y = 0
                        elif k == 1 and m == 1:
                            y = 1
                        elif k == 2 and m == 2:
                            y = 2
                        elif (k== 1 and m == 2) or (k == 2 and m == 1):
                            y = 3
                        elif (k == 0 and m == 2) or (k == 2 and m == 0):
                            y = 4
                        elif (k == 0 and m == 1) or (k == 1 and m == 0):
                            y = 5

                        result[i,j,k,m] = data[x,y]
            
        return result

    def from_3x3x3x3_to_6x6(data ,dict_components):
        result = np.zeros((6,6))

        for comp6x6, comp3x3x3x3 in dict_components.items():
            result[comp6x6] = data[comp3x3x3x3]
        result += result.T - np.diag(np.diag(result))
        return result
            

    def __get_Cklmn_from_k_mu__(self):
        lambda_ = self.k_rock - 2 * self.mu_rock / 3 
        c11 = lambda_ + 2 * self.mu_rock
        c12 = lambda_
        c44 = self.mu_rock

        self.C6x6 = np.zeros((6,6))
        self.C6x6[0,0] = c11
        self.C6x6[0,1] = c12
        self.C6x6[0,2] = c12
        self.C6x6[1,0] = c12
        self.C6x6[1,1] = c11
        self.C6x6[1,2] = c12
        self.C6x6[2,0] = c12
        self.C6x6[2,1] = c12
        self.C6x6[2,2] = c11
        self.C6x6[3,3] = c44
        self.C6x6[4,4] = c44
        self.C6x6[5,5] = c44
        self.Ckmln = rock.Voigt_6x6_to_full_3x3x3x3(self.C6x6)
    

    
    def Voigt_6x6_to_full_3x3x3x3(C):
        """
        Convert from the Voigt representation of the stiffness matrix to the full
        3x3x3x3 representation.
        Parameters
        ----------
        C : array_like
            6x6 stiffness matrix (Voigt notation).
        Returns
        -------
        C : array_like
            3x3x3x3 stiffness matrix.
        """
        def full_3x3_to_Voigt_6_index(i, j):
            if i == j:
                return i
            return 6-i-j

        C = np.asarray(C)
        C_out = np.zeros((3,3,3,3), dtype=float)
        for i, j, k, l in itertools.product(range(3), range(3), range(3), range(3)):
            Voigt_i = full_3x3_to_Voigt_6_index(i, j)
            Voigt_j = full_3x3_to_Voigt_6_index(k, l)
            C_out[i, j, k, l] = C[Voigt_i, Voigt_j]
        return C_out
    
    def full_3x3x3x3_to_Voigt_6x6(C, tol=1e-3, check_symmetry=True):
        Voigt_notation = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

        C = np.asarray(C)
        Voigt = np.zeros((6,6))
        for i in range(6):
            for j in range(6):
                k, l = Voigt_notation[i]
                m, n = Voigt_notation[j]
                Voigt[i,j] = C[k,l,m,n]
                """
                print('---')
                print("k,l,m,n", C[k,l,m,n])
                print("m,n,k,l", C[m,n,k,l])
                print("l,k,m,n", C[l,k,m,n])
                print("k,l,n,m", C[k,l,n,m])
                print("m,n,l,k", C[m,n,l,k])
                print("n,m,k,l", C[n,m,k,l])
                print("l,k,n,m", C[l,k,n,m])
                print("n,m,l,k", C[n,m,l,k])
                print('---')
                """
                # if check_symmetry:
                #     assert abs(Voigt[i,j]-C[m,n,k,l]) < tol, \
                #         '1 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], m, n, k, l, C[m,n,k,l])
                #     assert abs(Voigt[i,j]-C[l,k,m,n]) < tol, \
                #         '2 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], l, k, m, n, C[l,k,m,n])
                #     assert abs(Voigt[i,j]-C[k,l,n,m]) < tol, \
                #         '3 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], k, l, n, m, C[k,l,n,m])
                #     assert abs(Voigt[i,j]-C[m,n,l,k]) < tol, \
                #         '4 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], m, n, l, k, C[m,n,l,k])
                #     assert abs(Voigt[i,j]-C[n,m,k,l]) < tol, \
                #         '5 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], n, m, k, l, C[n,m,k,l])
                #     assert abs(Voigt[i,j]-C[l,k,n,m]) < tol, \
                #         '6 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], l, k, n, m, C[l,k,n,m])
                #     assert abs(Voigt[i,j]-C[n,m,l,k]) < tol, \
                #         '7 Voigt[{},{}] = {}, C[{},{},{},{}] = {}' \
                #         .format(i, j, Voigt[i,j], n, m, l, k, C[n,m,l,k])

        return Voigt
"""
    i,j,k,m - компоненты, но не связаны с компонентами k,l,m,n
    [0,0] - [0,0,0,0]
    [0,1] - [0,0,1,1]
    [0,2] - [0,0,2,2]
    [0,3] - [0,0,1,2]
    [0,4] - [0,0,0,2]
    [0,5] - [0,0,0,1]
    [1,1] - [1,1,1,1]
    [1,2] - [1,1,2,2]
    [1,3] - [1,1,1,2]
    [1,4] - [1,1,0,2]
    [1,5] - [1,1,0,1]
    [2,2] - [2,2,2,2]
    [2,3] - [2,2,1,2]
    [2,4] - [2,2,0,2]
    [2,5] - [2,2,0,1]
    [3,3] - [1,2,1,2]
    [3,4] - [1,2,0,2]
    [3,5] - [1,2,0,1]
    [4,4] - [0,2,0,2]
    [4,5] - [0,2,0,1]
    [5,5] - [0,1,0,1]
    """
    