def read_file(filename):
    file = open(filename).read().split('\n')
    if not file[-1]:
        file = file[:-1]

    return file