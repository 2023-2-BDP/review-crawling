from bs4 import BeautifulSoup as bs
from typing import Optional, Union, Dict, List
import requests as rq
import time
import re
from utils.get_headers import get_headers


class Coupang:
    def __init__(self) -> None:
        self.__headers: Dict[str, str] = get_headers(
            "json/headers_coupang.json", key="headers"
        )
        self.default_review_page_count = 50  # 리뷰 페이지 개수 기본값

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
            result = []
            for _url in urls:
                reviews = self.fetch_reviews(url=_url, session=session)
                if not reviews:
                    break
                result.append(reviews)
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

            # 리뷰가 없다면 (default_review_page_count를 넘어서면) 중단
            if article_lenth == 0:
                return False

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
        default_product_link_count = 50  # 상품 링크 개수 기본값
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
                        :default_product_link_count
                    ]
                ]
                return product_links

    def get_review_count(self, product_link: str):
        with rq.Session() as session:
            with session.get(url=product_link, headers=self.__headers) as response:
                html = response.text
                soup = bs(html, "html.parser")
                review_count = soup.select_one(".product-tab-review-count")
                return review_count


if __name__ == "__main__":
    from utils.add_data_to_csvfile import add_data_to_csvfile
    from utils.url_editor import remove_query_params
    from product_list import COMBI_PRODUCT_LIST

    coupang = Coupang()

    error_cnt = 0  # 에러 횟수가 1000번 이상이면 프로그램 종료
    current_product = ("청바지", 23)  # 티셔츠 9번째 상품부터 재시작
    start_crawling = False

    for search_word in COMBI_PRODUCT_LIST:
        product_links = coupang.get_product_links_by_search_word(search_word)
        # 한국어 encode 에러 문제로 q= 에 해당하는 param 제거
        product_links = [remove_query_params(link, "q") for link in product_links]
        for i, link in enumerate(product_links):
            # 특정 상품부터 재시작 설정
            if current_product == (search_word, i + 1):
                start_crawling = True
            if not start_crawling:
                continue

            try:
                print(f"{search_word} - {i+1}번째 상품 리뷰 데이터 진행 중")
                reviews = coupang.get_reviews(link)

                # 헤더, 내용 모두 없는 리뷰 필터 (정상적인 내용이면 True 리턴)
                review_filter = lambda review: (
                    "등록된 헤드라인이 없습니다" not in review["headline"]
                ) or ("등록된 리뷰내용이 없습니다" not in review["review_content"])

                # headline, review_content만 추출
                reviews = [
                    {
                        "rating": review["rating"],  # 리뷰 평점
                        "headline": review["headline"],  # 리뷰 제목
                        "review_content": review["review_content"],  # 리뷰 내용
                    }
                    for review in reviews
                    if review_filter(review)
                ]
                add_data_to_csvfile(
                    path="result/coupang_reviews.csv",
                    data=reviews,
                    sep="\t",
                )

                print(f"{search_word} - {i+1}번째 상품 리뷰 데이터 저장 완료")

            except Exception as e:
                error_cnt += 1
                if error_cnt >= 1000:
                    exit(0)
                print(f"{search_word} 검색어에서 오류 발생")
                add_data_to_csvfile(
                    path="result/coupang_reviews_error_log.csv",
                    data=[{"search_word": search_word, "n": i + 1, "error": str(e)}],
                    encoding=None,
                )
