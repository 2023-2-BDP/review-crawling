from coupang import Coupang
from utils.add_data_to_csvfile import add_data_to_csvfile
from utils.url_editor import remove_query_params
from product_list import COMBI_PRODUCT_LIST

coupang = Coupang()

error_cnt = 0  # 에러 횟수가 1000번 이상이면 프로그램 종료

for search_word in COMBI_PRODUCT_LIST:
    product_links = coupang.get_product_links_by_search_word(search_word)

    # 한국어 encode 에러 문제로 q= 에 해당하는 param 제거
    product_links = [remove_query_params(link, "q") for link in product_links]
    for i, link in enumerate(product_links):
        try:
            reviews = coupang.get_reviews(link)

            # 헤더, 내용 모두 없는 리뷰 필터 (정상적인 내용이면 True 리턴)
            review_filter = lambda review: (
                "등록된 헤드라인이 없습니다" not in review["headline"]
            ) or ("등록된 리뷰내용이 없습니다" not in review["review_content"])

            # headline, review_content만 추출
            reviews = [
                {
                    "headline": review["headline"],
                    "review_content": review["review_content"],
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
