import csv


def load_page_title_file(path):
    page_title_list = list()
    with open(path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            page_id, page_title = row
            # print(page_title)
            page_title_list.append(page_title)
    return page_title_list


def load_page_rank_file(path):
    page_rank_list = list()
    with open(path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            value = float(row[0])
            page_rank_list.append(value)
    return page_rank_list


if __name__ == '__main__':
    page_title_list = load_page_title_file('./page-result.txt')
    page_rank_list = load_page_rank_file('./page-rank-result.txt')
    sorted_list = sorted(list(zip(page_rank_list, page_title_list)), key=lambda x: x[0], reverse=True)
    with open('./sorted-page-title-by-page-rank.txt', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        for page_rank, page_title in sorted_list:
            writer.writerow([page_rank, page_title])
