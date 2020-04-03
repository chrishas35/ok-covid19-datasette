from parsel import Selector


def main():
    # with open("data/html/news/situation-update-covid-19-03152020.html", "r") as f:
    with open("data/html/osdh-homepage-2020-04-03_1110.html", "r") as f:
        sel = Selector(f.read())

    for table in sel.css("table"):
        if table.attrib["summary"] == "COVID-19 Cases by County":
            parse_county_table(table)
        elif table.attrib["summary"] == "COVID-19 Cases by Age Group":
            parse_age_group_table(table)
        elif table.attrib["summary"] == "COVID-19 Cases by Gender":
            parse_gender_table(table)
        else:
            continue


def parse_county_table(table):
    # 26 March added Deaths
    # print(table.get())
    rows = table.css("tr")
    # print("".join(rows[0].css("td")[0].css("*::text").getall()).strip())
    headers = [
        "".join(col.css("*::text").getall()).strip()
        for col in rows[0].css("td, th")  # 20 Mar used th instead of td, 21 onward
    ]
    headers = [
        "Cases"
        if header in ("COVID-19 Cases by County", "COVID-19 Cases by County*")
        else header
        for header in headers
    ]

    values = list()
    for row in rows[1:-1]:
        values.append(
            dict(
                zip(headers, [col.css("::text").get().strip() for col in row.css("td")])
            )
        )

    print(values)


def parse_age_group_table(table):
    pass


def parse_gender_table(table):
    pass


if __name__ == "__main__":
    main()
