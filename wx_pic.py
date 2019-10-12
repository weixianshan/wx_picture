import os
import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

from read_source import read_file


def scrapy_imgs(sour_path, targ_path):

    sources = read_file(path=sour_path)

    for url, child_path in sources:
        targetPath = os.path.join(targ_path, child_path)
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        with urlopen(url) as p:
            content = p.read().decode()

        partten = 'data-src="(https://[^\s]*?=png)"'
        regex = re.compile(partten, re.S)

        result = regex.findall(content)
        for index, item in enumerate(result):
            with urlopen(str(item)) as fp:
                path = os.path.join(targetPath, str(index) + ".png")
                with open(path, "wb") as fp1:
                    fp1.write(fp.read())


def scrapy_text(sour_path, targ_path):
    sources = read_file(path=sour_path)

    for url, child_path in sources:
        if not os.path.join(targ_path):
            os.makedirs(targ_path)

        targetPath = os.path.join(targ_path, child_path)

        with urlopen(url) as p:
            content = p.read()

        title_partten = "\d+\..*"

        soup = BeautifulSoup(content, 'html.parser')
        f = open(targetPath, "a")
        for tag in soup.find_all("p"):
            title, context = None, None
            strong_tag = tag.find("strong")
            if strong_tag is not None:
                span_tag = strong_tag.find("span")
                if span_tag is not None:
                    title = span_tag.get_text()

            span_tags = tag.find("span")
            if span_tags is not None and strong_tag is None:
                txt = span_tags.get_text()
                txt_arr = re.findall(r'.{' + str(50) + '}', txt)
                txt_arr.append(txt[(len(txt_arr) * 50):])
                context = "\n".join(txt_arr)

            if title is not None and re.match(title_partten, title):
                f.write(title)
                f.write("\n")
            if context is not None:
                f.write(context)
                f.write("\n\n")


if __name__ == "__main__":
    args = sys.argv
    source_path = args[1]
    target_path = args[2]
    select = args[3]

    if select == "text":
        scrapy_text(sour_path=source_path, targ_path=target_path)
    elif select == "img":
        scrapy_imgs(sour_path=source_path, targ_path=target_path)
