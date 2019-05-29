import csv
from collections import defaultdict

from lazyme import per_chunk

def convert_types(string):
    try:
        return float(value.replace(',', '').replace('%', '').replace('"', ''))
    except:
        return string

def similarweb_parser(filename):
    country_datapoint_domain = defaultdict(lambda: defaultdict(dict))
    with open(filename) as fin:
        # Skip the first 13 lines.
        for _ in range(13):
            next(fin)
        # This the header line with the column names.
        headers = next(fin)

        # Iterating through each domain/site.
        for domain_data in per_chunk(fin, n=7):
            first_row = domain_data[0]
            top_of_countries, domain, data_point, *countries = first_row.strip().split('\t')
            for row in domain_data[1:]:
                data_point, *values  = row.strip().split('\t')
                _, data_point = domain.strip(), data_point.strip()
                for country, value in zip(countries, values):
                    country_datapoint_domain[country][data_point][domain] = convert_types(value)
    return country_datapoint_domain
