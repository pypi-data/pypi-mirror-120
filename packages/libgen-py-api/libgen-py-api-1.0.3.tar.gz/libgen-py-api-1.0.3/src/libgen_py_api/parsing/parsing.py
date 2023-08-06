import re
import bs4
from ..results import SearchResult
from ..query import SearchQuery
from ..utils.common_types \
    import DownloadType, ResultPerPage, ViewType, SearchField, SearchPhrasing


SEARCH_RESULTS_COLUMNS = {
    1: 'id_num',
    2: 'authors',
    3: 'title',
    4: 'publisher',
    5: 'year',
    6: 'pages',
    7: 'language',
    8: 'size',
    9: 'extension',
    10: 'mirror1',
    11: 'mirror2',
    12: 'mirror3',
    13: 'mirror4',
    14: 'mirror5'
}

TITLE_COLUMN_EMPTY_DICT = {
    'edition': '',
    'isbn': '',
    'md5': '',
    'series': '',
    'title': ''
}

# The search result dict would be something like this:
# {'authors': ['Martin', ' Robert'],
# 'extension': 'epub',
# 'id_num': '2659591',
# 'language': 'English',
# 'mirror1': {'enabled': True,
#             'link': 'http://library.lol/main/F9D7691737352F4BE37FD46060A3669A&open=2'},
# 'mirror2': {'enabled': True,
#             'link': 'http://libgen.lc/ads.php?md5=F9D7691737352F4BE37FD46060A3669A&open=2'},
# 'mirror3': {'enabled': True,
#             'link': 'https://3lib.net/md5/F9D7691737352F4BE37FD46060A3669A'},
# 'mirror4': {'enabled': False, 'link': 'https://libgen.pw/item?id=2659591'},
# 'mirror5': {'enabled': False,
#             'link': 'http://bookfi.net/md5/F9D7691737352F4BE37FD46060A3669A'},
# 'pages': '432 pages',
# 'publisher': 'Pearson Education;Prentice Hall',
# 'size': '6 Mb',
# 'title': {'edition': '1st edition',
#           'isbn': '9780134494166, 0134494164, 9780134494326',
#           'md5': 'F9D7691737352F4BE37FD46060A3669A',
#           'series': 'Robert C. Martin',
#           'title': "Clean Architecture A Craftsman's Guide to Software "
#                    'Structure and Design-Pearson Education '},
# 'year': '2018;2017'}


