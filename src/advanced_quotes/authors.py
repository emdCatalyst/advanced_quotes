from requests import get
from bs4 import BeautifulSoup
import re

def index(letter:str='a', page:int=1):
    """

    Retrieve all the authors whom name starts with a given letter

    Args:
        letter (str, optional): The letter to filter by (case unsensitive), defaults to 'a'.
        page: (int, optional): Due to high number of authors, the authors are split in pages (typically 200 per page). Make sure the letter you're giving contains enough authors. Defaults to 1.

    Returns:
        list<``Author``>: The authors related to this letter

    Raises:
        TypeError: In case you gave a param of wrong type

    Examples:
        Viewing the first a author's snippet

        >>> print(all()['authors'][0].snippet())
        {'nationality': 'American', 'occupation': 'Musician', 'dates': {'birth': {'date': 'December 6', 'year': '1995'}, 'death': None}, 'related_authors': [<__main__.Athor object at 0x033898D0>, <__main__.Author object at 0x03389890>, <__main__.Author object at 0x03389D10>, <__main__.Author object at 0x03389D50>, <__main__.Author object at 0x03389D70>, <__main__.Author object at 0x03389DB0>, <__main__.Author object at 0x03389DD0>, <__main__.Author object at 0x03389DF0>]}

        Viewing all of 'a' letter authors

        >>> print(all()['authors'])
        {'authors': [<__main__.Author object at 0x03242CB0>...200], 'total_pages': 12, 'on_page': 200}
    """
    try:
        if(not type(page) == int):
            raise TypeError('The page must be a string')
        authors = f'https://www.brainyquote.com/authors/{letter.lower()}{str(page)}'
        body = get(authors).text
        parsed_body = BeautifulSoup(body, 'html.parser')
        data = {
            'authors': [],
            'total_pages': int(parsed_body.select_one('body > div.container.bqTopLevel > div > div.col-sm-8.col-md-8 > div:nth-child(4) > div > div > div > div > div > div > nav > ul').find_all('li')[len(parsed_body.select_one('body > div.container.bqTopLevel > div > div.col-sm-8.col-md-8 > div:nth-child(4) > div > div > div > div > div > div > nav > ul').find_all('li')) - 2].get_text()),
        }
        for tr in parsed_body.find('tbody').find_all('tr'):
            data['authors'].append(Author(tr.select_one('td:nth-child(1) > a').get('href').strip()))
        data['on_page'] = len(data['authors'])
        return data
    except Exception as e:
        raise e

def most_viewed(letter:str='a'):
    """

    Retrieve the most viewed authors of a given letter

    Args:
        letter (str, optional): The letter to filter by (case unsensitive), defaults to 'a'.

    Returns:
        list<``Author``>: The authors.

    Raises:
        TypeError: In case you gave a param of wrong type

    """
    try:
        endpoint = f'https://www.brainyquote.com/authors/{letter.lower()}'
        body = get(endpoint).text
        parsed_body = BeautifulSoup(body, 'html.parser')
        data = []
        for a in parsed_body.select('a.block-sm-az'):
            data.append(Author(re.sub('/authors/','',a.get('href'))))
        return data
    except Exception as e:
        raise e

class Author():
    def __init__(self, UUID:str):
        """
        Create an author object wich allows access to every piece of data available on the author including the name, a set of his quotes, biography and full on social info.

        Args:
            UUID (str): A special formatted version of the author's name , all lowercase and special chars removed. Check the ``misc.toUUID()`` to convert a name to an UUID
        """
        self.UUID = UUID

    def snippet(self):
        """
        Basic info about the author such as nationality, occupation, birth/death and related authors

        Returns:
            dict<`str`>: The dict that holds the info.

        Raises:
            ValueError: That UUID is probably wrong bud.

        Note:
            Includes instances of the ``Author`` class
        """
        try:
            endpoint = f'https://www.brainyquote.com/authors/{self.UUID}'
            body = get(endpoint).text
            parsed_body  = BeautifulSoup(body, 'html.parser')
            data = {
                'name': re.sub('Quotes', '',parsed_body.select_one('#bqNavBarCtrl > div > nav > div.navbar-header > h1').get_text()),
                'nationality': parsed_body.select_one('body > div.subnav-below-p > a:nth-child(1)').get_text(),
                'occupation': parsed_body.select_one('body > div.subnav-below-p > a:nth-child(2)').get_text(),
                'related_authors': []
            }
            for author in parsed_body.select_one('body > div.infScrollFooter > div.container-fluid > div > div.col-sm-7.col-md-8.block-style > div.bq_s > div').find_all('div'):
                data['related_authors'].append(Author(re.sub('Quotes', '', author.select_one('.link-name').get_text().strip())))
            return data
        except Exception as e:
            raise ValueError('That UUID is probably wrong bud.')

    def biography(self):
        """
        Retrieve the author's biography if available.

        Returns:
            str: The biography.

        Raises:
            ValueError: That UUID is wrong or the biography is not available.
        """
        try:
            endpoint = f'https://www.brainyquote.com/quotes/biography/{self.UUID}'
            body = get(endpoint).text
            parsed_body  = BeautifulSoup(body, 'html.parser')
            return parsed_body.select_one('div.bio-content').get_text().strip()
        except Exception as e:
            raise ValueError('That UUID is wrong or the biography is not available.')


    def quotes(self, page:int=1):
        """
        Retrieve the author's set of quotes, instances of the ``Quote`` class

        Args:
            page: (int, optional): Due to high number of quotes sometimes, they are split in pages. Make sure the author you've selected has enough pages. Defaults to 1.

        Returns:
            list<``quotes.Quote``>: The set of quotes.

        Raises:
            ValueError: That UUID is probably wrong bud.
            TypeError: Invalid type or format of the page parameter.

        Example:
            Retrieve the first page of abraham lincoln quotes

            >>> print(Author('abraham-lincoln').quotes())
            {'current_page': 1, 'total_pages': 9, 'elements': [<quotes.Quote object at 0x031A6C10>...165], 'on_page': 165}
        """
        from advanced_quotes.quotes import Quote
        try:
            if(not type(page) == int or page < 1):
                raise TypeError('Invalid type or format of the page parameter.')
            endpoint = f'https://www.brainyquote.com/authors/{self.UUID}-quotes_{page}'
            body = get(endpoint).text
            parsed_body  = BeautifulSoup(body, 'html.parser')
            data = {
                'current_page': page,
                'total_pages': int(parsed_body.select_one('body > div.infScrollFooter > div.bq_s.hideInfScroll.bq_pageNumbersCont > nav > ul').find_all('li')[len(parsed_body.select_one('body > div.infScrollFooter > div.bq_s.hideInfScroll.bq_pageNumbersCont > nav > ul').find_all('li')) - 2].get_text()),
                'elements': []
            }
            for quote in parsed_body.select_one('#quotesList').find_all('div'):
                try:
                    data['elements'].append(Quote(re.sub('/quotes/','',quote.select_one('div > div:nth-child(1) > div > a').get('href'))))
                except Exception as e:
                    continue
            data['on_page'] = len(data['elements'])
            return data
        except Exception as e:
            raise ValueError('That UUID is probably wrong bud.')
