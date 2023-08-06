from enum import Enum

class DownloadType(Enum):
    RESUMED_DL_WITH_ORIGINAL_FILENAME = 0
    RESUMED_DL_WITH_TRANSIT_FILENAME = 1
    RESUMED_DL_WITH_MD5_FILENAME = 2
    OPEN_FILE_IN_BROWSER = 3


class ResultPerPage(Enum):
    TwentyFive = 25
    Fifty = 50
    Hundered = 100


class ViewType(Enum):
    Simple = 'simple'
    Detailed = 'detailed'


class SearchField(Enum):
    Default = 'def'
    Title = 'title'
    Author = 'author'
    Series = 'series'
    Publisher = 'publisher'
    Year = 'year'
    ISBN = 'identifier'
    Language = 'language'
    MD5 = 'md5'
    Tags = 'tags'
    Extension = 'extension'


class SearchPhrasing(Enum):
    WITH_MASK = 0
    WITHOUT_MASK = 1
