import re
import csv


class ReadData:
    def __init__(self, input_path, output_path):
        self._input_path = input_path
        self._output_path = output_path
        # self._index = 0
        self._f_write = None
        self._csv_write = None
        self._index = None
        self._current_line = None

    def read_field(self, field_type, can_be_null=False):
        if can_be_null and self._check_null():
            # skip null
            self._next_char(4)
            field_value = None
        else:
            if field_type == 'int':
                field_value = self.__read_int()
            elif field_type == 'float':
                field_value = self.__read_float()
            elif field_type == 'string':
                field_value = self.__read_string()
            else:
                raise ValueError("Do not support this field type")

        # skip next char
        self._next_char()
        return field_value

    def __read_int(self):
        cache_str = ''
        while self._get_current_char().isdigit() or self._get_current_char() == '-':
            cache_str += self._get_current_char()
            self._next_char()
        return int(cache_str)

    def __read_float(self):
        cache_str = ''
        while self._get_current_char().isdigit() or self._get_current_char() == '-' or self._get_current_char() == '.':
            cache_str += self._get_current_char()
            self._next_char()
        return float(cache_str)

    def __read_string(self):
        cache_str = ''
        # skip '
        self._next_char()
        while self._get_current_char() != "'":
            if self._get_current_char() == '\\':
                self._next_char()
            cache_str += self._get_current_char()
            self._next_char()
        # skip '
        self._next_char()
        return cache_str

    def _next_char(self, step=1):
        self._index += step

    def _get_current_char(self):
        return self._current_line[self._index]

    def _look_behind_char(self, step=1):
        return self._current_line[self._index - step] if self._index - step >= 0 else ''

    def _look_ahead_char(self, step=1):
        return self._current_line[self._index + step] if self._index + step < len(self._current_line) else ''

    def _check_null(self):
        return True if self._current_line[self._index:self._index + 4] == 'NULL' else False

    def _run(self):
        with open(self._input_path, mode='r', encoding='utf-8') as f_read:
            for index, line in enumerate(f_read):
                # index = 0
                # for line in f_read:
                match = re.search(r'^INSERT INTO `.*` VALUES (.*);', line)
                if match:
                    self._index = 0
                    self._current_line = match.group(1)
                    self._current_line = re.sub(r'\s', '', self._current_line)
                    # print(self._current_line)
                    self._extract_data()
                # os.system('cls')
                print(index)
                # index += 1

    def start(self):
        self._f_write = open(self._output_path, mode='w', encoding='utf-8', newline='')
        self._csv_write = csv.writer(self._f_write, delimiter=' ')
        self._run()
        self._f_write.close()

    def _write_2_file(self, *_value):
        self._csv_write.writerow(list(_value))

    def _extract_data(self):
        pass


class ReadPageLinksFile(ReadData):
    def __init__(self, input_path, output_path='./page-links-result.txt'):
        ReadData.__init__(self, input_path, output_path)

    def _extract_data(self):
        line_length = len(self._current_line)
        while self._index < line_length:
            # skip (
            self._next_char()

            pl_from = self.read_field('int')
            # print(pl_from)
            pl_namespace = self.read_field('int')
            # print(pl_namespace)
            pl_title = self.read_field('string')
            # print(pl_title)
            pl_from_namespace = self.read_field('int')
            # print(pl_from_namespace)
            # skip ,
            self._next_char()

            # print(pl_from, pl_namespace, pl_title, pl_from_namespace)
            if pl_namespace == 0 and pl_from_namespace == 0:
                self._write_2_file(pl_from, pl_title)


class ReadPageFile(ReadData):
    def __init__(self, input_path, output_path='./page-result.txt'):
        ReadData.__init__(self, input_path, output_path)

    def _extract_data(self):
        line_length = len(self._current_line)
        while self._index < line_length:
            # skip (
            self._next_char()
            page_id = self.read_field('int')
            page_namespace = self.read_field('int')
            page_title = self.read_field('string')
            page_restrictions = self.read_field('string')
            page_counter = self.read_field('int')
            page_is_redirect = self.read_field('int')
            page_is_new = self.read_field('int')
            page_random = self.read_field('float')
            page_touched = self.read_field('string')
            page_links_updated = self.read_field('string', can_be_null=True)
            page_latest = self.read_field('int')
            page_len = self.read_field('int')
            page_no_title_convert = self.read_field('int')
            page_content_model = self.read_field('string', can_be_null=True)
            page_lang = self.read_field('string', can_be_null=True)
            # skip ,
            self._next_char()

            if page_namespace == 0:
                self._write_2_file(page_id, page_title)


if __name__ == '__main__':
    page_links_reader = ReadPageLinksFile('./viwiki-20170901-pagelinks.sql')
    page_reader = ReadPageFile('./viwiki-20170901-page.sql')
    print("Start Page Reader")
    page_reader.start()
    print("Done Page Reader!")
    print("start Page links reader")
    page_links_reader.start()
    print("Done Page links reader!")
