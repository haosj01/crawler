#!/usr/bin/python
# -*- coding: UTF-8 -*-
from dataclasses import dataclass


@dataclass()
class Data_dto:
    current: int
    pages: int
    size: int
    total: int
    records: list
