
# In future maybe read the columns dynamically. Currently it is very far
# fetched because: 1- It hasn't been chagned in a long time 2- Inside each
# column there maybe other dynamic changes that still need to be considered so
# even by dynamically reading the column names we still would need to manually
# change the parsing code anyways.

# The title_info is a dict with at most 4 keys:
# 1- Side Title 2- Title 3- Edition 4- ISBN
class SearchResult:
    def __init__(self, id_num,
                 md5,
                 title,
                 authors=None,
                 series=None,
                 edition=None,
                 isbn=None,
                 publisher=None,
                 year=None,
                 pages=None,
                 language=None,
                 size=None,
                 extension=None,
                 mirror_urls=None):
        self.id_num = id_num
        self.md5 = md5
        self.title = title
        self.authors = authors
        self.series = series
        self.edition = edition
        self.isbn = isbn
        self.publisher = publisher
        self.year = year
        self.pages = pages
        self.language = language
        self.size = size
        self.extension = extension
        self.mirror_urls = mirror_urls
        self.download_urls = []
        self.cover_image_urls = []

    def add_cover_image_url(self, cover_image_url):
        self.cover_image_urls.append(cover_image_url)

    def add_download_url(self, download_url):
        self.download_urls.append(download_url)

    def __str__(self):
        return f"""
                {self.id_num}
                {self.md5}
                {self.title}
                {self.authors}
                {self.series}
                {self.edition}
                {self.isbn}
                {self.publisher}
                {self.year}
                {self.pages}
                {self.language}
                {self.size}
                {self.extension}
                {self.mirror_urls}
              """


    def __eq__(self, other):
        return \
            self.id_num == other.id_num\
            and self.md5 == other.md5\
            and self.title == other.title\
            and self.authors == other.authors\
            and self.series == other.series\
            and self.edition == other.edition\
            and self.isbn == other.isbn\
            and self.publisher == other.publisher\
            and self.year == other.year\
            and self.pages == other.pages\
            and self.language == other.language\
            and self.size == other.size\
            and self.extension == other.extension\
            and self.mirror_urls == other.mirror_urls



