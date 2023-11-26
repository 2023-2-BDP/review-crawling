from typing import List, Dict
import os


def add_data_to_csvfile(
    path: str, data: List[Dict], sep: str = ",", encoding: str = "UTF-8"
):
    """
    객체 형태의 데이터를 CSV 파일에 추가하는 메소드\n
    파일이 없거나 비어있을 경우에는 새로운 CSV 파일을 생성하고 데이터를 추가한다.
    """
    with open(path, "a", encoding=encoding) as file:
        # 파일이 비어있을 경우
        if os.path.getsize(path) == 0:
            file.write(sep.join(data[0].keys()) + "\n")

        for idx in range(len(data)):
            file.write(sep.join(map(str, data[idx].values())) + "\n")
