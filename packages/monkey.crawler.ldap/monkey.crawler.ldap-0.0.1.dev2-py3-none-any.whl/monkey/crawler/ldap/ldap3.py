# -*- coding: utf-8 -*-

from ldap3 import Server, Connection, SUBTREE

from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class LDAPCrawler(Crawler):

    def __init__(self, source_name: str, processor: Processor, ds_hostname: str, user_name: str, password: str,
                 search_base: str, search_filter: str, attributes=None,
                 search_scope=SUBTREE, limit: int = 0, page_size=100, offset: int = 0, max_retry: int = 0):
        super().__init__(source_name, processor, offset, max_retry)
        self.ds_hostname = ds_hostname
        self.user_name = user_name
        self.password = password
        self.base_dn = search_base
        self.search_filter = search_filter
        self.attributes = attributes
        self.limit = limit
        self.search_scope = search_scope
        self.page_size = page_size

    def _get_records(self):
        server = Server(self.ds_hostname)
        conn = Connection(server, user=self.user_name, password=self.password)
        conn.bind()
        self._cursor = conn.extend.standard.paged_search(self.base_dn, self.search_filter,
                                                         search_scope=self.search_scope,
                                                         attributes=self.attributes,
                                                         paged_size=self.page_size,
                                                         size_limit=self.limit,
                                                         generator=True)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            rec = next(self._cursor)
            dn = rec.get('dn', None)
            if dn is None:
                return next(self)
            else:
                record = {
                    'dn': dn
                }
                record.update(rec['attributes'])
                return record
        except StopIteration as e:
            raise e

    def _echo_start(self):
        self.logger.info(
            f'Crawling {self.source_name} from LDAP server {self.ds_hostname}.'
        )
