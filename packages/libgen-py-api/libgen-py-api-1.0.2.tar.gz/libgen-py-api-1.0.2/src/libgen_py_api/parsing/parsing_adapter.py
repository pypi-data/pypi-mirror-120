from ..results import SearchResult
from ..parsing.parsing import SEARCH_RESULTS_COLUMNS, TITLE_COLUMN_EMPTY_DICT

class SearchResultDictAdapter:

    # TODO: Add this to SearchResult as well
    REQUIRED_VALUES_KEYS = 'id_num', 'md5', 'title'

    def check_formatting(self, search_result_dict):
        # First check overall keys
        format_key_set = set(SEARCH_RESULTS_COLUMNS.values())
        current_key_set = set(search_result_dict.keys())
        if format_key_set.symmetric_difference(current_key_set):
            exception_error=\
               f"Keys are not according to format:\n{format_key_set}\n{current_key_set}"
            raise(Exception(exception_error))

        title_format_key_set = set(TITLE_COLUMN_EMPTY_DICT.keys())
        current_title_key_set = set(search_result_dict['title'].keys())
        if title_format_key_set.symmetric_difference(current_title_key_set):
            exception_error=\
               f"Keys are not according to format:\n{format_key_set}\n{current_key_set}"
            raise(Exception(exception_error))


    # Title column in search result dict is itself a dict that houses important
    # info about the dictionary which only because of design of website are
    # combined under a single column called title.
    def flatten_title_column(self, search_result_dict):
        # first we need to change the 'title' key to something else since title
        # itself is one of the children keys. Here we call it 'info'
        search_result_dict['info'] = search_result_dict['title']

        for key, value in search_result_dict['info'].items():
            search_result_dict[key] = value

        search_result_dict.pop('info')
        return search_result_dict

    # Note that this should be called after dictionary is flattened
    def check_if_required_keys_are_not_empty(self, search_result_dict):
        for key in SearchResultDictAdapter.REQUIRED_VALUES_KEYS:
            if len(search_result_dict[key]) == 0:
                raise Exception(f"Required Value Is Empty: {key}")


    def convert(self, search_result_dict) -> SearchResult:
        self.check_formatting(search_result_dict)
        search_result_dict = self.flatten_title_column(search_result_dict)
        self.check_if_required_keys_are_not_empty(search_result_dict)
        return self._convert_to_result(search_result_dict)

    # This doesn't check for formatting of the dict or required values being
    # ready
    def _convert_to_result(self, search_result_dict) -> SearchResult:

        mirror_urls = []
        mirror_keys = 'mirror1', 'mirror2', 'mirror3', 'mirror4', 'mirror5'
        for key in mirror_keys:
            mirror_dict = search_result_dict[key]
            if mirror_dict['enabled']:
                mirror_urls.append(mirror_dict['link'])

        converted_result =\
            SearchResult(id_num=search_result_dict['id_num'],
                         extension=search_result_dict['extension'],
                         authors=search_result_dict['authors'],
                         language=search_result_dict['language'],
                         pages=search_result_dict['pages'],
                         publisher=search_result_dict['publisher'],
                         size=search_result_dict['size'],
                         title=search_result_dict['title'],
                         isbn=search_result_dict['isbn'],
                         md5=search_result_dict['md5'],
                         series=search_result_dict['series'],
                         edition=search_result_dict['edition'],
                         year=search_result_dict['year'],
                         mirror_urls=mirror_urls
                         )
        return converted_result
