from glob import glob

import pytest

from extract import *

files = {}
for filename in glob("test-data/*.txt"):
    with open(filename, "r") as f:
        files[filename.split("/")[-1]] = f.read()


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], "March 22, 2020"),
        (files["covid-19_report-2.txt"], "March 23, 2020"),
        (files["covid-19_report-3.txt"], "March 24, 2020"),
        (files["covid-19_report-4.txt"], "March 25, 2020"),
        (files["covid-19_report-5.txt"], "March 26, 2020"),
        (files["covid-19_report-6.txt"], "March 27, 2020"),
    ],
)
def test_extract_date(contents, expected):
    assert extract_c19_report_date(contents) == expected


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 276, None, None),
        (files["covid-19_report-2.txt"], 282, None, None),
        (files["covid-19_report-3.txt"], 343, None, None),
        (files["covid-19_report-4.txt"], 290, 794, 37),
        (files["covid-19_report-5.txt"], 331, 906, 37),
        (files["covid-19_report-6.txt"], 316, 937, 34),
    ],
)
def test_extract_icu_beds(contents, numerator, denominator, percentage):
    assert extract_c19_icu_beds(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 2027, None, None),
        (files["covid-19_report-2.txt"], 2069, None, None),
        (files["covid-19_report-3.txt"], 2017, None, None),
        (files["covid-19_report-4.txt"], 2208, 4502, 49),
        (files["covid-19_report-5.txt"], 2216, 5283, 42),
        (files["covid-19_report-6.txt"], 2322, 5476, 42),
    ],
)
def test_extract_med_surg_beds(contents, numerator, denominator, percentage):
    assert extract_c19_med_surg_beds(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 379, None, None),
        (files["covid-19_report-2.txt"], 371, None, None),
        (files["covid-19_report-3.txt"], 431, None, None),
        (files["covid-19_report-4.txt"], 435, 433, 100),
        (files["covid-19_report-5.txt"], 519, 604, 86),
        (files["covid-19_report-6.txt"], 495, 602, 82),
    ],
)
def test_extract_or_beds(contents, numerator, denominator, percentage):
    assert extract_c19_or_beds(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 260, None, None),
        (files["covid-19_report-2.txt"], 205, None, None),
        (files["covid-19_report-3.txt"], 282, None, None),
        (files["covid-19_report-4.txt"], 152, 293, 52),
        (files["covid-19_report-5.txt"], 281, 480, 59),
        (files["covid-19_report-6.txt"], 265, 581, 46),
    ],
)
def test_extract_peds_beds(contents, numerator, denominator, percentage):
    assert extract_c19_peds_beds(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 28, None, None),
        (files["covid-19_report-2.txt"], 46, None, None),
        (files["covid-19_report-3.txt"], 50, None, None),
        (files["covid-19_report-4.txt"], 34, 146, 23),
        (files["covid-19_report-5.txt"], 52, 52, 100),
        (files["covid-19_report-6.txt"], 57, 97, 59),
    ],
)
def test_extract_picu_beds(contents, numerator, denominator, percentage):
    assert extract_c19_picu_beds(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 623),
        (files["covid-19_report-2.txt"], 611),
        (files["covid-19_report-3.txt"], 725),
        (files["covid-19_report-4.txt"], 682),
        (files["covid-19_report-5.txt"], 751),
        (files["covid-19_report-6.txt"], 746),
    ],
)
def test_extract_ventilators(contents, expected):
    assert extract_c19_ventilators(contents) == expected


@pytest.mark.parametrize(
    "contents,numerator,denominator,percentage",
    [
        (files["covid-19_report-1.txt"], 296, None, None),
        (files["covid-19_report-2.txt"], 350, None, None),
        (files["covid-19_report-3.txt"], 383, None, None),
        (files["covid-19_report-4.txt"], 342, 492, 70),
        (files["covid-19_report-5.txt"], 405, 745, 54),
        (files["covid-19_report-6.txt"], 443, 802, 55),
    ],
)
def test_extract_neg_flow_rooms(contents, numerator, denominator, percentage):
    assert extract_c19_neg_flow_rooms(contents) == (numerator, denominator, percentage)


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 5458),
        (files["covid-19_report-2.txt"], 4048),
        (files["covid-19_report-3.txt"], 5138),
        (files["covid-19_report-4.txt"], 4478),
        (files["covid-19_report-5.txt"], 4114),
        (files["covid-19_report-6.txt"], 4114),
    ],
)
def test_extract_occupancy(contents, expected):
    assert extract_c19_occupancy(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 9.1),
        (files["covid-19_report-2.txt"], 9.1),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], 9.7),
        (files["covid-19_report-5.txt"], 9.4),
        (files["covid-19_report-6.txt"], 11.1),
    ],
)
def test_extract_avg_days_ppe(contents, expected):
    assert extract_c19_avg_days_ppe(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 102616),
        (files["covid-19_report-2.txt"], 111616),
        (files["covid-19_report-3.txt"], 102616),
        (files["covid-19_report-4.txt"], 111904),
        (files["covid-19_report-5.txt"], 111904),
        (files["covid-19_report-6.txt"], 111808),
    ],
)
def test_extract_osdh_face_shields(contents, expected):
    assert extract_c19_osdh_face_shields(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 75492),
        (files["covid-19_report-2.txt"], 75492),
        (files["covid-19_report-3.txt"], 75492),
        (files["covid-19_report-4.txt"], 75492),
        (files["covid-19_report-5.txt"], 75492),
        (files["covid-19_report-6.txt"], 75474),
    ],
)
def test_extract_osdh_gowns(contents, expected):
    assert extract_c19_osdh_gowns(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 5530),
        (files["covid-19_report-2.txt"], 5530),
        (files["covid-19_report-3.txt"], 5530),
        (files["covid-19_report-4.txt"], 5590),
        (files["covid-19_report-5.txt"], 5570),
        (files["covid-19_report-6.txt"], 5570),
    ],
)
def test_extract_osdh_gloves(contents, expected):
    assert extract_c19_osdh_gloves(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 5530),
        (files["covid-19_report-2.txt"], 5530),
        (files["covid-19_report-3.txt"], 5530),
        (files["covid-19_report-4.txt"], 5590),
        (files["covid-19_report-5.txt"], 5570),
        (files["covid-19_report-6.txt"], 5570),
    ],
)
def test_extract_osdh_gloves(contents, expected):
    assert extract_c19_osdh_gloves(contents) == expected


