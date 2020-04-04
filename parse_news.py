from glob import glob

from parsel import Selector


def main():
    for filename in sorted(glob("data/html/news/situation-update-covid-19-*.html")):
        print(f"{filename}...")
        with open(filename, "r") as f:
            sel = Selector(f.read())

        for table in sel.css("table"):
            if table.attrib["summary"] == "COVID-19 Cases by County":
                parse_county_table(table)
            elif table.attrib["summary"] in (
                "COVID-19 Cases by Age Group",
                "COVID-19 Cases by Age Grouping",
            ):
                parse_age_group_table(table)
            elif table.attrib["summary"] == "COVID-19 Cases by Gender":
                print(parse_gender_table(table))
            else:
                continue


def parse_county_table(table):
    # 26 March added Deaths
    # print(table.get())
    rows = table.css("tr")
    # print("".join(rows[0].css("td")[0].css("*::text").getall()).strip())
    headers = [
        "".join(col.css("*::text").getall()).strip() for col in rows[0].css("td, th")
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

    return values


def parse_age_group_table(table):
    rows = table.css("tr")
    headers = [
        "".join(col.css("*::text").getall()).strip() for col in rows[0].css("td, th")
    ]
    headers = [
        "Cases"
        if header in ("COVID-19 Cases*", "COVID-19 Cases")
        else "Age Group"
        if header == "Age Group, Years"
        else header
        for header in headers
    ]

    values = list()
    for row in rows[1:-2]:
        values.append(
            dict(
                zip(headers, [col.css("::text").get().strip() for col in row.css("td")])
            )
        )

    return values


def parse_gender_table(table):
    rows = table.css("tr")
    if len(rows) == 3:
        # No header row for 18-21 March
        start = 0
        headers = ["Gender", "Cases"]
    else:
        start = 1
        headers = [
            "".join(col.css("*::text").getall()).strip()
            for col in rows[0].css("td, th")
        ]
        headers = [
            "Gender"
            if header in ("County", "")
            else "Cases"
            if header == "COVID-19 Cases by Gender"
            else header
            for header in headers
        ]

    values = list()
    for row in rows[start:-1]:
        values.append(
            dict(
                zip(headers, [col.css("::text").get().strip() for col in row.css("td")])
            )
        )

    return values


if __name__ == "__main__":
    main()
