
__all__ = [
    "BaseExtractor",
    "MdpiExtractor",
    "PMCExtractor",
    "NihExtractor",
    "ScienceDirectExtractor",
    "SpringerExtractor",
    "ApsNetExtractor",
    "WileyExtractor",
    "DailyGroupExtractor",
    "FreshFruitPortalExtractor",
    "HuffingtonExtractor",
]

import re
from requests import get
from requests.compat import urljoin
from requests.exceptions import InvalidURL
from requests.utils import default_headers, urlparse
from bs4 import BeautifulSoup as B
from tldextract import extract
from html import unescape
from json import loads
from pprint import pprint as cat, pformat as pcat
from datetime import datetime


from rollet import settings
from rollet.rollet import get_content
from rollet.utils import (
    rfinditem
)


class BaseExtractor:
    def __init__(self, url, **kwargs):
        """
        Create BaseExtractor instance
        url: string
        timeout: float, request timeout. Default 1 sec.
        rebond: bool, request <a> tag. Default False.
        abstract_**kwargs: **kwargs for abstract fetch
        title_**kwargs: **kwargs for title fetch
        """
        
        self.url = self._clean_url(url)
        self.domain = extract(url).domain
        self.rebond = bool(kwargs.get('rebond', False))
        self.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self._scrap(**kwargs)
        self._init_kwargs(**kwargs)
    
    
    @staticmethod
    def _clean_url(url):
        return url
    
    def _scrap(self, **kwargs):
        timeout = kwargs.pop('timeout', 1)
        headers = default_headers()
        headers.update({
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        headers = kwargs.pop('headers', headers)

        with get(self.url, timeout = timeout, headers = headers) as response:
            self._status = response.status_code
            self._header = response.headers
            self._content_type()
            if self.content_type == 'html':
                self._page = B(response.text, 'html.parser')
            else:
                self._page = B()
    
    def _init_kwargs(self, **kwargs):
        self._fulltext_kwargs, self._abstract_kwargs, self._title_kwargs, self._lang_kwargs = {}, {}, {}, {}
        for k,v in kwargs.items():
            field, key, *_ = k.split('__') + [None]
            if field == 'fulltext': self._fulltext_kwargs.update({key:v})
            elif field == 'abstract': self._abstract_kwargs.update({key:v})
            elif field == 'title': self._title_kwargs.update({key:v})
            elif field == 'lang': self._lang_kwargs.update({key:v})
    

    def _content_type(self):
        if self.url[-3:] == 'pdf': content = 'pdf'
        else:
            charset = self._header.get('Content-Type', '')
            content = re.findall('(html|pdf|json|xml)', charset)
            content = content[0] if len(content) else 'html'
        self.content_type = content


    def _get_content(self, tag, **kwargs):
        """
        Get content from element Tag
        tag: bs4.element.Tag
        script_keys: List, of keys if tag is script
        attr: str, key attribute if tag is neither a meta nor a script
        fields: List, of fields to concat if rebond
        :return: content
        """
        fields = kwargs.get('fields', ['fulltext'])
        if tag.name == 'meta':
            content = tag.attrs.get('content', [])
        elif tag.name == 'a' and tag.attrs.get('href') and self.rebond:
            self._presave = True
            raw_content = get_content(urljoin(self.url, tag.attrs['href']), rebond = False)
            content = '. '.join(raw_content.get(field, '') if raw_content.get(field, '') else '' for field in fields )
        elif tag.name == 'script':
            keys = kwargs.get('script_keys', [])
            try:
                serie = loads(tag.content[0])
            except:
                content = list()
            else:
                content = [rfinditem(serie, key) for key in keys]
        elif kwargs.get('attr'):
            content = tag.attrs.get(kwargs.get('attr'))
        else:
            content = tag.get_text(separator = ' ').strip().replace('\n', ' ')

        content = content[0] if isinstance(content, list) and len(content) else content
        content = unescape(content) if isinstance(content, str) else content
        return content
    

    def __repr__(self):
        string = "Title: {}\nFrom: {}\nFetched at: {}\nStatus: {}\nType: {}\n{} Abstract {}\n{}\n{} Full Text {}\n{}"
        return string.format(
            self.title, self.url, self.date,
            self._status, self.content_type,
            '-'*5, '-'*5, pcat(self.abstract),
            '-'*5, '-'*5, pcat(self.fulltext)
        )


    def fetch(self, selectors, which='first', **kwargs):
        content = list()
        arg_w = ('first', 'min', 'max')
        if which not in arg_w:
            raise ValueError(f'which should be one of {arg_w}')
        for s in selectors:
            contents_ = list()
            tags = self._page.select(s)
            if len(tags): contents_ = [self._get_content(tag, **kwargs) for tag in tags]
            if len(contents_) and which == 'first': 
                content = [contents_[0]]
                break
            else:
                try: content += ['. '.join(set(contents_))]
                except: pass
        content = content if len(content) else [None]
        if which == 'max': content = max(content, key=lambda x: len(str(x)))
        else: content = min(content, key=lambda x: len(str(x)))
        return content
    
    @property
    def title(self):
        title = None
        if self.content_type == 'html':
            title = self.fetch(settings.TITLE, **self._title_kwargs)
        return title
    
    @property
    def abstract(self):
        abstract = None
        if self.content_type == 'html':
            abstract = self.fetch(settings.ABSTRACT, **self._abstract_kwargs)
        return abstract
    
    @property
    def fulltext(self):
        fulltext = getattr(self, '_fulltext', None)
        if not fulltext and self.content_type == 'html':
            fulltext = self.fetch(settings.FULLTEXT, fields = ['fulltext'], **self._fulltext_kwargs)
            self._fulltext = fulltext if getattr(self, '_presave', False) else None
        return fulltext
    
    @property
    def lang(self):
        lang = None
        if self.content_type == 'html':
            lang = self._page.html.get('lang', None)
        return lang
    
    
    def to_dict(self, fulltext: bool = False):
        return {
            'url': self.url,
            'status': self._status,
            'title': self.title,
            'abstract': self.abstract,
            'fulltext': self.fulltext if fulltext else None,
            'lang': self.lang,
            'content_type': self.content_type,
            'date': self.date
        }
    
    def to_list(self, *args):
        if len(args): listed = [getattr(self, arg, None) for arg in args]
        else: listed = list(self.to_dict().values())
        return listed



class BaseContentExtractor(BaseExtractor):
    """
    Extractor for content in list
    """
    
    def _content(self):
        return list()
    
    @property
    def abstract(self):
        abstract = None
        try: abstract = self._content()[0].get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def fulltext(self):
        fulltext = None
        try: fulltext = '. '.join(map(lambda x:x.get_text(' ', True), self._content()[1:]))
        except: fulltext = super().fulltext
        return fulltext



class MdpiExtractor(BaseExtractor):
    """
    Extractor for base mdpi.com domain
    """
    
    @staticmethod
    def _clean_url(url):
        parsed = urlparse(url)
        path = re.sub(r'/(htm|pdf|xml|scifeed_display|notes|reprints|s[0-9]|review_report)?/?$', '', parsed.path) + '/htm'
        return f'{urljoin(url, path)}?{parsed.query}'
    
    @property
    def abstract(self):
        abstract = self._page.find(class_='art-abstract').get_text(separator = ' ').strip()
        abstract = super().abstract if not abstract else abstract
        return abstract

    @property
    def title(self):
        title = self._page.find(class_='title', attrs={
            'itemprop': 'name'
        }).get_text(separator = ' ').strip()
        title = super().title if not title else title
        return title
    
    @property
    def fulltext(self):
        self._fulltext = '. '.join(map(
            lambda x:x.get_text(' ', True),
            self._page.select('div[class="html-body"] section')))
        fulltext = super().fulltext if not len(self._fulltext) else self._fulltext
        return fulltext



class PMCExtractor(BaseContentExtractor):
    """
    Extractor for PubMed Central articles
    """
    
    def _content(self):
        return self._page.select('div[class="tsec sec" i]')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find('h1', class_='content-title').get_text(' ', True)
        except: title = super().title
        return title



class NihExtractor(BaseExtractor):
    """
    Extractor for base nih.gov domain
    """
    
    def __new__(cls, url, **kwargs):
        """
        Redirect to PMC version if exist
        """
        headers = default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        response = get(url, headers = headers)
        links = B(response.text, 'html.parser').select('a[class*="pmc"][data-ga-category*="full_text"]')
        if len(links):
            pmc_url = list({u.attrs['href'] for u in links if u.attrs.get('href')})[0]
            pmc_url = urljoin(url, pmc_url)
            return PMCExtractor(pmc_url, **kwargs)
        return super().__new__(cls)
    
    @property
    def abstract(self):
        try: abstract = self._page.find(id='enc-abstract').get_text(separator = ' ').strip()
        except: abstract = None
        finally: abstract = super().abstract if not abstract else abstract
        return abstract

    @property
    def title(self):
        try: title = self._page.find('h1', class_='heading-title').get_text(separator = ' ').strip()
        except: title = None
        finally: title = super().title if not title else title
        return title
    
    @property
    def fulltext(self):
        if getattr(self, '_fulltext', None): return self._fulltext
        full_url = list({
            u.attrs['href']
            for u in self._page.select('a[data-ga-category*="full_text" i]')
            if u.attrs.get('href')})
        try: _fulltext = get_content(full_url[-1], rebond = False)['fulltext']
        except: _fulltext = None
        if _fulltext:
            self._presave = True
            self._fulltext = _fulltext
        return super().fulltext



class ScienceDirectExtractor(BaseExtractor):
    """
    Extractor for base sciencedirect.com domain
    """

    @property
    def abstract(self):
        try:
            abstract = self._page.find(id='abstracts',
                                   class_='Abstracts').get_text(' ').strip()
        except: abstract = None
        abstract = super().abstract if not abstract else abstract
        return abstract

    @property
    def title(self):
        try: title = self._page.find('span', class_='title-text').get_text(' ').strip()
        except: title = None
        title = super().title if not title else title
        return title



class SpringerExtractor(BaseExtractor):
    """
    Extractor for base springer.com domain
    """
    
    @property
    def title(self):
        title = self._page.find('h1', class_ = 'c-article-title')
        title = title.get_text(' ').strip() if title else super().title
        return title
    
    @property
    def abstract(self):
        try:
            abstract = list(set(map(
                lambda x:x.get_text(' ', True),
                self._page.select(
                    'div[id^="Abs"][class*="c-article-section__content"]'
                ))))[0]
        except: abstract = super().abstract
        return abstract
    
    @property
    def fulltext(self):
        try:
            self._fulltext = '. '.join(set(map(
                lambda x:x.get_text(' ', True),
                self._page.select(
                    'div[id^="Sec"][class="c-article-section"]'
                ))))
        except: self._fulltext = None
        return super().fulltext



class ApsNetExtractor(BaseExtractor):
    
    @staticmethod
    def _clean_url(url):
        return re.sub(
            r'(/doi/)[a-zA-Z]*/?([0-9])',
            r'\1full/\2', url)
    
    @property
    def title(self):
        try: title = self._page.find('h1', class_ = 'citation__title').get_text(' ', True)
        except: title = None
        finally: title = title if title else super().title
        return title
        
    @property
    def abstract(self):
        try: abstract = self._page.find('div', class_ = 'hlFld-Abstract').get_text(' ', True)
        except: abstract = None
        finally: abstract = abstract if abstract else super().abstract
        return abstract
    
    @property
    def fulltext(self):
        try: self._fulltext = self._page.find('div', class_ = 'hlFld-Fulltext').get_text(' ', True)
        except: self._fulltext = None
        return super().fulltext



class WileyExtractor(BaseExtractor):
    
    @staticmethod
    def _clean_url(url):
        return re.sub(
            r'(/doi/)[a-zA-Z]*/?([0-9])',
            r'\1full/\2', url)
        
    @property
    def abstract(self):
        try: abstract = self._page.find(
            class_ = 'article-section article-section__abstract').get_text(' ', True)
        except: abstract = None
        finally: abstract = abstract if abstract else super().abstract
        return abstract
    
    @property
    def fulltext(self):
        try: self._fulltext = self._page.find(
            class_ = 'article-section article-section__full').get_text(' ', True)
        except: self._fulltext = None
        return super().fulltext



class DailyGroupExtractor(BaseContentExtractor):
    """
    Extractor for Daily Group
    """
    
    def _content(self):
        return self._page.select('div[itemprop="articleBody" i] p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find('h1', itemprop = 'name headline').get_text(' ', True)
        except: title = super().title
        return title



class FreshFruitPortalExtractor(BaseContentExtractor):
    """
    Extractor for Daily Group
    """
    
    def _content(self):
        return self._page.select('div[class="post-content" i] p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find(class_ = 'post-title').get_text(' ', True)
        except: title = super().title
        return title



class HuffingtonExtractor(BaseContentExtractor):
    """
    Extractor for HuffingtonPost
    """
    
    def _content(self):
        return self._page.select('.post-contents .content-list-component.text > p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find(class_ = 'headline__title').get_text(' ', True)
        except: title = super().title
        return title