from src import formator


def output_to_file(results):
    with open("../ready_2_db_v3.txt", "a", encoding="UTF-8") as file_object:
        for item in results:
            file_object.write(item)
        file_object.write("\n")


if __name__ == '__main__':
    url_file = formator.input_from_file("../poem_img_url_3.txt")
    count = 0
    temp = []
    for line in url_file:
        infos = (str(line).strip()).split("@")
        if count % 2 != 0:
            del infos[0]
            number = int((count + 1) / 2)
            temp.append(infos[0])
            temp.append("")
            temp.append(str(number))
            res = "\"" + "\"\t\"".join(temp) + "\""
            print(res)
            output_to_file(res)
            temp = []
        else:
            number = int((count / 2) + 1)
            temp = [str(number), infos[0], infos[1]]
        count += 1
