import csv

import requests
from sqlalchemy.orm import Mapped

from jobs_api.common.database.base import BaseModel
from jobs_api.common.types import int_pk


class GeoModel(BaseModel):
    __tablename__ = "geo"

    id: Mapped[int_pk]
    name: Mapped[str]
    parent_id: Mapped[int | None]


def download_geo() -> list[dict[str, str | int]]:
    url = "https://raw.githubusercontent.com/hflabs/city/master/city.csv"
    response = requests.get(url)
    if response.status_code == 200:
        geo_csv = response.text
        all_geo = list(csv.DictReader(geo_csv.splitlines(), delimiter=","))

        region_id = 1
        # Более оптимизированный вариант, но не красивый
        # geo: dict[str, int] = {}
        # geo_rows: list[tuple[int, str, int | None]] = []
        #
        # for country, region, city in {(row["country"], row["region"], row["city"]) for row in all_geo}:
        #     if country not in geo:
        #         geo[country] = region_id
        #         geo_rows.append((region_id, country, None))
        #     if region not in geo:
        #         geo[region] = region_id
        #         geo_rows.append((region_id, region, geo[country]))
        #     if city not in geo:
        #         geo[city] = region_id
        #         geo_rows.append((region_id, city, geo[region]))
        #     region_id += 1

        # Тут можно было бы пройтись в один цикл, но для красоты дерева и сортировки по алфавиту сделал так
        geo: dict[str, int] = {}
        geo_rows: list[dict[str, str | int]] = []
        for country in {row["country"] for row in all_geo}:
            geo_rows.append({"id": region_id, "name": country, "parent_id": None})
            geo[country] = region_id
            region_id += 1
        for country, region in sorted({(row["country"], row["region"]) for row in all_geo}):
            geo_rows.append({"id": region_id, "name": region, "parent_id": geo[country]})
            geo[region] = region_id
            region_id += 1
        for country, region, city in sorted({(row["country"], row["region"], row["city"]) for row in all_geo}):
            geo_rows.append({"id": region_id, "name": city, "parent_id": geo[region]})
            region_id += 1
        return geo_rows
    else:
        raise Exception("Can't download geo")
