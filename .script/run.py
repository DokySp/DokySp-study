'''
# Script for creating README.md
'''

from re import L
import requests
from bs4 import BeautifulSoup


class Data:
    title = ""
    content = ""
    status = "unknown"
    # lang = "unknown"
    # branch = -1
    # star = -1
    # issues = -1
    # pulls = -1
    date = ""


data_list = []
page_no = 1
done_num = 0
ip_num = 0

while True:

    res = requests.get(
        f"https://github.com/orgs/DokySp-study/repositories?page={page_no}")
    raw_doc = BeautifulSoup(res.content, 'html.parser')

    raw_doc = raw_doc.find(
        "div", {"data-view-component": "true", "class": "Box"})

    if raw_doc == None:
        break

    lists = raw_doc.find("ul").findAll("li")

    result_md = ""
    result_md += "# DokySp Study\n\n"
    result_md += "- 개인 공부 내용을 정리한 Organization입니다.\n"
    result_md += "- 매주 월요일 0시에 업데이트됩니다. 최신 내용을 확인하시려면 아래 Organization을 방문해주세요.\n"

    for i, item in enumerate(lists):
        # print(f"========={i}=========")
        data = Data()

        header = item.find("div").find(
            "div", {"class": "d-flex flex-justify-between"}).find("div")
        additional = item.find("div").find(
            "div", {"data-view-component": "true", "class": "color-fg-muted f6 mt-2"})

        title = header.find("h3").find("a")
        content = header.find("p")

        data.title = title.text.strip()

        if data.title[0] == ".":
            continue

        if content is not None:
            content = content.text.strip()

            if content.find("[Done]") == 0:
                # 완료
                data.status = "Done"
                data.content = content[6:]
                done_num += 1
            else:
                # 미분류 / 작업중
                data.status = "In Progress"
                data.content = content
                ip_num += 1
        else:
            # 미분류 / 작업중
            data.status = "In Progress"
            data.content = ""
            ip_num += 1

        # add1 = additional.findAll("a")
        # add2 = additional.findAll("span")

        # for i, item in enumerate(add1):
        #     if i == 0:
        #         star = int(item.text.strip())
        #     elif i == 1:
        #         issues = int(item.text.strip())

        # print(len(add2))

        # if len(add2) == 4:
        #     lang = add2.pop(0).text.strip()

        # print(len(add2), lang)

        # for i, item in enumerate(add2):
        #     print(i, item.text)
        #     if i == 0:
        #         branch = int(item.text.strip())
        #     elif i == 1:
        #         pulls = int(item.text.strip())
        #     elif i == 2:
        #         date = item.text.strip()

        ###############

        data.date = additional.find(
            "span", {"data-view-component": "true", "class": "no-wrap"}).text.strip()

        #####
        data_list.append(data)

    page_no += 1


result_md += f"- **총 {len(data_list)}개 레포** [완료: {done_num}개 / 진행중: {ip_num}개]\n"
result_md += "- [📚 Organization 방문하기](https://github.com/DokySp-study)\n\n"
result_md += "<br>\n\n"

data_list.sort(key=lambda x: x.title)
data_list.sort(key=lambda x: x.status)
ip_sep = False
result_md += "## **✅ 완료**\n\n"

for data in data_list:
    if not ip_sep and data.status == "In Progress":
        ip_sep = True
        result_md += "<br><br>\n\n"
        result_md += "## **🚧 진행중**\n\n"

    if data.content == "":
        result_md += f"### [{data.title}](https://github.com/DokySp-study/{data.title})\n\nstatus: **{data.status}**\n<br>`{data.date}`\n\n"
    else:
        result_md += f"### [{data.title}](https://github.com/DokySp-study/{data.title})\n\n{data.content}\n\n<br>`{data.date}`\n\n"

# make README.md file
f = open("README.md", 'w')
f.writelines(result_md)
f.close()

print(result_md)
