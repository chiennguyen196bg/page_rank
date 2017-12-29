from ReadData import *
from MakeDataSimple import MakeDataSimple
from PageRank import PageRank
from SortedPageTitleByPageRank import *
import time

if __name__ == '__main__':
    start = time.time()
    page_links_reader = ReadPageLinksFile('./viwiki-20170901-pagelinks.sql')
    page_title_reader = ReadPageFile('./viwiki-20170901-page.sql')
    make_data_simple = MakeDataSimple()
    page_rank = PageRank(n_page=1360035, max_iterator=100, n_thread=6)

    print("-----Start Page Title Reader-----")
    t = time.time()
    page_title_reader.start()
    print(time.time() - t)

    print("-----Start Page Links Reader-----")
    t = time.time()
    page_links_reader.start()
    print(time.time() - t)

    print("-----Make Data Simple-----")
    t = time.time()
    make_data_simple.start()
    print(time.time() - t)

    print("-----Calculate Page Rank------")
    t = time.time()
    page_rank.start()
    print(time.time() - t)

    print("-----Sort page title by page rank------")
    t = time.time()
    write_sorted_page_title_by_page_rank()
    print(time.time() - t)

    print("Total time: {}".format(time.time() - start))
