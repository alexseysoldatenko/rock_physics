import numpy as np

class integral():
    def __init__(self, data_json):
        """создает оси с лимитами, параметры в json"""

        self.limits = {}
        self.limits["tetta"] = []

        self.limits["phi"] = []
        for i in range(len(data_json["limits_tetta"])):
            self.limits["tetta"].append((data_json["limits_tetta"][i][0], 
                                         data_json["limits_tetta"][i][1], 
                                         data_json["limits_tetta"][i][2]))
                                         
        for i in range(len(data_json["limits_phi"])):
            self.limits["phi"].append((data_json["limits_phi"][i][0], 
                                       data_json["limits_phi"][i][1], 
                                       data_json["limits_phi"][i][2]))
        self.points = {}
    
    def __str__(self):
        rename_tetta = "Tetta Start Stop Step\n"
        rename_phi = "Phi Start Stop Step\n"
        for i in range(len(self.limits["tetta"])):
            rename_tetta += f"{i + 1}.\t{ self.limits['tetta'][i][0] }\t{self.limits['tetta'][i][1]}\t{self.limits['tetta'][i][2]}\n"
        for i in range(len(self.limits["phi"])):
            rename_phi += f"{i + 1}.\t{ self.limits['phi'][i][0] }\t{self.limits['phi'][i][1]}\t{self.limits['phi'][i][2]}\n"
        return str(self.rock_parametrs) +"\n"+ rename_tetta+rename_phi


    def get_axes(self):
        """ params: line_x это [(-np.pi/2, np.pi/, 0.001),(...)], где
            в каждом кортеже лежит начало конец и шаг по участку(граничные точки включаются 1 раз)
            return: возвращает сетку в которой нужно посчитать значения
            ____________________________________________________________
            записывает в поля grid_x1 и grid_x2 посчитанные точки для сетки
            """
        x = [np.array([self.limits["phi"][0][0]])]
        for part in self.limits["phi"]:
            data = np.arange(part[0]+part[2], part[1]+part[2], part[2])
            x.append(data)
        
        y = [np.array([self.limits["tetta"][0][0]])]
        for part in self.limits["tetta"]:
            data = np.arange(part[0]+part[2], part[1]+part[2], part[2])
            y.append(data)
        
        self.grid_phi = np.concatenate( x, axis=0 )
        
        self.grid_tetta = np.concatenate( y, axis=0 )
        
    
    def get_array(self, func,  args = []):
        """
        Возвращает рассчитанные значения сетки
        """
        self.res = np.zeros((self.grid_phi.shape[0], self.grid_tetta.shape[0]))
        for ix, phi in enumerate(self.grid_phi):
            for iy, tetta in enumerate(self.grid_tetta):
                self.res[ix][iy] = func(tetta, phi, *args)
               

    def integral_square(self):
        """Расчет интеграла по кубической формуле"""
        integ = 0
        # self.res_abs = np.abs(self.res)
        self.res_abs = self.res
        for x in range(self.res.shape[0]-1):
            for y in range(self.res.shape[1]-1):
                mean = (self.res_abs[x][y] + self.res_abs[x+1][y] + self.res_abs[x][y+1] + self.res_abs[x+1][y+1])/4
                step_x = self.grid_x1[x+1] - self.grid_x1[x]
                step_y = self.grid_x2[y+1] - self.grid_x2[y]
                integ +=  mean*(step_x * step_y)
        return -integ/(4*np.pi)

    @staticmethod
    def matrix_multiplication(a, b):
        assert a.shape == (3,3,3,3) and b.shape == (3,3,3,3), "a и b должны иметь размеры 3x3x3x3"

        result = np.zeros((3,3,3,3))
        for i, j, k, l in np.ndindex(a.shape):
            for m,n in np.ndindex((3,3)):
                result[i,j,k,l] += a[i,j,m,n] * b[m,n,k,l]

        return result

    @staticmethod
    def matrix_transform(a):
        Aklnm = np.transpose(a,[0,2,3,1])
        Amlnk = np.transpose(a,[1,2,3,0])
        Aknlm = np.transpose(a,[0,3,2,1])
        Amnlk = np.transpose(a,[1,3,2,0])
        result = 0.25*(Aklnm+Amlnk+Aknlm+Amnlk)

        return result

    # @staticmethod
    # def eye():
    #     x = np.array([np.eye(3),np.eye(3),np.eye(3)])
    #     ones_matrix = np.array([x,x,x])
    #     return ones_matrix

    @staticmethod
    def inverse(X):
        component_inv = {0:(0,0),1:(0,1),2:(0,2),3:(1,0),4:(1,1),5:(1,2),6:(2,0),7:(2,1),8:(2,2)}
        A = np.zeros((9,9))
        for n,m in np.ndindex(A.shape):
            comp = (*component_inv[n],*component_inv[m])
            A[n,m] = X[comp]
        inv_sub_matrix = np.linalg.inv(A)
        inv_matrix = np.zeros((3,3,3,3))
        for n,m in np.ndindex(A.shape):
            comp = (*component_inv[n],*component_inv[m])
            inv_matrix[comp] = inv_sub_matrix[n,m]
        return inv_matrix

    @staticmethod
    def eye():
        zeros = np.zeros((3,3,3,3))
        for i,j,k,l in np.ndindex((3,3,3,3)):
            if i == k and j == l:
                zeros[i,j,k,l] = 1
            else:
                zeros[i,j,k,l] = 0
        return zeros



    
    
