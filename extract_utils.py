import logging
import re
from glob import glob

import sqlite_utils
from dateutil.parser import parse
from tika import parser

REGEX_INTEGER_WITH_COMMAS = r"\d{1,3}(?:,\d{3})*"
REGEX_NUMBER_WITH_DECIMAL = r"\d*\.?\d+"


def int_or_none(val):
    if val:
        try:
            return int(val.replace(",", ""))
        except:
            return None
    return None


def float_or_none(val):
    if val:
        try:
            return float(val)
        except:
            return None
    return None


_content_cache = {}


def get_contents(pdf):
    global _content_cache

    if pdf not in _content_cache:
        logging.info(f"Parsing {pdf}")
        raw = parser.from_file(pdf)
        _content_cache[pdf] = raw["content"]
    return _content_cache[pdf]


def extract_c19_report_date(contents):
    pattern = r"COVID-19 Report (\w+ \d+, \d+)"
    match = re.search(pattern, contents)
    if match:
        return match.group(1)
    else:
        return False


def extract_c19_icu_beds(contents):
    pattern = fr"ICU Beds(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS}) \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_med_surg_beds(contents):
    pattern = fr"Medical Surgery Beds(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS}) \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_or_beds(contents):
    pattern = fr"Operating Room Beds(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS})\^? \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_peds_beds(contents):
    pattern = fr"Pediatric Beds(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS}) \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_picu_beds(contents):
    pattern = fr"PICU Beds(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS})\*? \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_ventilators(contents):
    pattern = fr"Ventilators:(?: Available)? ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_neg_flow_rooms(contents):
    pattern = fr"Negative Flow rooms(?: Available)?: ({REGEX_INTEGER_WITH_COMMAS})(?: of ({REGEX_INTEGER_WITH_COMMAS}) \((\d+)%\))?"
    match = re.search(pattern, contents)
    if match:
        return (
            int_or_none(match.group(1)),
            int_or_none(match.group(2)),
            int_or_none(match.group(3)),
        )
    else:
        return False


def extract_c19_occupancy(contents):
    pattern = fr"occupancy status: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_avg_days_ppe(contents):
    pattern = fr"Protective Equipment\(PPE\): ({REGEX_NUMBER_WITH_DECIMAL})"
    match = re.search(pattern, contents)
    if match:
        return float_or_none(match.group(1))
    else:
        return False


def extract_c19_osdh_face_shields(contents):
    pattern = fr"Total Face Shields: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_osdh_gowns(contents):
    pattern = fr"Total Gowns: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_osdh_gloves(contents):
    pattern = fr"Total Gloves(?: \(boxes\))?: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_positives(contents):
    pattern = fr"Positive Patients: \n\n\(hospitals, state & private labs\)\n({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_positives_icu(contents):
    pattern = fr"Positive Patients: \n\n\(hospitals, state & private labs\)\n(?P<positives>{REGEX_INTEGER_WITH_COMMAS})(?:(?: \(|; )?(?:(?P<positives_hospitalized>{REGEX_INTEGER_WITH_COMMAS}) Hospitalized; )?(?P<positives_icu>{REGEX_INTEGER_WITH_COMMAS}) in ICU\)?)?"
    match = re.search(pattern, contents)
    if match.group("positives_icu"):
        return int_or_none(match.group("positives_icu"))
    else:
        return False


def extract_c19_positives_hospitalized(contents):
    pattern = fr"Positive Patients: \n\n\(hospitals, state & private labs\)\n(?P<positives>{REGEX_INTEGER_WITH_COMMAS})(?:(?: \(|; )?(?:(?P<positives_hospitalized>{REGEX_INTEGER_WITH_COMMAS}) Hospitalized; )?(?P<positives_icu>{REGEX_INTEGER_WITH_COMMAS}) in ICU\)?)?"
    match = re.search(pattern, contents)
    if match.group("positives_hospitalized"):
        return int_or_none(match.group("positives_hospitalized"))
    else:
        return False


def extract_c19_pui_hospital(contents):
    pattern = fr"Persons Under Investigation \nin Hospital: (?P<hospital>{REGEX_INTEGER_WITH_COMMAS})(?:(?: \(|; )?(?P<icu>{REGEX_INTEGER_WITH_COMMAS}) in ICU\)?)?"
    match = re.search(pattern, contents)
    if match and match.group("hospital"):
        return int_or_none(match.group("hospital"))
    else:
        return False


def extract_c19_pui_icu(contents):
    pattern = fr"Persons Under Investigation \nin Hospital: (?P<hospital>{REGEX_INTEGER_WITH_COMMAS})(?:(?: \(|; )?(?P<icu>{REGEX_INTEGER_WITH_COMMAS}) in ICU\)?)?"
    match = re.search(pattern, contents)
    if match and match.group("icu"):
        return int_or_none(match.group("icu"))
    else:
        return False


def extract_c19_self_quarantine(contents):
    pattern = fr"Persons in self-quarantine: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_testing_supplies(contents):
    pattern = fr"COVID-19 Testing(?:\*)?\s*\nSupplies Availability: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_hospital_reporting_compliance(contents):
    pattern = fr"Hospital\s*Reporting\s*Compliance:\s*(\d+)%"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_positives_osdh_lab(contents):
    pattern = fr"OSDH Public\s*Health Lab: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_positives_dlo(contents):
    pattern = fr"Diagnostic Laboratory\s*of Oklahoma: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


def extract_c19_positives_other_labs(contents):
    pattern = fr"Other\s*Labs: ({REGEX_INTEGER_WITH_COMMAS})"
    match = re.search(pattern, contents)
    if match:
        return int_or_none(match.group(1))
    else:
        return False


if __name__ == "__main__":
    main()
