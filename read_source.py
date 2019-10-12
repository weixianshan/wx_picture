def read_file(path):

    source = []
    f = open(path)
    for line in f:
        if line.startswith("#"):
            continue
        url, save_path = line.split()
        source.append((url, save_path))

    return source


if __name__ == "__main__":
    p = "./source_url.txt"
    result = read_file(p)
    print("result : ", result)
