import os


def list_dir(base_path):
    res = []
    for path in os.listdir(base_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(base_path, path)):
            res.append(path)
    return res
 
