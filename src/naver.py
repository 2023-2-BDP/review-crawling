from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from typing import Optional, Union, Dict, List
import requests as rq
import time
import re
import json
from utils.get_headers import get_headers


class Naver:
    def __init__(self):
        self.default_review_page_count = 5
        self.default_product_link_count = 10 # 임의로 10 설정
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    def get_reviews(url: str) -> str:
        """
        상품 URL을 입력받아 해당 상품의 리뷰를 반환하는 메소드
        가져올 리뷰 페이지 개수 - self.default_review_page_count
        """
        # URL 주소 재가공
        urls: List[str] = [
            f"{url}&page={page}"
            for page in range(1, self.default_review_page_count + 1)
        ]

        # __headers에 referer 키 추가
    
        self.__headers["referer"] = url

        with rq.Session() as session:
            result = [self.fetch_reviews(url=url, session=session) for url in urls]
            json_list = []
            for lst in result:
                json_list.extend(lst)
            return json_list

    def fetch_reviews(self, url: str, session: rq.Session) -> List[Dict[str, Union[str, int]]]:
        """상품 URL과 Session 객체를 입력받아 크롤링을 진행하고 해당 상품의 리뷰를 반환하는 메소드\n
        상 품명, 구매자 이름, 평점, 리뷰 제목, 리뷰 내용
        """

        save_data: List[Dict[str, Union[str, int]]] = list()

        with session.get(url=url, headers=self.__headers) as response:
            html = response.text
            soup = bs(html, "html.parser")

            # Review Items
            review_items = soup.select("ul.reviewItems_list_review__q726A > li")

            for review_element in review_items:
                dict_data: Dict[str, Union[str, int]] = dict()

                # 구매자 정보
                reviewer_info = review_element.select('span.reviewItems_etc__9ej69')
                mall_name = reviewer_info[0].get_text(strip=True)
                user_id = reviewer_info[1].get_text(strip=True)
                review_date = reviewer_info[2].get_text(strip=True)
                size_info = reviewer_info[3].get_text(strip=True)

                # 리뷰 제목 및 내용 추출
                title = review_element.select_one('em.reviewItems_title__AwHcz').get_text(strip=True)
                content = review_element.select_one('p.reviewItems_text__XrSSf').get_text(strip=True)

                dict_data["title"] = title
                dict_data["content"] = content

                save_data.append(dict_data)

        time.sleep(0.2)

        return save_data


    @staticmethod
    def get_product_code(url: str) -> str:
        """입력받은 URL 주소의 PRODUCT CODE 추출하는 메소드"""
        prod_code = url.split("products/")[-1].split("?")[0]
        return prod_code
    
    
    def get_product_links_by_search_word(self, search_word: str):
        """
        검색어를 입력받아 상품 URL을 반환하는 메소드\n
        상위 N개의 상품 - self.default_product_link_count
        """
        search_url = (
            f"https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query={search_word}"
        )
        with rq.Session() as session:
            with session.get(url=search_url, headers=self.__headers) as response:
                html = response.text
                soup = bs(html, "html.parser")
                product_links = [
                    urljoin(response.url, link.select_one("a").attrs["href"])
                    for link in soup.select(".search-product")[
                        : self.default_product_link_count
                    ]
                ]
                return product_links