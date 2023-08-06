import re
import bs4
import requests



#TODO: Take care of 'open' parameter in urls

# This is an abstract base class for all parsed download mirror pages. 
class ParsedDownloadMirrorPage:
    def __init__(self, raw_html_page:str):
        self.page = bs4.BeautifulSoup(raw_html_page, 'html.parser')

    def get_download_links(self):
        pass

    def get_cover_image_url(self):
        pass


class LibraryLolParsedDownloadMirrorPage(ParsedDownloadMirrorPage):
    def __init__(self, raw_html_page:str, base_url:str):
        super().__init__(raw_html_page)
        self.base_url=base_url

    def get_download_links(self):
        download_urls = []
        first_anchor = self.page.find_all('a')[0]
        main_download_url = first_anchor['href']
        download_urls.append(main_download_url)

        secondary_download_urls = []
        unordered_list = self.page.find('ul')
        for list_item in unordered_list.find_all('li'):
            secondary_download_urls.append(list_item.a['href'])

        download_urls.extend(secondary_download_urls)

        return download_urls

    # Images don't need '/' to be appended to since they start with one
    def get_cover_image_url(self):
        image_cover = self.page.find('img')
        if image_cover:
            return f"{self.base_url}{image_cover['src']}"


class LibgenLcParsedDownloadMirrorPage(ParsedDownloadMirrorPage):
    def __init__(self, raw_html_page:str, base_url:str):
        super().__init__(raw_html_page)
        self.base_url=base_url

    def get_download_urls(self):
        first_anchor = self.page.find_all('a')[0]
        download_url_with_key =\
            f"{self.base_url}/{first_anchor['href']}"

        # The download url includes a key parameter that needs to be taken away
        # in order for it to be permanent url
        # download_url =\
        #     re.sub(r'&key=[^&]+','',download_url_with_key)

        download_url = download_url_with_key

        return [download_url]

    # Images don't need '/' to be appended to since they start with one
    def get_cover_image_url(self):
        image_cover = self.page.find('img')
        if image_cover:
            return f"{self.base_url}{image_cover['src']}"


# This doesn't work properly due to website dynamoically changing the download
# link. For more info refer to test file.
class ThreeLibNetParsedDownloadMirrorPage(ParsedDownloadMirrorPage):
    def __init__(self, raw_html_page:str):
        super().__init__(raw_html_page)
        self.base_url = 'https://3lib.net'

    # This download mirror differs from the libgen and library lol one in that
    # it hosts the info about the book inside another link inside the page. Here
    # we need to get this inner url and then parse that one for download and
    # image cover urls.
    def get_inner_page_url(self):
        first_result_anchor = self.page.find('h3').a
        inner_url =\
            f"{self.base_url}{first_result_anchor['href']}"
        return inner_url

    def get_download_links(self):
        inner_url = self.get_inner_page_url()
        print(f"Inner Url: {inner_url}")
        inner_page_raw_html = requests.get(inner_url).text
        inner_page = bs4.BeautifulSoup(inner_page_raw_html, 'html.parser')

        # First Method: Using div to find anchor
        book_details_button_div = inner_page\
            .find('div', attrs={'class': 'book-details-button'})

        book_details_anchor = book_details_button_div.find('a')
        book_details_anchor = inner_page\
            .find('a', attrs={'class': 'dlButton'})

        # Second Method: Using book button to find its sibling the ul list then
        # its first item which has anchor.
        # book_button = inner_page\
        #     .find('button', attrs={'id': 'btnCheckOtherFormats'})
        # book_details_ul = book_button.next_sibling.next_sibling
        # print(f"UL Details: {book_details_ul.attrs}")
        # book_details_anchor = book_details_ul.find_all('li')[0].a
        # print(f"Anchor attrs:\n {book_details_anchor.attrs}")

        if self.is_download_link_disabled(book_details_anchor):
            return []
        else:
            download_link =\
                f"{self.base_url}{book_details_anchor['href']}"
            print(f"Download_Link: {download_link}")
            return [download_link]

    def is_download_link_disabled(self, book_details_anchor):
        anchor_class = book_details_anchor['class']
        disabled = 'disabled' in anchor_class
        return disabled



