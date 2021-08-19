#!/usr/bin/python
# -*- coding: UTF-8 -*-
from dataclasses import dataclass
from dto.data_dto import Data_dto

@dataclass()
class Reslut_dto:
    code: str
    data: {}
    msg: str
