import requests
from bs4 import BeautifulSoup as bs
import re, os


URL = 'https://jlm-taurus.livejournal.com/calendar'

this_year = URL.replace('calendar', '2020')

LJ_NAME = re.search('://(.*).live', URL).group(1)

home = 'G:/Desktop/py/lj/' + LJ_NAME + '/'
lj_text = home + LJ_NAME + '.txt'
links_by_month = home + LJ_NAME + '_get_posts_by_month.txt'
all_posts = home + LJ_NAME + '_all_posts.txt'



class LJ:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)



    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass



    def get_years(self):
        soup = self.get_soup()

        years = [_['href'] for _ in soup.find('ul', class_='year').find_all('a')]
        # append 2020 year
        years.append(this_year)

        return years
            


    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('div', class_='asset-content'):
                post = month.find_all('a')
                for _ in post:
                    if 'View Subjects' in _.text:
                        print(_.get('href'))
                        links_by_month_.write(_.get('href') + '\n')

        links_by_month_.close()



    def get_all_posts(self):

        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            for post in soup.find_all('dd', class_='viewsubjects'):
                post = post.find_all('a')

                print(post[2]['href'])

                posts_.write(post[2]['href'] + '\n')

        posts_.close()



    def save_lj(self):

        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())

            title = soup.find('h1', class_='b-singlepost-title').text.strip()
            link = _.strip()
            text = soup.find('article', class_='b-singlepost-body').prettify()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')

            print(link.strip())
            print(title.strip())
            
        lj_.close()










class LJ2:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass


    def get_years(self):
        soup = self.get_soup()

        years = [_['href'] for _ in soup.find('ul', class_='j-years-nav').find_all('a')]
        # append 2020 year
        years.append(this_year)

        return years
            

    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('div', class_='j-calendar-month'):
                _ = month.a['href']
                links_by_month_.write(_ + '\n')

        links_by_month_.close()


    def get_all_posts(self):
        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            for post in soup.find_all('a', class_='j-day-subject-link'):
                print(post['href'])
                posts_.write(post['href'] + '\n')

        posts_.close()


    def save_lj(self):

        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())

            try:
                title = soup.find('h1', class_='b-singlepost-title').text.strip()
            except AttributeError:
                title = 'No subject'
            
            link = _.strip()
            text = soup.find('article', class_='b-singlepost-body').prettify()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            
            print(link)
            
        lj_.close()











class LJ3:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass


    def get_years(self):
        soup = self.get_soup()
        years = []

        for _ in soup.find('p', class_='Navigation').find_all('a'):
            match = re.search('\d\d\d\d', str(_))
            if match:
                years.append(_['href'])

        return years
            

    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('th', class_='MonthHeader'):
                _ = month.a['href']
                print(_)
                links_by_month_.write(_ + '\n')

        links_by_month_.close()


    def get_all_posts(self):
        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            try:
                for post in soup.find('div', class_='Listing').find_all('dd'):
                    post_url = post.a['href']
                    print(post_url)
                    posts_.write(post_url + '\n')
            except KeyError:
                pass                

        posts_.close()


    def save_lj(self):
        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())
            text = soup.find('div', class_='H3Holder s2-entrytext').prettify()

            try:
                title = text.h3.text.strip()
            except AttributeError:
                title = 'No subject'
            
            link = _.strip()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            
            print(title)
            print(link)
            print(data)
            
        lj_.close()






lj = LJ3()
# lj.get_years()
# lj.get_posts_by_month()
# lj.get_all_posts()
lj.save_lj()


