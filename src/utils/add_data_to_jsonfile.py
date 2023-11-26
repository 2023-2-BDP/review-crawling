import json


def add_data_to_jsonfile(path: str, data):
    """
    객체 형태의 데이터를 JSON 파일에 추가하는 메소드\n
    파일이 없거나 비어있을 경우에는 새로운 JSON 파일을 생성하고 데이터를 추가한다
    """
    with open(path, "r", encoding="UTF-8") as file:
        json_data = None

        # 파일이 비어있을 경우
        try:
            json_data = json.load(file)
        except:
            json_data = list()
        json_data.extend(data)
        json.dump(
            json_data,
            open("json/coupang.json", "w", encoding="UTF-8"),
            indent=4,
            ensure_ascii=False,
        )
