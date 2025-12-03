#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 22:17:30 2025

@author: pi
"""

import re

def clean_text(text):
    c1=re.sub(r' \([^)]+', '', text)
    c2=re.sub(r'\)', '', c1)
    c10=c2
    return c10

def substring_until(text,str_until):
    index = text.find(str_until)
    if index != -1:
        return text[:index]
    else:
        return text




texts = [
    "example1 (Europe) (En,Fr,De,Es,It)[!]",
    "example2 (Asia) (En,Fr,De,Es,It)",
    "example2 [!] (Asia) (En,Fr,De,Es,It)",
]

clean_texts = [clean_text(text) for text in texts]

print(clean_texts)

ctexts = [substring_until(text,' (') for text in texts]
clean_texts = [substring_until(ctext,' [') for ctext in ctexts]

print(clean_texts)