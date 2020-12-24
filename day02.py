#!/usr/bin/env python
# coding: utf-8

# In[13]:

import re
from collections import Counter

from util import get_data
# In[8]:


def parse_val(val):
    for datatype in int, float, str:
        try:
            return datatype(val)
        except:
            pass


def extract(line):
    parts = re.findall(r'[a-zA-Z0-9]+', line)
    return [*map(parse_val, parts)]


# In[10]:


def load():
    get_data(2)  #make sure 2.txt is present
    with open("input/2.txt", "r") as f:
        data = f.readlines()
    return [*map(extract, data[:-1])]


# In[19]:


def pass_ok_1(entry):
    l, u, c, pw = entry
    return l <= Counter(pw)[c] <= u


def part1(data):
    return len([*filter(pass_ok_1, data)])


def pass_ok_2(entry):
    l, u, c, pw = entry
    return sum(1 for i in [l, u] if pw[i - 1] == c) == 1


def part2(data):
    return len([*filter(pass_ok_2, data)])


# In[18]:

data = load()
print(part1(data))

# In[20]:

print(part2(data))

# In[ ]:
