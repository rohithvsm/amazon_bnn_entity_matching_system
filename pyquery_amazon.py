#!/usr/bin/env python

from pyquery import PyQuery as pq
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
}

def get_book_info(url):
    response = requests.get(url, headers=headers)
    doc = pq(response.content)

    book = {}

    # <span id="productTitle" class="a-size-large">Harry Potter and the Sorcerer's Stone (Harry Potters)</span>
    title = doc('#productTitle').text()
    book['title'] = title

    # <a data-asin="B000AP9A6K" class="a-link-normal contributorNameID" href="/J.K.-Rowling/e/B000AP9A6K/ref=dp_byline_cont_book_1">J.K. Rowling</a>
    author = doc('.contributorNameID').text()
    book['author'] = author


    # <span class="a-size-medium a-color-price offer-price a-text-normal">$6.92</span>
    price_text = doc("span.offer-price.a-color-price").text()
    price = float(price_text[1:]) # get rid of the dollar sign
    book['price'] = price

    print doc('#productDetails')
    print doc('Publisher')

    return book

def main():
    print get_book_info('http://www.amazon.com/dp/059035342X/')

if __name__ == "__main__":
    main()
