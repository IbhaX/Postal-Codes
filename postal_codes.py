from __future__ import annotations
from dataclasses import dataclass as dc, asdict, field
from pydantic.dataclasses import dataclass
from typing import Optional

import requests
import json

class NothingToSearchException(Exception):
    __module__ = Exception.__module__
    def __str__(self):
        return (
            "Search for some keyword first!!\n"
            "TypeError is a side effect of this Exception!!"
          )
          
@dataclass
class Area:
    state: str
    district: str
    taluk: str
    pincode: int
    to_dict = asdict


@dataclass
class Locations:
    areas: list[Area]
    to_dict = asdict

Response = requests.models.Response

class Pincode:
    def __init__(self) -> None:
        self.__pincode_list = self.__get_data()
        self.__locations = None
    
    @property
    def __convert(self) -> Locations:
        try:
            return Locations([Area(**i) for i in self.__locations])
        except TypeError:
            raise NothingToSearchException
        
    def __get_data(self) -> Response:
        url = "https://raw.githubusercontent.com/IbhaX/json/main/pincodes.json"
        return requests.get(url).json()["locations"]
    
    def by_state(self, state: str) -> Pincode:
        areas = []
        state = "".join(state.casefold().split())
        areas_list = self.__locations or self.__pincode_list
        for area in areas_list:
            jstate = "".join(area["state"].casefold().split())
            if jstate is state or state in jstate:
                areas.append(area)
        self.__locations = areas
        return self
    
    def by_district(self, district: str) -> Pincode:
        areas = []
        district = "".join(district.casefold().split())
        areas_list = self.__locations or self.__pincode_list
        for area in areas_list:
            jdistrict = "".join(area["district"].casefold().split())
            if district is jdistrict or district in jdistrict:
                areas.append(area)
        self.__locations = areas
        return self
    
    def by_taluk(self, taluk: str) -> Pincode:
        areas = []
        taluk = "".join(taluk.casefold().split())
        areas_list = self.__locations or self.__pincode_list
        for area in areas_list:
            jtaluk = "".join(area["taluk"].casefold().split())
            if taluk is jtaluk or taluk in jtaluk:
                areas.append(area)
        self.__locations = areas
        return self
    
    def by_pincode(self, pincode: int) -> Pincode:
        areas = []
        areas_list = self.__locations or self.__pincode_list
        for area in areas_list:
            if area["pincode"] is int(pincode) or str(pincode) in str(area["pincode"]):
                areas.append(area)
        self.__locations = areas
        return self
    
    def dict(self) -> dict:
        return self.__convert.to_dict()
     
    def json(self, indent: int=4) -> json:
         return json.dumps(self.__convert.to_dict(), indent=indent)
    
    def schema(self) -> json:
        return self.__convert.__pydantic_model__.schema()
      
    def __repr__(self) -> str:
        return str(self.schema()) if self.__locations else "null"
    
    def __str__(self) -> str:
        return "Type \"print(instance.dict())\" or \"print(instance.json())\" to print the result!!" if self.__locations else "No queries found!!"


if __name__ == "__main__":
    postal = Pincode()
    postal.by_taluk("ara")\
          .by_state("tam")\
          .by_district("nil")\
          .by_pincode(212)
    p = postal.dict()
    print(p)
    
    

