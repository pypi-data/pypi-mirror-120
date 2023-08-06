from pandas import DataFrame
from requests_testadapter import Resp
from collections import Counter
from bs4 import BeautifulSoup
import re
import requests
import os


class WebPageAnalyticTool:
    """
        A class used to analyse a webpage Html Tags
        
    """

    def __init__(self, url: str = 'www.google.com') -> None:
        self.__url = self.__formaturl(url)
        self.__content = None
        self.__headers = {
                            'upgrade-insecure-requests': '1',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
                            'accept': 't	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'sec-fetch-site': 'cross-site',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-user': '?1',
                            'sec-fetch-dest': 'document',
                            'referer': 'https://www.google.com/',
                            'accept-language': 'en-US,en;q=0.9',
                            }

        self.__validate_input(self.__url)
        self.__validate_webpage_exist(self.__url, self.__headers)


    @staticmethod
    def __validate_input(url: str) -> None:

        """
            Check if the url passed is a valid string

            Parameters
            ----------
                url: string
                    The url of the webpage

            returns
            --------
                bool

        """

        if not isinstance(url, str):
            raise TypeError('accepted type is string for url')


    def __validate_webpage_exist(self, url:str, headers) -> tuple:
        """
            Checks if the supplied url is valid and returns a response
        """
        if not re.match('(?:http|ftp|https|file)://', url):
            content = requests.get(url, headers=headers)
            if content.status_code != 200:
                raise ValueError(f"supplied {url} returned status code {content.status_code}")
            else:
                self.__content = content.content
        else:
            requests_session = requests.session()
            requests_session.mount('file://', LocalFileAdapter())
            r = requests_session.get(url)
            
            self.__content = r.content

    def __formaturl(self,url):
        """
            formatting the url to the appropriate syntax for requests
        """
        if not re.match('(?:http|ftp|https|file)://', url):
            return 'http://{}'.format(url)
        return url

    @property
    def url(self) -> str:
        '''
            returns the url
        '''
        return self.__url

    @property
    def header(self) -> str:
        '''
            returns the header for the url
        '''
        return self.__headers

    @header.setter
    def header(self, header_info:str) -> None:
        '''
            sets the header property
        '''
        self.__headers = header_info

    @property
    def get_content(self):
        '''
            returns the scraped page content
        '''
        return self.__content


    def __get_all_tags(self):
        """
            Returns all tags in a document
        """
        soup_content = BeautifulSoup(self.__content, "html.parser")
        return [tag.name for tag in soup_content.find_all()]

    @property
    def get_all_tags(self):
        """
            Returns all tags
        """
        return self.__get_all_tags()

    
    def __get_unique_tags(self):
        """
            returns all unique tags in a document
        """
        return set(self.__get_all_tags())

    @property
    def get_unique_tags(self) -> set:
        """
            returns all unique tags in a document
        """
        return self.__get_unique_tags()

    def __get_most_common_tag(self):
        """
            returns most common tag
        """
        return sorted(Counter(self.__get_all_tags()).most_common(1))[0][0]

    @property
    def get_most_common_tags(self) -> str:
        """
            returns most common tag
        """
        return self.__get_most_common_tag()

    def __get_root_tags(self) -> list:
        """
            Returns the root node tags
        """
        soup_content = BeautifulSoup(self.__content, "html.parser")
        tags = [tag for tag in soup_content.find_all()]
        element_count = [len(list(a.parents)) for a in tags]

        root_index = min((index for index, element in enumerate(element_count)    
                                    if element == max(element_count)))
        return tags[root_index:]

    def __get_node_paths(self, root) -> str:
        """
            returns nodes path
        """
        path = [root.name] + [tags.name for tags in root.parents if  tags.name not in ['[document]']]
        return ' > '.join(path[::-1])

    def __create_insight_df(self) -> DataFrame:
        """
            Creates a DataFrame that contains nodes information
        """
        roots = self.__get_root_tags()
        tag_nodes = [self.__get_node_paths(root) for root in roots]
        df = DataFrame(tag_nodes, columns=['root_link'])
        df['length'] = df['root_link'].str.split('>').str.len()
        df['count'] = df['root_link'].str.findall(self.get_most_common_tags).str.len()

        return df

    def __get_longest_path(self) -> str:
        """
            returns longest node path
        """
        df = self.__create_insight_df()
        return df.sort_values(by=['length', 'root_link'], ascending=False)['root_link'].values[0]

    @property
    def get_longest_path(self) -> str:
        """
            returns longest node path
        """
        return self.__get_longest_path()

    def __get_longest_path_with_most_common_tag(self) -> str:
        """
            returns longest node path with the most common tag
        """
        df = self.__create_insight_df()
        return df.sort_values(by=['count','root_link'], ascending=False)['root_link'].values[0]

    @property
    def get_longest_path_with_most_common_tag(self) -> str:
        """
            returns longest node path with the most common tag
        """
        return self.__get_longest_path_with_most_common_tag()


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    """
        Helper class to read local files
    """
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            response_ret = self.build_response(request, resp)

            return response_ret

    def send(self, request, stream=False, timeout=None,verify=True, cert=None, proxies=None):
        return self.build_response_from_file(request)