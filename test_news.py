from glob import glob

import pytest
from parsel import Selector

from parse_news import *

files = {}
for filename in glob("data/html/news/situation-update-covid-19-*.html"):
    with open(filename, "r") as f:
        files[filename.split("/")[-1]] = f.read()


@pytest.mark.parametrize(
    "contents,expected",
    [
        (
            files["situation-update-covid-19-03152020.html"],
            [
                {"County": "Cleveland", "Cases": "1"},
                {"County": "Jackson", "Cases": "1"},
                {"County": "Oklahoma", "Cases": "1"},
                {"County": "Payne", "Cases": "1"},
                {"County": "Tulsa", "Cases": "3"},
            ],
        ),
        (
            # Switched to <th> elements for headers
            files["situation-update-covid-19-03192020.html"],
            [
                {"County": "Canadian", "Cases": "2"},
                {"County": "Cleveland", "Cases": "9"},
                {"County": "Custer", "Cases": "1"},
                {"County": "Grady", "Cases": "1"},
                {"County": "Jackson", "Cases": "1"},
                {"County": "Kay", "Cases": "2"},
                {"County": "Logan", "Cases": "1"},
                {"County": "McClain", "Cases": "1"},
                {"County": "Oklahoma", "Cases": "18"},
                {"County": "Pawnee", "Cases": "1"},
                {"County": "Payne", "Cases": "1"},
                {"County": "Tulsa", "Cases": "5"},
                {"County": "Washington", "Cases": "1"},
            ],
        ),
        (
            # Added Death column
            files["situation-update-covid-19-03262020.html"],
            [
                {"County": "Adair", "Cases": "2", "Deaths": "0"},
                {"County": "Bryan", "Cases": "1", "Deaths": "0"},
                {"County": "Canadian", "Cases": "6", "Deaths": "0"},
                {"County": "Carter", "Cases": "1", "Deaths": "0"},
                {"County": "Cleveland", "Cases": "39", "Deaths": "3"},
                {"County": "Comanche", "Cases": "3", "Deaths": "0"},
                {"County": "Craig", "Cases": "1", "Deaths": "0"},
                {"County": "Creek", "Cases": "10", "Deaths": "0"},
                {"County": "Custer", "Cases": "3", "Deaths": "0"},
                {"County": "Delaware", "Cases": "1", "Deaths": "0"},
                {"County": "Garvin", "Cases": "2", "Deaths": "0"},
                {"County": "Grady", "Cases": "2", "Deaths": "0"},
                {"County": "Jackson", "Cases": "1", "Deaths": "0"},
                {"County": "Kay", "Cases": "11", "Deaths": "0"},
                {"County": "Lincoln", "Cases": "1", "Deaths": "0"},
                {"County": "Logan", "Cases": "3", "Deaths": "0"},
                {"County": "Mayes", "Cases": "2", "Deaths": "0"},
                {"County": "McClain", "Cases": "2", "Deaths": "0"},
                {"County": "Muskogee", "Cases": "4", "Deaths": "0"},
                {"County": "Noble", "Cases": "2", "Deaths": "0"},
                {"County": "Oklahoma", "Cases": "73", "Deaths": "2"},
                {"County": "Okmulgee", "Cases": "2", "Deaths": "0"},
                {"County": "Osage", "Cases": "3", "Deaths": "0"},
                {"County": "Ottawa", "Cases": "1", "Deaths": "0"},
                {"County": "Pawnee", "Cases": "10", "Deaths": "1"},
                {"County": "Payne", "Cases": "5", "Deaths": "0"},
                {"County": "Pontotoc", "Cases": "1", "Deaths": "0"},
                {"County": "Pottawatomie", "Cases": "2", "Deaths": "0"},
                {"County": "Sequoyah", "Cases": "1", "Deaths": "0"},
                {"County": "Stephens", "Cases": "1", "Deaths": "0"},
                {"County": "Tulsa", "Cases": "41", "Deaths": "1"},
                {"County": "Wagoner", "Cases": "6", "Deaths": "0"},
                {"County": "Washington", "Cases": "5", "Deaths": "0"},
            ],
        ),
    ],
)
def test_parse_county_table(contents, expected):
    table = Selector(contents).xpath('//table[@summary="COVID-19 Cases by County"]')
    assert parse_county_table(table) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (
            files["situation-update-covid-19-03152020.html"],
            [
                {"Age Group": "00-04", "Cases": "0"},
                {"Age Group": "05-17", "Cases": "0"},
                {"Age Group": "18-49", "Cases": "3"},
                {"Age Group": "50-64", "Cases": "3"},
                {"Age Group": "65+", "Cases": "1"},
            ],
        ),
        (
            # Switched to <th> elements for headers
            files["situation-update-covid-19-03192020.html"],
            [
                {"Age Group": "00-04", "Cases": "2"},
                {"Age Group": "05-17", "Cases": "0"},
                {"Age Group": "18-49", "Cases": "21"},
                {"Age Group": "50-64", "Cases": "13"},
                {"Age Group": "65+", "Cases": "8"},
            ],
        ),
        (
            # Header change, added Death column
            files["situation-update-covid-19-03272020.html"],
            [
                {"Age Group": "00-04", "Cases": "3", "Deaths": "0"},
                {"Age Group": "05-17", "Cases": "5", "Deaths": "0"},
                {"Age Group": "18-35", "Cases": "54", "Deaths": "0"},
                {"Age Group": "36-49", "Cases": "64", "Deaths": "1"},
                {"Age Group": "50-64", "Cases": "81", "Deaths": "2"},
                {"Age Group": "65+", "Cases": "115", "Deaths": "5"},
            ],
        ),
    ],
)
def test_parse_age_group_table(contents, expected):
    table = Selector(contents).xpath('//table[@summary="COVID-19 Cases by Age Group"]')
    if not table:
        table = Selector(contents).xpath(
            '//table[@summary="COVID-19 Cases by Age Grouping"]'
        )
    assert parse_age_group_table(table) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (
            files["situation-update-covid-19-03152020.html"],
            [{"Gender": "Female", "Cases": "5"}, {"Gender": "Male", "Cases": "2"}],
        ),
        (
            # No header row
            files["situation-update-covid-19-03182020.html"],
            [{"Gender": "Male", "Cases": "16"}, {"Gender": "Female", "Cases": "13"}],
        ),
        (
            # Switched to <th> elements for headers, blank header
            files["situation-update-covid-19-03222020.html"],
            [{"Gender": "Female", "Cases": "33"}, {"Gender": "Male", "Cases": "34"}],
        ),
        (
            # Header change, added Death column
            files["situation-update-covid-19-03272020.html"],
            [
                {"Gender": "Female", "Cases": "165", "Deaths": "2"},
                {"Gender": "Male", "Cases": "157", "Deaths": "6"},
            ],
        ),
    ],
)
def test_parse_gender_table(contents, expected):
    table = Selector(contents).xpath('//table[@summary="COVID-19 Cases by Gender"]')
    assert parse_gender_table(table) == expected
