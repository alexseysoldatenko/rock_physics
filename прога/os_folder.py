import os


for k in range(3):
    for m in range(3):
        for l in range(3):
            for n in range(3):

                path = f"test17.05.2022(1,1000,1000)\\k = {k}, m = {m}, l = {l}, n = {n}"


                os.mkdir(path)
                try:
                    os.mkdir(path)
                except OSError:
                    print ("Creation of the directory %s failed" % path)
                else:
                    print ("Successfully created the directory %s " % path)

