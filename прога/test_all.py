import composite

a = composite.Composite("C:\\Users\\alexsey\\Desktop\\диплом\programm\\all_data_for_pytest\\martix_test.json",["C:\\Users\\alexsey\\Desktop\\диплом\programm\\all_data_for_pytest\\inclusion_test.json"])
print(a.matrix)
for i in range(len(a.inclusions)):
    print(a.inclusions[i])