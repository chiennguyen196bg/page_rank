from ReadData import *
from MakeDataSimple import MakeDataSimple
from PageRank import PageRank
from SortedPageTitleByPageRank import *
import time

if __name__ == '__main__':
    start = time.time()
    page_links_reader = ReadPageLinksFile('./viwiki-20170901-pagelinks.sql')
    page_title_reader = ReadPageTitleFile('./viwiki-20170901-page.sql')
    make_data_simple = MakeDataSimple()

    print("-----Start Page Title Reader-----")
    page_title_reader.start()
    n_page = page_title_reader.get_total_field()

    print("-----Start Page Links Reader-----")
    page_links_reader.start()

    print("-----Make Data Simple-----")
    make_data_simple.start()

    print("-----Calculate Page Rank------")
    page_rank = PageRank(n_page=n_page, max_iterator=100, n_thread=6)
    page_rank.start()

    print("-----Sort page title by page rank------")
    write_sorted_page_title_by_page_rank()

    print("n_page {}".format(n_page))
    print("Total time: {}".format(time.time() - start))
