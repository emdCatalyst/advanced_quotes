from requests import get
from bs4 import BeautifulSoup
import re
from datetime import datetime as dt


def random():
    """
    Generate a random quote.

    Returns:
        Quote: The random qoute.

    """
    from topics import most_viewed
    from random import choice
    random_topic = choice(most_viewed())
    random_quote = choice(random_topic.quotes()['elements'])
    return random_quote
def top_30():
    """
    Top 30 quotes of all time, based on user selections.

    Returns:
        dict<`int`:``Quote``>: A dict holding position and the quote as an instance of a ``Quote`` class.

    Raises:
        Error: Resulting from requesting the website
    """
    try:
        endpoint = 'https://www.brainyquote.com/top_100_quotes'
        body = get(endpoint).text
        parsed_body = BeautifulSoup(body, 'html.parser')
        data = {}
        i = 1
        for position in parsed_body.select('.listPositionNum'):
            if(i == 31):
                break
            data[i] = Quote(re.sub('/quotes/','',position.parent.find('a').get('href')))
            i = i+1

        for light_position in parsed_body.select('.listPositionNumLight'):
            if(i == 31):
                break
            data[i] = Quote(re.sub('/quotes/','',light_position.parent.find('a').get('href')))
            i = i+1
        return data
    except Exception as e:
        raise e


def todays_pick():
    """
    Todays quote, updates every 24 hours.

    Returns:
        dict<`str`:```Quote``|`str`>: A dict holding the date and the quote as an instance of a ``Quote`` class.

    Raises:
        Error: Resulting from requesting the website

    Example:

        The pick of Moday, June 08 th, 2020
        >>> print(quotes.todays_pick()['quote'].snippet()['body'])
        The backbone of surprise is fusing speed with secrecy.
    """
    try:
        endpoint = 'https://www.brainyquote.com/quote_of_the_day'
        body = get(endpoint).text
        parsed_body = BeautifulSoup(body, 'html.parser')
        return {
            'date': dt.now(),
            'quote': Quote(re.sub('/quotes/','',parsed_body.select_one('body > div.qotd_days.m_panel > div:nth-child(4) > div > div > div > div:nth-child(2) > div > a').get('href')))
        }
    except Exception as e:
        raise e
class Quote():

    def __init__(self, UUID:str):
        """
        Create a quote object wich allows access to every piece of data available on the quote including the body (both text and image if available), author and related topics/authors/quotes.

        Args:
            UUID (str): A special formatted version of the name including a special id to suit the scraping system.
        """
        self.UUID = UUID

    def snippet(self):
        """
            Retrieve the quote's body and author.

            Returns:
                dict<`str`>: The dict that holds the info.

            Raises:
                ValueError: That UUID is probably wrong bud.

            Note:
                Includes instances of the ``Author`` class
        """
        from authors import Author
        try:
            endpoint = f'https://www.brainyquote.com/quotes/{self.UUID}'
            body = get(endpoint).text
            parsed_body = BeautifulSoup(body, 'html.parser')
            return {
                'body': parsed_body.select_one('#quotePageTopHolder > div > div > div.col-sm-7.col-md-8 > div > div > div > div > div.quoteContent > div > p').get_text(),
                'author': Author(re.sub('(/authors/|-quotes)','',parsed_body.select_one('#quotePageTopHolder > div > div > div.col-sm-7.col-md-8 > div > div > div > div > div.quoteContent > div > p.bq_fq_a > a').get('href')))
            }
        except Exception as e:
            raise ValueError('It seems like that UUID is invalid bud.')
    def image_content(self, background_id:int=1):
        """
            Retrieve the quote's image version if available, the background is customizable.

            Args:
                background_id (int, optional): The background id, defaults to 1.

            Returns:
                str: The image url.
                None: The image version is not available for this quote.

            Raises:
                ValueError: That UUID is probably wrong bud.

        """
        try:
            endpoint = f'https://www.brainyquote.com/quotes/{self.UUID}?img={background_id}'
            body = get(endpoint).text
            parsed_body = BeautifulSoup(body, 'html.parser')
            return  'https://www.brainyquote.com{}'.format(parsed_body.select_one('div.quoteContent > div > a > img').get('data-img-url')) if parsed_body.select_one('div.quoteContent > div > a > img') else None
        except Exception as e:
            raise ValueError('It seems like that UUID / background id is invalid  bud.')

    def related_quotes(self):
        """
        Retrieve related quotes as instances of the ``Quote`` class.

        Returns:
            list<``Quote``>: The list of the related quotes.

        Raises:
            ValueError: It seems like that UUID is invalid bud.
        """
        from quotes import Quote
        try:
            endpoint = f'https://www.brainyquote.com/quotes/{self.UUID}'
            body = get(endpoint).text
            parsed_body = BeautifulSoup(body, 'html.parser')
            data = []
            for quote in parsed_body.select_one('#quotesList').find_all('div'):
                try:
                    data.append(Quote(re.sub('/quotes/','',quote.select_one('div > div:nth-child(1) > div > a').get('href'))))
                except Exception as e:
                    continue
            return data
        except Exception as e:
            raise ValueError('It seems like that UUID is invalid bud.')
