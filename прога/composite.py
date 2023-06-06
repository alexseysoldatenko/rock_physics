import json
import rock_parametrs

class Composite():
    def __init__(self, matrix_path, inclusions_paths):
        self.__get_matrix__(matrix_path)
        assert len(inclusions_paths) != 0, "количество включений должно быть отлично от нуля"
        self.__get_inclusions__(inclusions_paths)
        self.__get_Cc_with_fparam__(0)
        
    
    def __get_matrix__(self, matrix_path):
        with open(matrix_path, "r") as read_file:
            matrix_info = json.load(read_file)
        
        if matrix_info["type_add_tensor"] == "isotropic":
            self.matrix = rock_parametrs.rock(matrix_info["type_add_tensor"],
                                              matrix_info["composition_part"],
                                              k=matrix_info["k"],
                                              mu=matrix_info["mu"])
        elif matrix_info["type_add_tensor"] == "anisotropic":
            self.matrix = rock_parametrs.rock(matrix_info["type_add_tensor"],
                                              matrix_info["composition_part"],
                                              tensor = matrix_info["tensor"])
        else:
            assert False, "Unknown type add tensor, only isotropic and anisotropic allowed"

    def __get_inclusions__(self, inclusions_paths):
        """
        Method for getting list of rocks
        """
        self.inclusions = []
        for i in range(len(inclusions_paths)):
            with open(inclusions_paths[i], "r") as read_file:
                inclusion_info = json.load(read_file)
            if inclusion_info["type_add_tensor"] == "isotropic":
                inclusion = rock_parametrs.rock(inclusion_info["type_add_tensor"],
                                                inclusion_info["composition_part"],
                                                f_param = inclusion_info["f"],
                                                concentration = inclusion_info["concentration"],
                                                a1 = inclusion_info["a1"],
                                                a2 = inclusion_info["a2"],
                                                a3 = inclusion_info["a3"],
                                                k = inclusion_info["k"],
                                                mu = inclusion_info["mu"],
                                                eulerian= inclusion_info["eulerian_angles"])
            elif inclusion_info["type_add_tensor"] == "anisotropic":
                inclusion = rock_parametrs.rock(inclusion_info["type_add_tensor"],
                                                inclusion_info["composition_part"],
                                                f_param = inclusion_info["f"],
                                                concentration = inclusion_info["concentration"],
                                                a1 = inclusion_info["a1"],
                                                a2 = inclusion_info["a2"],
                                                a3 = inclusion_info["a3"],
                                                tensor = inclusion_info["tensor"],
                                                eulerian= inclusion_info["eulerian_angles"])
            else:
                assert False, "Unknown type add tensor, only isotropic and anisotropic allowed"
            self.inclusions.append(inclusion) 

    def __get_Cc_with_fparam__(self, inclusion_number):
        self.Cc = (1-self.inclusions[inclusion_number].f_param)*self.matrix.Ckmln + self.inclusions[inclusion_number].f_param*self.inclusions[inclusion_number].Ckmln

              
                



