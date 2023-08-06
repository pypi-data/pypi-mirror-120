import os
import re
import requests


class ConnectionHandler():
    def get_raw_html(self, url):
        result = requests.get(url, allow_redirects=True).text
        return result

    def get_base_url(self, url):
        url = requests.get(url, allow_redirects=True).url
        result  = re.findall(r'^https?://[^/]+', url)[0]
        return result


    # This is based on content disposition header
    def get_file_name(self, res):
        disposition_header_str = res.headers['Content-Disposition']
        file_name = re.findall(r'".+"', disposition_header_str)[0].strip('"')
        return file_name

    # Returns a tuple of (<FileName>, <FileContentAsBytes>)
    def get_file(self, url):
        res = requests.get(url)
        file_name = self.get_file_name(res)
        file_content = res.content
        return file_name, file_content

    # Returns the full path to downloaded file
    def download_file_in_directory(self, url, dir_path):
        file_name, file_content = self.get_file(url)
        os.makedirs(dir_path, exist_ok=True)
        dl_file_path = os.path.join(dir_path, file_name)
        with open(dl_file_path, 'wb') as output:
            output.write(file_content)
            return dl_file_path
