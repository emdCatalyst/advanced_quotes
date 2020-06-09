from requests import get
from bs4 import BeautifulSoup
import re



def most_viewed():
    """

    Retrieve the most viewed topics.

    Returns:
        list<``Topic``>: The topics.

    Raises:
        Error: Resulting from requesting the website

    """
    try:
        endpoint = f'https://www.brainyquote.com/topics'
        body = get(endpoint).text
        parsed_body = BeautifulSoup(body, 'html.parser')
        data = []
        for a in parsed_body.select_one('body > div.container.bqTopLevel > div.row.bq_left').find_all('a'):
            data.append(Topic(re.sub('(/topics/|-quotes)','',a.get('href'))))
        return data
    except Exception as e:
        raise e

class Topic(object):

    def __init__(self, UUID:str):
        """
        Create a topic object wich allows access to quotes related to this topic.

        Args:
            UUID (str): A special formatted version of the topic name , all lowercase and special chars removed. Check the ``misc.toUUID()`` to convert a name to an UUID.
        """
        self.UUID = UUID

    def quotes(self, page:int=1):
        from quotes import Quote
        """
        Retrieve the quotes related to this topic.

        Returns:
            list<``quotes.Quote``>: The quotes related to this topic.

        Raises:
            ValueError: That UUID is probably wrong bud.
            TypeError: Invalid type or format of the page parameter.

        """
        try:
            if(not type(page) == int or page < 1):
                raise TypeError('Invalid type or format of the page parameter.')
            endpoint = f'https://www.brainyquote.com/topics/{self.UUID}-quotes_{page}'
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