# TODO: Masks, Facility counts (24-Mar)


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 67),
        (files["covid-19_report-2.txt"], 81),
        (files["covid-19_report-3.txt"], 106),
        (files["covid-19_report-4.txt"], 164),
        (files["covid-19_report-5.txt"], 248),
        (files["covid-19_report-6.txt"], 322),
    ],
)
def test_extract_positives(contents, expected):
    assert extract_c19_positives(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], 35),
        (files["covid-19_report-5.txt"], 41),
        (files["covid-19_report-6.txt"], 50),
    ],
)
def test_extract_positives_icu(contents, expected):
    assert extract_c19_positives_icu(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], False),
        (files["covid-19_report-5.txt"], False),
        (files["covid-19_report-6.txt"], 105),
    ],
)
def test_extract_positives_hospitalized(contents, expected):
    assert extract_c19_positives_hospitalized(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 247),
        (files["covid-19_report-2.txt"], 257),
        (files["covid-19_report-3.txt"], 399),
        (files["covid-19_report-4.txt"], 326),
        (files["covid-19_report-5.txt"], 334),
        (files["covid-19_report-6.txt"], 377),
    ],
)
def test_extract_positives_pui_hospital(contents, expected):
    assert extract_c19_pui_hospital(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], 93),
        (files["covid-19_report-5.txt"], 92),
        (files["covid-19_report-6.txt"], 105),
    ],
)
def test_extract_positives_pui_icu(contents, expected):
    assert extract_c19_pui_icu(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 395),
        (files["covid-19_report-2.txt"], 340),
        (files["covid-19_report-3.txt"], 492),
        (files["covid-19_report-4.txt"], 373),
        (files["covid-19_report-5.txt"], 467),
        (files["covid-19_report-6.txt"], 433),
    ],
)
def test_extract_self_quarantine(contents, expected):
    assert extract_c19_self_quarantine(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 2686),
        (files["covid-19_report-2.txt"], 2269),
        (files["covid-19_report-3.txt"], 15410),
        (files["covid-19_report-4.txt"], 11369),
        (files["covid-19_report-5.txt"], 14211),
        (files["covid-19_report-6.txt"], 15197),
    ],
)
def test_extract_c19_testing_supplies(contents, expected):
    assert extract_c19_testing_supplies(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], 88),
        (files["covid-19_report-2.txt"], 92),
        (files["covid-19_report-3.txt"], 92),
        (files["covid-19_report-4.txt"], 88),
        (files["covid-19_report-5.txt"], 95),
        (files["covid-19_report-6.txt"], 92),
    ],
)
def test_extract_c19_hospital_reporting_compliance(contents, expected):
    assert extract_c19_hospital_reporting_compliance(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], False),
        (files["covid-19_report-5.txt"], False),
        (files["covid-19_report-6.txt"], 113),
    ],
)
def test_extract_c19_positives_osdh_lab(contents, expected):
    assert extract_c19_positives_osdh_lab(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], False),
        (files["covid-19_report-5.txt"], False),
        (files["covid-19_report-6.txt"], 55),
    ],
)
def test_extract_c19_positives_dlo(contents, expected):
    assert extract_c19_positives_dlo(contents) == expected


@pytest.mark.parametrize(
    "contents,expected",
    [
        (files["covid-19_report-1.txt"], False),
        (files["covid-19_report-2.txt"], False),
        (files["covid-19_report-3.txt"], False),
        (files["covid-19_report-4.txt"], False),
        (files["covid-19_report-5.txt"], False),
        (files["covid-19_report-6.txt"], 154),
    ],
)
def test_extract_c19_positives_other_labs(contents, expected):
    assert extract_c19_positives_other_labs(contents) == expected
