import requests, zipfile, io, json
from collections import namedtuple

class Wrapper:

    def __init__(self):
        self.url = 'https://www.quandl.com/api/v3/databases'
        self.session = requests.Session()

    def get_pages(self):
        first_page = self.session.get(self.url).json()
        yield first_page
        num_pages = first_page['meta']['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self.session.get(self.url, params={'page': page}).json()
            yield next_page

    def databases(self):
        dbs = []

        for page in self.get_pages():
            print(page)
            for row in page['databases']:
                dbs.append(row)

        return dbs

    def metas(self, dbs):
        for db in dbs:
            if db['premium'] == False:
                zipUrl = self.url + '/' + db['database_code'] + '/metadata'
                r = requests.get(zipUrl)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall('../meta/')


if __name__ == "__main__":
    wrapper = Wrapper()

    dbs = wrapper.databases()
    wrapper.metas(dbs)
