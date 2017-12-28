import csv
import numpy as np
import threading
import math


class PageRank:

    def __init__(self, n_page, n_thread=1, max_iterator=1000, epsilon=1e-9, beta=0.85, page_links_file='./simple-links.txt'):
        self.__page_links_file = page_links_file
        self.__n_thread = n_thread
        self.__max_iterator = max_iterator
        self.__epsilon = epsilon
        self.__n_page = n_page
        self.__beta = beta
        self.__page_rank_vector = np.full((n_page,), 1 / n_page)
        self.__page_links_dict = dict()
        self.__temp_result_list = [None] * n_thread

    def __load_page_links_file(self):
        with open(self.__page_links_file, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for index, row in enumerate(reader):
                print(index)
                source_id = int(row[0])
                destination_ids = list(map(int, row[1:]))
                self.__page_links_dict[source_id] = destination_ids

    def __calc_page_rank(self, start_index=0):
        __new_page_rank_vector = np.zeros((self.__n_page,), dtype=np.double)
        for source_i in range(start_index, self.__n_page, self.__n_thread):
            dest_id_list = self.__page_links_dict.get(source_i, None)
            if dest_id_list:
                __new_page_rank_vector[dest_id_list] += (
                        self.__beta * self.__page_rank_vector[source_i] / len(dest_id_list))
            else:
                __new_page_rank_vector += (self.__beta * self.__page_rank_vector[source_i] / self.__n_page)
        self.__temp_result_list[start_index] = __new_page_rank_vector

    def __write_to_file(self):
        with open('./page-rank-result.txt', mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=' ')
            for value in self.__page_rank_vector:
                writer.writerow([math.log(value)])

    def start(self):
        print("Start load page link file!")
        self.__load_page_links_file()
        print("Done load page link file!")
        iterator = 0
        while iterator < self.__max_iterator and np.linalg.norm:
            print(iterator)
            threads = [None] * 10
            for i in range(self.__n_thread):
                threads[i] = threading.Thread(target=self.__calc_page_rank, args=(i,))
                threads[i].start()
            for i in range(self.__n_thread):
                threads[i].join()

            __new_page_rank_vector = np.zeros((self.__n_page,), dtype=np.double)
            for i in range(self.__n_thread):
                __new_page_rank_vector += self.__temp_result_list[i]
                self.__temp_result_list[i] = None
            __new_page_rank_vector += (1 - self.__beta) / self.__n_page

            epsilon = np.linalg.norm(__new_page_rank_vector - self.__page_rank_vector)
            print(epsilon)
            if epsilon < self.__epsilon:
                break
            else:
                self.__page_rank_vector = __new_page_rank_vector
            iterator += 1
        print(self.__page_rank_vector)
        self.__write_to_file()


if __name__ == '__main__':
    pr = PageRank(n_page=1360035, max_iterator=100, n_thread=6)
    pr.start()
