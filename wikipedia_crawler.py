from bs4 import BeautifulSoup
import requests, time, urllib

start_url = "https://en.wikipedia.org/wiki/Grand_Theft_Auto_V"
target_url = "https://en.wikipedia.org/wiki/Video_game_genre"

article_chain = [start_url]

def web_crawl():
    while continue_crawl(article_chain, target_url):
        # download html of last article in article_chain
        report = requests.get(article_chain[-1])
        out_html = report.text
        # find the first link in that html
        first_link = find_first_link(article_chain[-1])
        # add the first link to article chain
        article_chain.append(first_link)
        # delay for about two seconds
        time.sleep(2)

def find_first_link(url):
    # get the HTML from "url", use the requests library
    report = requests.get(article_chain[-1])
    out_html = report.text
    # feed the HTML into Beautiful Soup
    soup = BeautifulSoup(out_html, 'html.parser')
    # find the first link in the article
    out_div = soup.find(id='mw-content-text').find(class_='mw-parser-output')#.p.a.get('href')
    rel_link = None
    for element in out_div.find_all("p", recursive = False):
        if element.a:
            rel_link = element.find("a", recursive = False).get('href')
            break

    if not rel_link:
        return

    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', rel_link)
    # return the first link as a string, or return None if there is no link
    return first_link

def continue_crawl(search_history, target_url):
    if search_history[-1] == target_url:
        print("Found it")
        return False
    elif len(search_history) > 25:
        print("Max Length exceeded")
        return False
    elif len(search_history) != len(set(search_history)):
        print("History repeats itself")
        return False
    else:
        return True

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no links, aborting search!")
        break

    article_chain.append(first_link)

    time.sleep(2)
