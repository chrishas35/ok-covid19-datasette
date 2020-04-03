from extract_utils import *


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    db = sqlite_utils.Database("ok-covid19.db")

    table = db["occupancy_stats"]
    if table.exists():
        table.drop()
    table.insert_all(load_occupancy_stats(), pk="date")

    # TODO: Add the non-EO stats (news, homepage) to give history and upsert with EO
    table = db["case_stats"]
    if table.exists():
        table.drop()
    table.insert_all(load_case_stats(), pk="date")


def extract_occupancy_stats(pdf):
    logging.info(f"Extracting occupancy stats from {pdf}...")
    contents = get_contents(pdf)

    document = dict()
    document["date"] = parse(extract_c19_report_date(contents)).strftime("%Y-%m-%d")
    document[
        "hospital_reporting_compliance"
    ] = extract_c19_hospital_reporting_compliance(contents)
    (
        document["icu_beds_numerator"],
        document["icu_beds_denominator"],
        document["icu_beds_percentage"],
    ) = extract_c19_icu_beds(contents)

    (
        document["medical_surgery_beds_numerator"],
        document["medical_surgery_beds_denominator"],
        document["medical_surgery_beds_percentage"],
    ) = extract_c19_med_surg_beds(contents)

    (
        document["operating_room_beds_numerator"],
        document["operating_room_beds_denominator"],
        document["operating_room_beds_percentage"],
    ) = extract_c19_or_beds(contents)

    (
        document["pediatric_beds_numerator"],
        document["pediatric_beds_denominator"],
        document["pediatric_beds_percentage"],
    ) = extract_c19_peds_beds(contents)

    (
        document["picu_beds_numerator"],
        document["picu_beds_denominator"],
        document["picu_beds_percentage"],
    ) = extract_c19_picu_beds(contents)

    document["ventilators"] = extract_c19_ventilators(contents)

    (
        document["negative_flow_rooms_numerator"],
        document["negative_flow_rooms_denominator"],
        document["negative_flow_rooms_percentage"],
    ) = extract_c19_neg_flow_rooms(contents)

    document["overall_hospital_occupancy_status"] = extract_c19_occupancy(contents)

    return document


def extract_case_stats(pdf):
    logging.info(f"Extracting case stats from {pdf}...")
    contents = get_contents(pdf)

    document = dict()
    document["date"] = parse(extract_c19_report_date(contents)).strftime("%Y-%m-%d")

    document["positive_patients_all"] = extract_c19_positives(contents)
    document["positive_patients_hospitalized"] = extract_c19_positives_hospitalized(
        contents
    )
    document["positive_patients_in_icu"] = extract_c19_positives_icu(contents)

    document["persons_under_investigation_in_hospital"] = extract_c19_pui_hospital(
        contents
    )
    document["persons_under_investigation_in_icu"] = extract_c19_pui_icu(contents)
    document["persons_in_self_quarantine"] = extract_c19_self_quarantine(contents)

    document["positive_cases_by_lab_osdh"] = extract_c19_positives_osdh_lab(contents)
    document["positive_cases_by_lab_dlo"] = extract_c19_positives_dlo(contents)
    document["positive_cases_by_lab_other"] = extract_c19_positives_other_labs(contents)

    return document


def load_occupancy_stats():
    for pdf in glob("data/pdfs/*covid-19_report*.pdf"):
        yield extract_occupancy_stats(pdf)


def load_case_stats():
    for pdf in glob("data/pdfs/*covid-19_report*.pdf"):
        yield extract_case_stats(pdf)


if __name__ == "__main__":
    main()
