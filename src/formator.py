def input_from_file(path):
    file_object = open(path, 'r')
    return file_object


def output_to_file(result):
    with open("poem_new.txt", "a") as file_object:
        file_object.write(result)


if __name__ == '__main__':
    poem_file = input_from_file("../poem.txt")
    for line in poem_file:
        print(line.strip().replace(" ", ""))
        output_to_file(line.strip().replace(" ", ""))
        output_to_file("\n")
    poem_file.close()
