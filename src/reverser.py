def input_from_file(path):
    file_object = open(path, 'r')
    return file_object

def output_to_file(result):
    with open("poem_new.txt", "a") as file_object:
        file_object.write(result)

if __name__ == '__main__':
    input_from_file()