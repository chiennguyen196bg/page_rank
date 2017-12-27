import csv
import numpy as np


class PageRank:

    def __init__(self, page_links_file, n_page, n_thread=1, max_iterator=1000, epsilon=10 ^ -10, beta=0.85):
        self.__page_links_file = page_links_file
        self.__n_thread = n_thread
        self.__max_iterator = max_iterator
        self.__epsilon = epsilon
        self.__n_page = n_page
        self.__beta = beta
        self.__page_rank_vector = np.full((n_page,), 1 / n_page)
        self.__page_links_dict = dict()

    def __load_page_links_file(self):
        with open(self.__page_links_file, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for index, row in enumerate(reader):
                print(index)
                source_id = int(row[0])
                destination_ids = list(map(int, row[1:]))
                self.__page_links_dict[source_id] = destination_ids

    def __calc_page_rank(self, start, end):
        __new_page_rank_vector = np.full((self.__n_page,), (1 - self.__beta) / self.__n_page)
        for source_i in range(start, end):
            dest_id_list = self.__page_links_dict.get(source_i, None)
            if dest_id_list:
                __new_page_rank_vector[dest_id_list] += (
                        self.__beta * self.__page_rank_vector[source_i] / len(dest_id_list))
            else:
                __new_page_rank_vector += (self.__beta * self.__page_rank_vector[source_i] / self.__n_page)
        return __new_page_rank_vector

    def start(self):
        print("Start load page link file!")
        self.__load_page_links_file()
        print("Done load page link file!")
        iterator = 0
        while iterator < self.__max_iterator and np.linalg.norm:
            print(iterator)
            __new_page_rank_vector = self.__calc_page_rank()
            if np.linalg.norm(__new_page_rank_vector - self.__page_rank_vector) < self.__epsilon:
                break
            else:
                self.__page_rank_vector = __new_page_rank_vector
            iterator += 1
        print(self.__page_rank_vector)


if __name__ == '__main__':
    pr = PageRank('./simple-links.txt', n_page=1360035, max_iterator=100)
    pr.start()
