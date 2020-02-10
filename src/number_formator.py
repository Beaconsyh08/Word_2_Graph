from src import formator


def output_to_file(results):
    with open("../ready_2_db_v33.txt", "a", encoding="UTF-8") as file_object:
        for item in results:
            file_object.write(item)
        file_object.write("\n")


if __name__ == '__main__':
    url_file = formator.input_from_file("../ready_2_db_v3.txt")
    count = 120570
    for line in url_file:
        # if count == 120570:
        #     count += 1
        #     output_to_file(line.strip())
        #     continue
        # else:
            infos = (str(line).strip()).split("\t")
            # print(infos[0])
            number = "\"" + str(count) + "\""
            print(number)
            infos[0] = number
            res = "\t".join(infos)
            # print(res)
            output_to_file(res)
            count += 1
