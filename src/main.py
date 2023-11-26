from coupang import Coupang
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
