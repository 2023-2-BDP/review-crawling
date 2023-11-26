from bs4 import BeautifulSoup as bs
from typing import Optional, Union, Dict, List
import requests as rq
import time
import re
import json
from utils.get_headers import get_headers


class Coupang:
    def __init__(self) -> None:
        self.__headers: Dict[str, str] = get_headers(
            "json/headers_coupang.json", key="headers"
        )
        self.default_review_page_count = 5  # 리뷰 페이지 개수 기본값
        self.default_product_link_count = 10  # 상품 링크 개수 기본값

    def get_reviews(self, url: str) -> List[Dict[str, Union[str, int]]]:
        """
        상품 URL을 입력받아 해당 상품의 리뷰를 반환하는 메소드\n
        가져올 리뷰 페이지 개수 - self.default_review_page_count
        """
        # URL의 Product Code 추출
        prod_code: str = self.get_product_code(url)

        # URL 주소 재가공
        urls: List[str] = [
            f"https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={page}&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true"
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

    def fetch_reviews(
        self, url: str, session: rq.Session
    ) -> List[Dict[str, Union[str, int]]]:
        """
        상품 URL과 Session 객체를 입력받아 크롤링을 진행하고 해당 상품의 리뷰를 반환하는 메소드\n
        상품명, 구매자 이름, 평점, 리뷰 제목, 리뷰 내용
        """

        save_data: List[Dict[str, Union[str, int]]] = list()

        with session.get(url=url, headers=self.__headers) as response:
            html = response.text
            soup = bs(html, "html.parser")

            # Article Boxes
            article_lenth = len(soup.select("article.sdp-review__article__list"))

            for idx in range(article_lenth):
                dict_data: Dict[str, Union[str, int]] = dict()
                articles = soup.select("article.sdp-review__article__list")

                # 구매자 이름
                user_name = articles[idx].select_one(
                    "span.sdp-review__article__list__info__user__name"
                )
                if user_name == None or user_name.text == "":
                    user_name = "-"
                else:
                    user_name = user_name.text.strip()

                # 평점
                rating = articles[idx].select_one(
                    "div.sdp-review__article__list__info__product-info__star-orange"
                )
                if rating == None:
                    rating = 0
                else:
                    rating = int(rating.attrs["data-rating"])

                # 구매자 상품명
                prod_name = articles[idx].select_one(
                    "div.sdp-review__article__list__info__product-info__name"
                )
                if prod_name == None or prod_name.text == "":
                    prod_name = "-"
                else:
                    prod_name = prod_name.text.strip()

                # 헤드라인(타이틀)
                headline = articles[idx].select_one(
                    "div.sdp-review__article__list__headline"
                )
                if headline == None or headline.text == "":
                    headline = "등록된 헤드라인이 없습니다"
                else:
                    headline = headline.text.strip()

                # 리뷰 내용
                review_content = articles[idx].select_one(
                    "div.sdp-review__article__list__review > div"
                )
                if review_content == None:
                    review_content = "등록된 리뷰내용이 없습니다"
                else:
                    review_content = re.sub("[\n\t]", "", review_content.text.strip())

                dict_data["prod_name"] = prod_name
                dict_data["user_name"] = user_name
                dict_data["rating"] = rating
                dict_data["headline"] = headline
                dict_data["review_content"] = review_content

                save_data.append(dict_data)

                # print(dict_data, "\n")

            time.sleep(0.1)

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
            f"https://www.coupang.com/np/search?component=&q={search_word}&channel=user"
        )
        with rq.Session() as session:
            with session.get(url=search_url, headers=self.__headers) as response:
                html = response.text
                soup = bs(html, "html.parser")
                product_links = [
                    f'{self.__headers["origin"]}{link.select_one("a").attrs["href"]}'
                    for link in soup.select(".search-product")[
                        : self.default_product_link_count
                    ]
                ]
                return product_links
