from src import formator

def output_to_file(results):
    with open("../ready_2_db.txt", "a", encoding='UTF-8') as file_object:
        for item in results:
            file_object.write(item)
        file_object.write("\n")

if __name__ == '__main__':
    file = formator.input_from_file("../ready_2_db_v3.txt")
    for line in file:
        print(line.strip())
        output_to_file(line.strip())