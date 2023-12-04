from coupang import Coupang
from naver import Naver
from utils.add_data_to_csvfile import add_data_to_csvfile

coupang = Coupang()
search_words = ["삼겹살", "주먹밥", "헤드셋"]  # 검색어
for search_word in search_words:
    for i, link in enumerate(coupang.get_product_links_by_search_word(search_word)):
        reviews = coupang.get_reviews(link)

        # headline, review_content만 추출
        reviews = [
            {"headline": review["headline"], "review_content": review["review_content"]}
            for review in reviews
        ]
        add_data_to_csvfile(
            path="result/coupang_reviews.csv",
            data=reviews,
            sep="\t",
        )

        print(f"{search_word} - {i+1}번째 상품 리뷰 데이터 저장 완료")


naver = Naver()
search_words = ["면도기", "쉐이빙크림"]  # 검색어
for search_word in search_words:
    for i, link in enumerate(naver.get_product_links_by_search_word(search_word)):
        try:
            print(0)
            reviews = naver.get_reviews(link)
            print(1)
        except Exception as e:
            print(f"Error fetching reviews for {search_word} - {i+1}번째 상품: {e}")
            continue

        reviews = [
            {"headline": review["title"], "review_content": review["content"]}
            for review in reviews
        ]

        try:
            # 디버깅을 위해 print 문 추가
            print(f"{search_word} - {i+1}번째 상품 리뷰 데이터 처리 중")

            add_data_to_csvfile(
                path="result/naver_reviews.csv",
                data=reviews,
                sep="\t",
            )

            print(f"{search_word} - {i+1}번째 상품 리뷰 데이터 저장 완료")

        except Exception as e:
            print(f"Error saving reviews to CSV for {search_word} - {i+1}번째 상품: {e}")