class ParsedResultsPage():
    def __init__(self, raw_html_page: str):
        self.page = bs4.BeautifulSoup(raw_html_page, 'html.parser')
        # self.view_type = ParsedPage.get_view_type(self.page)

    def get_main_query(self):
        return self.page.find(id="searchform")['value']

    def get_search_field(self):
        search_field = self.page\
            .find_all('input', attrs={"checked": True, "name": "column"})[0]['value']
        return SearchField(search_field)

    def get_view_type(self):
        view_type = self.page\
            .find('input', attrs={"checked": True, "name": "view"})['value']
        return ViewType(view_type)

    def get_search_phrasing(self):
        raw_phrasing = self.page\
            .find('input', attrs={"checked": True, "name": "phrase"})['value']
        # Phrasing needs to be inverted since the question in page is asked
        # in the other way
        phrasing = 0 if raw_phrasing == '1' else 1
        return SearchPhrasing(phrasing)

    def get_dl_type(self):
        dl_type_selector = self.page\
            .find('select', attrs={"name": "open"})
        raw_dl_type = dl_type_selector\
            .find('option', attrs={"selected": "selected"})['value']
        return DownloadType(int(raw_dl_type))

    def get_res_number(self):
        res_number_selector = self.page\
            .find('select', attrs={"name": 'res'})
        raw_res_number = res_number_selector\
            .find('option', attrs={'selected': 'selected'})['value']
        return ResultPerPage(int(raw_res_number))

    def get_search_query(self):
        return SearchQuery(
            self.get_main_query(), self.get_dl_type(), self.get_res_number(),
            self.get_view_type(), self.get_search_phrasing(),
            self.get_search_field())

    # Search result dict is a dictionary in which keys are column names and
    # their value is a string, list or dict that is parsed from content of that
    # specific cell positioned in the specified column of the row.
    # Minimal conversion is done on the cell input so that the data remains raw
    # as much as possible. This is to ensure conversion to other formats (e.g.
    # SearchResult object, ...) can be done simply with an adapter.
    def get_results_as_list_of_search_result_dicts(self):
        search_results = []
        table = self.page\
            .find('table', attrs={"class": "c"})
        if table:
            results_table = table.find_all('tr')[1:]

            for result_row in results_table:
                search_results.append(
                    self.convert_result_row_to_dict(result_row))

            return search_results
        else:
            return []

    def convert_result_row_to_dict(self, result_row):
        view_type = self.get_view_type()
        if view_type == ViewType.Simple:
            return\
                self.convert_result_row_to_dict_simple_view(result_row)
        # elif view_type == ViewType.Detailed:
        #     return\
        #         self.convert_result_row_to_dict_detailed_view(result_row)
        else:
            raise Exception('View type not supported')

    def convert_result_row_to_dict_simple_view(self, result_row):
        search_result_dict = {}
        for index, column in enumerate(result_row.find_all('td'), start=1):
            # The 15th column is for editing the results which we don't need
            if index == 15:
                break
            key = SEARCH_RESULTS_COLUMNS[index]
            if index == 2:
                value = self.parse_authors_column(column)
            elif index == 3:
                value = self.parse_title_column(column)
            elif index == 6:
                value = self.parse_pages_column(column)
            elif index >= 10:
                value = self.parse_mirror_columns(column)
            else:
                value = self.parse_other_columns(column)
            search_result_dict[key] = value

        return search_result_dict

    def parse_other_columns(self, column):
        value = column.string
        return value

    # For mirrors we save the mirror link instead of its name
    def parse_mirror_columns(self, column):
        # print(column.a.attrs)
        is_enabled = False if 'style' in column.a.attrs else True
        # print(is_enabled)
        value = {
            'link': column.a['href'],
            'enabled': is_enabled
        }
        return value

    # For pages column, we use the first part of column contents since
    # the other parts are extra info (if available) we don't need

    def parse_pages_column(self, column):
        # If there are no pages the contents would be empty, In that case we
        # need to return an empty string
        if column.contents:
            value = column.contents[0]
        else:
            value = ''
        return value

    def parse_authors_column(self, column):
        value = []
        for anchor in column.find_all('a'):
            value.append(anchor.string)
        return value

    def parse_title_column(self, column):
        value = self.instantiate_title_block_dict()
        anchors = column.find_all('a')
        if len(anchors) == 2:
            # It has series
            value['series'] = anchors[0].font.i.string
            value = self.parse_title_block(anchors[1], value)
        elif len(anchors) == 1:
            # It doesn't have series
            value = self.parse_title_block(anchors[0], value)
        else:
            raise Exception('Title column parsing error')
        return value

    # TODO: Get MD5 From Href
    def parse_title_block(self, column_block, value):
        value['title'] = list(column_block.strings)[0]
        value['md5'] =\
            re.search(r'(?<=md5=)[^&]+', column_block['href']).group(0)
        # It has ISBN, this means it is guranteed to have a font tag after it
        # but may or may not have a font tag (showing edition) before it.
        if br := column_block.find('br'):
            if br.next_sibling and br.next_sibling.next_sibling:
                isbn = br.next_sibling.next_sibling.string
                value['isbn'] = isbn
                if edition := br.previous_sibling:
                    # We need to remove the brackets around edition string
                    value['edition'] = edition.string.strip('[]')

        # It doesn't have ISBN, we need to check whether it has a font tag for
        # edition or it doesn't even have that.
        else:
            if edition := column_block.find('font'):
                value['edition'] = edition.i.string

        # Fix edition text not being unicode for some reason
        value['edition'] = value['edition'].replace('\xa0', ' ')
        # Means it has isbn
        return value

    def instantiate_title_block_dict(self):
        return TITLE_COLUMN_EMPTY_DICT.copy()


def get_thumbnail_urls_from_detailed_results_page(raw_html_page, base_url):
    page = bs4.BeautifulSoup(raw_html_page, 'html.parser')
    rows = page.find_all('table', attrs={'rules': 'cols', 'border': '0'})
    img_elements = []
    for row in rows:
        # This is to weed out zero height tables which are used as borders 
        if row.find_all('img'):
            img_elements.append(row.find_all('img')[0])

    # return img_elements

    thumbnail_urls = list(map(lambda img: f"{base_url}{img['src']}",
                              img_elements))
    return thumbnail_urls



