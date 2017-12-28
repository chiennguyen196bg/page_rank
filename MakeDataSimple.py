import csv


class MakeDataSimple:
    def __init__(self, page_title_file='./page-title-result.txt', page_links_file='page-links-result.txt',
                 result_path='./simple-links.txt'):
        self.__page_title_file = page_title_file
        self.__page_links_file = page_links_file
        self.__result_path = result_path
        self.__page_id_dict = dict()
        self.__page_title_dict = dict()
        self.__simple_page_links_dict = dict()
        self.__last_index = 0

    def __map_page_file(self):
        with open(self.__page_title_file, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', dialect='excel')
            for index, row in enumerate(reader):
                page_id, page_title = row
                self.__page_id_dict[page_id] = index
                self.__page_title_dict[page_title] = index
                self.__last_index = index

    def __make_simple_page_link_dict(self):
        with open(self.__page_links_file, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', dialect='excel')
            for index, row in enumerate(reader):
                if index % 100000 == 0: print(index)

                pl_from_id, pl_to_title = row

                if pl_from_id not in self.__page_id_dict or pl_to_title not in self.__page_title_dict:
                    continue

                from_index = self.__page_id_dict[pl_from_id]
                to_index = self.__page_title_dict[pl_to_title]

                if from_index not in self.__simple_page_links_dict:
                    self.__simple_page_links_dict[from_index] = list([to_index])
                else:
                    self.__simple_page_links_dict[from_index].append(to_index)

    def __write_2_file(self):
        with open(self.__result_path, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            for key, value in self.__simple_page_links_dict.items():
                writer.writerow([key, *value])

    def start(self):
        print("start map page file")
        self.__map_page_file()
        print(self.__last_index)
        print("make simple page link dict")
        self.__make_simple_page_link_dict()
        print("write to file")
        self.__write_2_file()


if __name__ == "__main__":
    make_simple_page_links = MakeDataSimple()
    make_simple_page_links.start()
