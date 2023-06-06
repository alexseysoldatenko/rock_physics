import numpy as np
import json
import integral_calculation
from datetime import datetime
import lymbda
import composite
import rock_parametrs
import plot_data
import pandas as pd
from scipy.integrate import dblquad
inv = integral_calculation.integral.inverse


df = pd.DataFrame(None, columns = ['component_number','grid_tetta', 'grid_phi', "time", "square"])
class Experiment():
    def __init__(self, path_start_json, matrix_path_json, inclusions_path_jsons):
        self.__21component__ = {(0,0):(0,0,0,0),(0,1):(0,0,1,1),(0,2):(0,0,2,2),
                                (0,3):(0,0,1,2),(0,4):(0,0,0,2),(0,5):(0,0,0,1),
                                (1,1):(1,1,1,1),(1,2):(1,1,2,2),(1,3):(1,1,1,2),
                                (1,4):(1,1,0,2),(1,5):(1,1,0,1),(2,2):(2,2,2,2),
                                (2,3):(2,2,1,2),(2,4):(2,2,0,2),(2,5):(2,2,0,1),
                                (3,3):(1,2,1,2),(3,4):(1,2,0,2),(3,5):(1,2,0,1),
                                (4,4):(0,2,0,2),(4,5):(0,2,0,1),(5,5):(0,1,0,1)}

        with open(path_start_json, "r") as read_file:
            start_data = json.load(read_file)
        with open("programm\\global_test_info.json", "r") as gl:
            test_number_info = json.load(gl)
        
        self.composite_info = composite.Composite(matrix_path_json, inclusions_path_jsons)
        print(rock_parametrs.rock.from_3x3x3x3_to_6x6(self.composite_info.matrix.Ckmln,self.__21component__))
        print(rock_parametrs.rock.from_3x3x3x3_to_6x6(self.composite_info.inclusions[0].Ckmln,self.__21component__))    
        print(rock_parametrs.rock.from_3x3x3x3_to_6x6(self.composite_info.Cc,self.__21component__)) 
        self.start = datetime.now()
        self.duration = None
        self.type = start_data["type"]
        self.number = test_number_info[self.type]
        self.start_data = start_data
        

        test_number_info[self.type] += 1    
        with open("programm\\global_test_info.json", "w") as gl:
            json.dump(test_number_info, gl, indent=4, default=str)

    
    
    def run_test(self, func, func_matrix_test):
        limits_tetta = [
            [[0,3.14,0.01]],
            [[0,3.14,0.005]],
            [[0,3.14,0.002]]
            ]
        limits_phi = [
            [[0,1.5,0.01],[1.5,1.64,0.005],[1.64,4.64,0.01],[4.64,4.78,0.0005],[4.78,6.28,0.01]],
            [[0,1.5,0.01],[1.5,1.64,0.0005],[1.64,4.64,0.01],[4.64,4.78,0.0005],[4.78,6.28,0.01]],
            [[0,1.5,0.01],[1.5,1.64,0.00025],[1.64,4.64,0.01],[4.64,4.78,0.00025],[4.78,6.28,0.01]],
            [[0,1.5,0.01],[1.5,1.64,0.0001],[1.64,4.64,0.01],[4.64,4.78,0.0001],[4.78,6.28,0.01]],
            [[0,1.54,0.01],[1.54,1.6,0.005],[1.6,4.68,0.01],[4.68,4.74,0.0005],[4.74,6.28,0.01]],
            [[0,1.54,0.01],[1.54,1.6,0.0005],[1.6,4.68,0.01],[4.68,4.74,0.0005],[4.74,6.28,0.01]],
            [[0,1.54,0.01],[1.54,1.6,0.00025],[1.6,4.68,0.01],[4.68,4.74,0.00025],[4.74,6.28,0.01]],
            [[0,1.54,0.01],[1.54,1.6,0.0001],[1.6,4.68,0.01],[4.68,4.74,0.0001],[4.74,6.28,0.01]],
            ]
        if self.type == "one":
            for key, value in self.__21component__.items():
                        value = (0,0,2,2)
                # for grid_tetta in limits_tetta:
                #     for grid_phi in limits_phi:
                        time_start = datetime.now()
                        # self.start_data["limits_tetta"] = grid_tetta
                        # self.start_data["limits_phi"] = grid_phi
                        integral_data = integral_calculation.integral(self.start_data)
                        integral_data.get_axes()
                        #integral_data.get_array(func, args = [self.composite_info,*self.start_data["component"]])
                        integral_data.get_array(func, args = [self.composite_info,*value])
                        graph = plot_data.plot_object([*value], integral_data.res, integral_data.grid_x1, integral_data.grid_x2)
                        # graph.plot6()
                        # for i in [.25, .5, .75]:
                        #     graph.save_slice(i, "phi")
                        #     graph.save_slice(i, "tetta")
                        graph.save_3d()

                        square = integral_data.integral_square()
                        result_time = (datetime.now() - time_start).total_seconds()
                        
                        # result_dict = {"component_number": value, "grid_tetta":grid_tetta, "grid_phi":grid_phi,"time":result_time, "square":square}
                        # with open("result_grid_29.05.2022.txt", "a") as f:
                        #     f.write(str(result_dict)+"\n")
                        # print(*value, limits_tetta.index(grid_tetta), limits_phi.index(grid_phi),"done")
            return {"square": square}
        if self.type == "all":
            # calculation for inclusion
            result_tensor = np.zeros((6,6))
            integral_data = integral_calculation.integral(self.start_data)
            integral_data.get_axes()
            for comp6x6, comp3x3x3x3 in self.__21component__.items():
                integral_data.get_array(func, args = [self.composite_info,*comp3x3x3x3])
                square = integral_data.integral_square()
                result_tensor[comp6x6[0]][comp6x6[1]] = square
                print(comp6x6[0],comp6x6[1])

                
            
            result_tensor += result_tensor.T - np.diag(np.diag(result_tensor))#так как считаю только верхние 21 компоненту, то остальные симметрично отражаю
            np.set_printoptions(precision=6, suppress=True)
            print(result_tensor)

            self.Akmln = rock_parametrs.rock.Voigt_6x6_to_full_3x3x3x3(result_tensor)
            self.gkmln_inclusion = integral_calculation.integral.matrix_transform(self.Akmln)

            
            # calculation for matrix
            
            result_tensor = np.zeros((6,6))
            integral_data = integral_calculation.integral(self.start_data)
            integral_data.get_axes()
            for comp6x6, comp3x3x3x3 in self.__21component__.items():
                integral_data.get_array(func_matrix_test, args = [self.composite_info,*comp3x3x3x3])
                square = integral_data.integral_square()
                result_tensor[comp6x6[0]][comp6x6[1]] = square
                print(comp6x6[0],comp6x6[1])
            
            
            result_tensor += result_tensor.T - np.diag(np.diag(result_tensor))#так как считаю только верхние 21 компоненту, то остальные симметрично отражаю
            
            self.Akmln = rock_parametrs.rock.Voigt_6x6_to_full_3x3x3x3(result_tensor)

            self.gkmln_matrix = integral_calculation.integral.matrix_transform(self.Akmln)
            print(rock_parametrs.rock.full_3x3x3x3_to_Voigt_6x6(self.gkmln_matrix))

    def new_integral(self):
        def get_value(x, y, rock, k, m, l, n):    
            linv = lymbda.LYAMBDA(rock.Cc, x, y, rock.inclusions[0].a1, rock.inclusions[0].a2, rock.inclusions[0].a3)
            return  linv[k, l] * lymbda.Nmn(x, y, rock.inclusions[0].a1, rock.inclusions[0].a2, rock.inclusions[0].a3, n = n, m = m)*np.sin(x)

        result_tensor = np.zeros((6,6))
        for key, value in self.__21component__.items():
            test_lambda = lambda x,y : get_value(x, y, self.composite_info, *value)
            result = dblquad(test_lambda, 0, np.pi*2,lambda x: 0, lambda x: np.pi)
        
            result_tensor[key[0]][key[1]] = -result[0]/(4*np.pi)


        result_tensor += result_tensor.T - np.diag(np.diag(result_tensor))
        
        
        self.Akmln = rock_parametrs.rock.Voigt_6x6_to_full_3x3x3x3(result_tensor)
        self.gkmln_inclusion = integral_calculation.integral.matrix_transform(self.Akmln)
        np.set_printoptions(precision=6, suppress=True)
        print(rock_parametrs.rock.full_3x3x3x3_to_Voigt_6x6(self.gkmln_inclusion))
        

        def get_value_matrix_test(x, y, rock, k, m, l, n):    
            linv = lymbda.LYAMBDA(rock.Cc, x, y, rock.matrix.a1, rock.matrix.a2, rock.matrix.a3)
            return  linv[k, l] * lymbda.Nmn(x, y, rock.matrix.a1, rock.matrix.a2, rock.matrix.a3, n = n, m = m)*np.sin(x)

        result_tensor = np.zeros((6,6))
        for key, value in self.__21component__.items():
            test_lambda = lambda x,y : get_value_matrix_test(x, y, self.composite_info, *value)
            result = dblquad(test_lambda, 0, np.pi*2,lambda x: 0, lambda x: np.pi)
        
            result_tensor[key[0]][key[1]] = -result[0]/(4*np.pi)
        
        result_tensor += result_tensor.T - np.diag(np.diag(result_tensor))
        self.Akmln = rock_parametrs.rock.Voigt_6x6_to_full_3x3x3x3(result_tensor)
        self.gkmln_matrix = integral_calculation.integral.matrix_transform(self.Akmln)
        print(rock_parametrs.rock.full_3x3x3x3_to_Voigt_6x6(self.gkmln_matrix))

    def log_data(self, data_from_calculation):
        """LOG DATA AFTER COMPLITE PROGRAM"""
        if self.type == "one":
            result_json = {}
            result_json["experiment_number"] = self.number
            result_json["experiment_type"] = self.type
            result_json["start"] = self.start
            result_json["duration"] = (datetime.now() - self.start).total_seconds()
            result_json["square"] = data_from_calculation["square"]
            result_json.update(self.start_data)


            with open(f"programm\\tests_json\\{self.type}_{self.number}.json", "w") as log:
                log.write(json.dumps(result_json, indent=4, default=str))
        
        if self.type == "all":
            result_json = {}
            result_json["experiment_number"] = self.number
            result_json["experiment_type"] = self.type
            result_json["start"] = self.start
            result_json["duration"] = (datetime.now() - self.start).total_seconds()
            result_json["square"] = list(np.round(data_from_calculation,6))

            with open(f"programm\\tests_json\\{self.type}_{self.number}.json", "w") as log:
                log.write(json.dumps(result_json, indent=4, default=str))
                
    def final_calculations(self):
        ones_matrix = integral_calculation.integral.eye()

        help_bracket = inv(ones_matrix-np.tensordot(self.gkmln_inclusion,(self.composite_info.inclusions[0].Ckmln-self.composite_info.Cc), axes = ([2,3],[0,1])))
        Cfinal1_inclusion = self.composite_info.inclusions[0].concentration * np.tensordot(self.composite_info.inclusions[0].Ckmln, help_bracket, axes = ([2,3],[0,1]))
        Cfinal2_inclusion = (self.composite_info.inclusions[0].concentration*help_bracket)
        
        help_bracket = inv(ones_matrix-np.tensordot(self.gkmln_matrix,(self.composite_info.matrix.Ckmln-self.composite_info.Cc), axes = ([2,3],[0,1])))
        Cfinal1_matrix = (1-self.composite_info.inclusions[0].concentration) * np.tensordot(self.composite_info.matrix.Ckmln, help_bracket, axes = ([2,3],[0,1]))
        Cfinal2_matrix = ((1-self.composite_info.inclusions[0].concentration)*help_bracket)

        Cfinal1 = Cfinal1_matrix + Cfinal1_inclusion
        Cfinal2 = inv(Cfinal2_matrix + Cfinal2_inclusion)

        self.final = np.tensordot(Cfinal1, Cfinal2, axes = ([2,3],[0,1]))
        
    

