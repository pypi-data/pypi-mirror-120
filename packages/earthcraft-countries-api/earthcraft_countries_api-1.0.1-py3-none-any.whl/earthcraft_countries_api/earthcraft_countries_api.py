import json
from collections import Counter


class JsonImports:
    official_country_names = json.loads(open(r"earthcraft_countries_api\json\dicts\official_country_names.json").read())
    iso3_to_capital = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_capital.json").read())
    iso3_to_iso2 = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_iso2.json").read())
    iso2_to_iso3 = json.loads(open(r"earthcraft_countries_api\json/dicts/iso2_to_iso3.json").read())
    three_letter_iso_blank = json.loads(open(r"earthcraft_countries_api\json/dicts/three_letter_iso_blank.json").read())
    two_letter_iso_blank = json.loads(open(r"earthcraft_countries_api\json/dicts/two_letter_iso_blank.json").read())
    country_name_to_iso3 = json.loads(open(r"earthcraft_countries_api\json/dicts/country_name_to_iso3.json").read())
    iso3_to_name = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_name.json").read())
    iso3_to_calling_code = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_calling_code.json").read())
    iso3_to_borders = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_borders.json").read())
    iso3_to_un_gdp_nominal = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_un_gdp_nominal.json").read())
    iso3_to_population = json.loads(open(r"earthcraft_countries_api\json/dicts/iso3_to_population.json").read())
    countries_iso3_list = json.loads(open(r"earthcraft_countries_api\json/lists/countries_iso3_list.json").read())
    countries_iso2_list = json.loads(open(r"earthcraft_countries_api\json/lists/countries_iso2_list.json").read())
    countries_name_list = json.loads(open(r"earthcraft_countries_api\json/lists/countries_name_list.json").read())


def get_iso2_from_iso3(iso3: str):
    if JsonImports.iso3_to_iso2[iso3.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.iso3_to_iso2[iso3.upper().replace(" ", "_")]


def get_iso3_from_iso2(iso2: str):
    if JsonImports.iso2_to_iso3[iso2.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.iso2_to_iso3[iso2.upper().replace(" ", "_")]


def get_name_from_iso3(iso3: str):
    # iso3 > name
    if JsonImports.iso3_to_name[iso3.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.iso3_to_name[iso3.upper().replace(" ", "_")]


def get_iso3_from_name(name: str):
    # name > iso3
    if JsonImports.country_name_to_iso3[name.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.country_name_to_iso3[name.upper().replace(" ", "_")]


def get_capital_from_iso3(iso3: str):
    if JsonImports.iso3_to_capital[iso3.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.iso3_to_capital[iso3.upper().replace(" ", "_")]


def get_calling_code_from_iso3(iso3: str):
    if JsonImports.iso3_to_calling_code[iso3.upper().replace(" ", "_")] is None:
        return IndexError
    else:
        return JsonImports.iso3_to_calling_code[iso3.upper().replace(" ", "_")]


def get_borders_from_iso3(iso3: str):
    if JsonImports.iso3_to_borders[iso3.upper().replace(" ", "_")] is None:
        return None
    else:
        return JsonImports.iso3_to_borders[iso3.upper().replace(" ", "_")]


def get_gdp_nominal_from_iso3(iso3: str):
    if JsonImports.iso3_to_un_gdp_nominal[iso3.upper().replace(" ", "_")] is None:
        return None
    else:
        return JsonImports.iso3_to_un_gdp_nominal[iso3.upper().replace(" ", "_")]


def get_population_from_iso3(iso3: str):
    if JsonImports.iso3_to_population[iso3.upper().replace(" ", "_")] is None:
        return None
    else:
        return JsonImports.iso3_to_population[iso3.upper().replace(" ", "_")]


def get_gdp_per_capita_from_iso3(iso3: str):
    if JsonImports.iso3_to_un_gdp_nominal[iso3.upper().replace(" ", "_")] is None:
        return None
    else:
        population_var = get_population_from_iso3(iso3)
        gdp_var = get_gdp_nominal_from_iso3(iso3)
        return round(gdp_var / population_var)


def get_gdp_per_capita_descending():
    new_dict = {}
    for country in JsonImports.countries_iso3_list:
        if get_gdp_per_capita_from_iso3(country) is None:
            pass
        else:
            new_dict[country] = get_gdp_per_capita_from_iso3(country)
    c = Counter(new_dict)
    return c.most_common()


def get_country_iso3_list():
    return JsonImports.countries_iso3_list


def get_country_iso2_list():
    return JsonImports.countries_iso2_list


def get_country_name_list():
    return JsonImports.countries_name_list