def get_value(x, y, rock, k, m, l, n):    
    linv = lymbda.LYAMBDA(rock.Cc, x, y, rock.inclusions[0].a1, rock.inclusions[0].a2, rock.inclusions[0].a3)
    return  linv[k, l] * lymbda.Nmn(tetta = x, phi = y, a1 = rock.inclusions[0].a1, a2 = rock.inclusions[0].a2, a3 = rock.inclusions[0].a3, n = n, m = m)*np.sin(x)

def get_value_matrix_test(x, y, rock, k, m, l, n):    
    linv = lymbda.LYAMBDA(rock.Cc, x, y, rock.matrix.a1, rock.matrix.a2, rock.matrix.a3)
    return  linv[k, l] * lymbda.Nmn(x, y, rock.matrix.a1, rock.matrix.a2, rock.matrix.a3, n = n, m = m)*np.sin(x)

test = Experiment("programm\\all_data_for_pytest\\grid_info_test (5).json",
                  "programm\\all_data_for_pytest\\martix_test.json",
                  ["programm\\all_data_for_pytest\\inclusion_test.json"])
                  
test.run_test(get_value, get_value_matrix_test)


#test.new_integral()

# test.gkmln_inclusion = -np.load("test_sym_incl.npy")

# test.gkmln_matrix = -np.load("test_sym_mat.npy")
test.final_calculations()
# print(rock_parametrs.rock.from_3x3x3x3_to_6x6(test.final,test.__21component__))
print(rock_parametrs.rock.full_3x3x3x3_to_Voigt_6x6(test.final))
# print(rock_parametrs.rock.full_3x3x3x3_to_Voigt_6x6(test.final)-rock_parametrs.rock.from_3x3x3x3_to_6x6(test.final,test.__21component__))
#test.log_data(test.run_test(get_value))



