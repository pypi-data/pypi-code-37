# TR-J1 Journal Requests (excluding OA Gold)
#   “Total_Item_Requests”, “Unique_Item_Requests”
# TR-J3 Journal Usage By Access Type
#   “Total_Item_Investigations”, “Unique_Item_Investigations”
#   “Total_Item_Requests”, “Unique_Item_Requests”
# IR-A1 Journal article requests
#   “Total_Item_Requests”, Unique_Items_Requests
import copy
import csv
import datetime
import json

from dateutil import (
    rrule,
    relativedelta,
)
from collections import OrderedDict
from typing import (
    List,
    Optional,
    Callable,
    NamedTuple,
    Dict,
    IO,
    Tuple,
    Any,
)

SEP = '; '

REPORT_NAMES = {
    'TR_J1': 'Journal Requests (Excluding OA_Gold)',
    'TR_J3': 'Journal Usage by Access Type',
    'IR_A1': 'Journal Article Requests',
}

SearchFunction = Callable[[dict], dict]


class StandardViewParams(NamedTuple):
    """Params for all standard views (eg: TR_J1, TR_J3), master reports will need more
    parameters. """
    search: SearchFunction
    created: datetime.datetime
    created_by: str
    begin_date: datetime.date
    end_date: datetime.date
    customer_id: str
    customer_name: str
    platform: str
    with_breakdown_by_month: bool


class MonthCount(NamedTuple):
    month: datetime.date
    count: int


class QueryResultData(NamedTuple):
    total_count: int
    top_event: dict
    by_month: Optional[List[MonthCount]]


class ReportException(NamedTuple):
    Code: int
    Severity: str
    Message: str
    Data: str


class ReportHeader(NamedTuple):
    Created: datetime.date
    Created_By: str
    Report_ID: str
    Report_Name: str
    Institution_Name: str
    Institution_ID: str
    Metric_Types: List[str]
    Report_Filters: List[Tuple[str, str]]
    Report_Attributes: List[Tuple[str, str]]
    Begin_Date: datetime.date
    End_Date: datetime.date
    Release: str = '5'
    Exceptions: List[ReportException] = []


class QueryResults(NamedTuple):
    header: ReportHeader
    results_data: List[QueryResultData]


def fast_copy(d: dict) -> dict:
    return json.loads(json.dumps(d))


def extract_result_data(bucket: dict) -> QueryResultData:
    if 'hits_over_months' in bucket:
        hits_over_months = bucket['hits_over_months']['buckets']
        by_month = []
        for month_bucket in hits_over_months:
            month_as_date = parse_r5_date(month_bucket['key_as_string'])
            hits_by_month = MonthCount(
                month=month_as_date.date(),
                count=month_bucket['doc_count']
            )
            by_month.append(hits_by_month)
    else:
        by_month = None

    return QueryResultData(
        total_count=bucket['doc_count'],
        top_event=bucket['event_top_hit']['hits']['hits'][0]['_source'],
        by_month=by_month
    )


def parse_r5_date(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def format_date(d: datetime.date):
    return d.strftime('%Y-%m-%d')


def make_exception_message(exception):
    message = f'{exception.Code}: {exception.Message}'
    if exception.Data:
        message += f' ({exception.Data})'
    return message


class CounterReportException(Exception):
    def __init__(self, header: ReportHeader, exception: ReportException):
        self.header = header._replace(Exceptions=header.Exceptions + [exception])
        super().__init__(make_exception_message(exception))


def get_counter_report_data(search: SearchFunction, header: ReportHeader,
                            query_body: dict) -> Tuple[ReportHeader, dict]:
    if header.End_Date <= header.Begin_Date:
        raise CounterReportException(
            header, ReportException(3020, 'Error', 'Invalid date arguments',
                                    f'Begin_Date={header.Begin_Date};End_Date={header.End_Date}'))
    try:
        results = search(query_body)
    except ConnectionError as e:
        raise CounterReportException(
            header, ReportException(1000, 'Fatal', 'Service unavailable', str(e)))
    if results['hits']['total'] == 0:
        raise CounterReportException(
            header, ReportException(3030, 'Error', 'No Usage Available for Requested Dates',
                                    f'Begin_Date={header.Begin_Date};End_Date={header.End_Date}'))
    return header, results


def list_months_fields(begin_date: datetime.date, end_date: datetime.date) -> List[str]:
    first_day_of_first_month = begin_date.replace(day=1)
    month_dates = []
    for month_date in rrule.rrule(rrule.MONTHLY, first_day_of_first_month, until=end_date):
        month_dates.append((month_date.month, month_date.year))
    return [f'{MONTHS[month_number - 1]}-{year}' for month_number, year in month_dates]


def make_report_header(params: StandardViewParams, report_id: str, report_name: str,
                       metric_types: List[str],
                       report_filters: List[Tuple[str, str]]) -> ReportHeader:
    return ReportHeader(
        Created=params.created,
        Created_By=params.created_by,
        Report_ID=report_id,
        Report_Name=report_name,
        Institution_Name=params.customer_name,
        Institution_ID=f'{params.platform}:{params.customer_id}',
        Metric_Types=metric_types,
        Report_Filters=report_filters,
        Report_Attributes=[],
        Begin_Date=params.begin_date,
        End_Date=params.end_date,
    )


def get_tr_j1_field_names(params: StandardViewParams) -> List[str]:
    field_names = [
        'Title', 'Publisher', 'Publisher_ID', 'Platform', 'Proprietary_ID', 'Print_ISSN',
        'Online_ISSN', 'URI', 'Metric_Type', 'Reporting_Period_Total'
    ]
    if params.with_breakdown_by_month:
        field_names.extend(list_months_fields(params.begin_date, params.end_date))
    return field_names


def get_ir_a1_field_names(params: StandardViewParams) -> List[str]:
    field_names = [
        'Item', 'Publisher', 'Publisher_ID', 'Platform', 'Authors', 'Publication_Date',
        'Article_Version', 'DOI', 'Proprietary_ID', 'Print_ISSN', 'Online_ISSN', 'URI',
        'Parent_Title', 'Parent_Authors', 'Parent_Article_Version', 'Parent_DOI',
        'Parent_Proprietary_ID', 'Parent_Print_ISSN', 'Parent_Online_ISSN', 'Parent_URI',
        'Access_Type', 'Metric_Type', 'Reporting_Period_Total'
    ]
    if params.with_breakdown_by_month:
        field_names.extend(list_months_fields(params.begin_date, params.end_date))
    return field_names


def get_tr_j3_field_names(params: StandardViewParams) -> List[str]:
    field_names = [
        'Title', 'Publisher', 'Publisher_ID', 'Platform', 'DOI', 'Proprietary_ID', 'Print_ISSN',
        'Online_ISSN', 'URI', 'Access_Type', 'Metric_Type', 'Reporting_Period_Total']
    if params.with_breakdown_by_month:
        field_names.extend(list_months_fields(params.begin_date, params.end_date))
    return field_names


def get_composite_query_results_data(params: StandardViewParams, query_body: dict, report_id: str,
                                     report_name: str, metric_types: List[str],
                                     report_filters: List[Tuple[str, str]]):
    header = make_report_header(params, report_id, report_name, metric_types, report_filters)
    empty_result_set = False
    all_result_data = []
    after_key = None
    while not empty_result_set:
        if after_key:
            query_body = copy.deepcopy(query_body)
            query_body['aggs']['composite_agg']['composite']['after'] = after_key
        header, result = get_counter_report_data(params.search, header, query_body)
        after_key, result_data = extract_result_data_from_composite_elasticsearch_result(result)
        all_result_data.extend(result_data)
        empty_result_set = after_key is None

    return QueryResults(header, all_result_data)


def get_tr_j1_data(params: StandardViewParams) -> QueryResults:
    query_body = get_tr_j1_query(params)
    return get_composite_query_results_data(
        params, query_body, 'TR_J1', REPORT_NAMES['TR_J1'],
        ['Total_Item_Requests', 'Unique_Item_Requests'],
        [('Data_Type', 'Journal'), ('Access_Type', 'Controlled'), ('Access_Method', 'Regular')]
    )


def get_ir_a1_data(params: StandardViewParams) -> QueryResults:
    query_body = get_ir_a1_query(params)
    return get_composite_query_results_data(
        params, query_body, 'IR_A1', REPORT_NAMES['IR_A1'],
        ['Total_Item_Requests', 'Unique_Item_Requests'],
        [('Data_Type', 'Article'), ('Parent_Data_Type', 'Journal'), ('Access_Method', 'Regular')])


def get_tr_j3_data(params: StandardViewParams) -> QueryResults:
    query_body = get_tr_j3_query(params)
    return get_composite_query_results_data(
        params, query_body, 'TR_J3', REPORT_NAMES['TR_J3'],
        ['Total_Item_Requests', 'Unique_Item_Requests', 'Total_Item_Investigations',
         'Unique_Item_Investigations'],
        [('Data_Type', 'Journal'), ('Access_Method', 'Regular')])


def get_tr_j1_query(params: StandardViewParams) -> dict:
    query_body = make_composite_aggregation(['is_unique', 'parent_proprietary_id'],
                                            params.with_breakdown_by_month)
    add_bool_clauses(query_body, params, [("access_type", "Controlled"),
                                          ("is_request", True)])
    return query_body


def get_ir_a1_query(params: StandardViewParams) -> dict:
    query_body = make_composite_aggregation(['proprietary_id', 'is_unique', 'access_type'],
                                            with_breakdown_by_month=params.with_breakdown_by_month)
    add_bool_clauses(query_body, params, [("is_request", True)])
    return query_body


def get_tr_j3_query(params: StandardViewParams) -> dict:
    query_body = make_composite_aggregation(
        ["parent_proprietary_id", "is_unique", "access_type", "is_request"],
        params.with_breakdown_by_month)
    add_bool_clauses(query_body, params)
    return query_body


def extract_result_data_from_composite_elasticsearch_result(
        query_result: dict) -> Tuple[dict, List[QueryResultData]]:
    aggregations = query_result['aggregations']['composite_agg']
    buckets = aggregations['buckets']
    # if buckets are empty (ie. no more data), after_key is absent
    after_key = aggregations.get('after_key', None)
    return after_key, [extract_result_data(bucket) for bucket in buckets]


def date_range(begin_date: datetime.date, end_date: datetime.date) -> dict:
    begin_date_str = format_date(begin_date)
    end_date_str = format_date(end_date)
    date_format = 'yyyy-MM-dd'
    return {'range': {'timestamp': {'gte': begin_date_str,
                                    'lt': end_date_str,
                                    'format': date_format}}}


def add_bool_clauses(query_body: dict, params: StandardViewParams,
                     additional_terms: List[Tuple[str, Any]] = None) -> None:
    query_body['size'] = 0
    query_body['query'] = {'bool': {'must': []}}
    must_clauses = query_body['query']['bool']['must']
    must_clauses.append(date_range(params.begin_date, params.end_date))
    must_clauses.extend([
        {'term': {"institution_identifiers.value": params.customer_id}},
        {'term': {"institution_identifiers.type": "Proprietary"}},
        {'term': {"platform": params.platform}},
        {'term': {"is_double_click": False}},
    ])
    if additional_terms:
        for term in additional_terms:
            must_clauses.append({'term': {term[0]: term[1]}})


def get_last_aggs(with_breakdown_by_month: bool) -> dict:
    aggs = {
        "event_top_hit": {
            "top_hits": {
                "sort": [
                    {
                        "timestamp": {
                            "order": "desc"
                        }
                    }
                ],
                "size": 1
            }
        },
    }
    if with_breakdown_by_month:
        aggs["hits_over_months"] = {
            "date_histogram": {
                "field": "timestamp",
                "interval": "month",
                "format": "yyyy-MM-dd"
            }
        }
    return aggs


def make_composite_aggregation(fields: List[str], with_breakdown_by_month: bool) -> dict:
    sources = [{f: {"terms": {"field": f}}} for f in fields]
    aggs = {
        "aggs": {
            "composite_agg": {
                "composite": {
                    "size": 1000,
                    "sources": sources
                },
                "aggregations": get_last_aggs(with_breakdown_by_month)
            }
        }
    }
    return aggs


def publisher_ids_to_str(event: dict) -> str:
    publisher_identifiers = event.get('publisher_identifiers', [])
    publisher_ids = []
    for pub_id in publisher_identifiers:
        pub_id_type = pub_id['type']
        if pub_id_type == 'Proprietary':
            pub_id_type = event['platform']
        publisher_ids.append(f"{pub_id_type}:{pub_id['value']}")
    publisher_ids_str = SEP.join(publisher_ids)
    return publisher_ids_str


def extract_identifier(identifiers: List[Dict[str, str]], id_type: str, default: str = None) -> str:
    ids_dict = {d['type']: d['value'] for d in identifiers}
    if default is None:
        return ids_dict[id_type]
    else:
        return ids_dict.get(id_type, default)


MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def extract_stats_by_month(by_month: List[MonthCount]) -> OrderedDict:
    if not by_month:
        return OrderedDict()
    stats_by_month = OrderedDict()
    for month_count in by_month:
        month_number = month_count.month.month
        year = month_count.month.year
        month_str = MONTHS[month_number - 1]
        stats_by_month[f'{month_str}-{year}'] = month_count.count
    return stats_by_month


def tr_j1_query_results_data_to_csv_rows(results: List[QueryResultData]) -> List[OrderedDict]:
    items = []
    for result in results:
        event = result.top_event
        is_unique = event['is_unique']
        metric_type = "Unique_Item_Requests" if is_unique else "Total_Item_Requests"
        item = OrderedDict(
            Title=event['parent_title'],
            Publisher=event['publisher_name'],
            Publisher_ID=publisher_ids_to_str(event),
            Platform=event['platform'],
            Proprietary_ID=f"{event['platform']}:{event['parent_proprietary_id']}",
            Print_ISSN=extract_identifier(event['parent_item_identifiers'], 'Print_ISSN', ''),
            Online_ISSN=extract_identifier(event['parent_item_identifiers'], 'Online_ISSN'),
            URI=event['parent_uri'],
            Metric_Type=metric_type,
            Reporting_Period_Total=result.total_count,
        )
        item.update(extract_stats_by_month(result.by_month))
        items.append(item)
    return items


def format_contributors(contributors: List[dict]) -> str:
    return SEP.join([f'{c["name"]}({c["identifier"]})' for c in contributors])


def ir_a1_query_results_data_to_csv_rows(results: List[QueryResultData]) -> List[OrderedDict]:
    items = []
    for result in results:
        event = result.top_event
        is_unique = event['is_unique']
        metric_type = "Unique_Item_Requests" if is_unique else "Total_Item_Requests"
        authors = format_contributors(event.get('item_contributors', []))
        parent_authors = format_contributors(event.get('parent_item_contributors', []))
        item = OrderedDict(
            Item=event['title'],
            Publisher=event['publisher_name'],
            Publisher_ID=publisher_ids_to_str(event),
            Platform=event['platform'],
            Authors=authors,
            Publication_Date=event['publication_date'],
            Article_Version='VoR',  # event['article_version'],
            DOI=event.get('doi', ''),
            Proprietary_ID=f"{event['platform']}:{event['proprietary_id']}",
            Print_ISSN=extract_identifier(event['item_identifiers'], 'Print_ISSN', ''),
            Online_ISSN=extract_identifier(event['item_identifiers'], 'Online_ISSN', ''),
            URI=event['uri'],
            Parent_Title=event['parent_title'],
            Parent_Authors=parent_authors,
            Parent_Article_Version='VoR',
            Parent_DOI=event.get('parent_doi', ''),
            Parent_Proprietary_ID=event['parent_proprietary_id'],
            Parent_Print_ISSN=extract_identifier(
                event['parent_item_identifiers'], 'Print_ISSN', ''),
            Parent_Online_ISSN=extract_identifier(event['parent_item_identifiers'], 'Online_ISSN',
                                                  ''),
            Parent_URI=event['parent_uri'],
            Access_Type=event['access_type'],
            Metric_Type=metric_type,
            Reporting_Period_Total=result.total_count,
        )
        item.update(extract_stats_by_month(result.by_month))
        items.append(item)
    return items


def tr_j3_query_results_data_to_csv_rows(results: List[QueryResultData]) -> List[OrderedDict]:
    items = []
    for result in results:
        event = result.top_event
        metric_type = get_metric_type(event)
        item = OrderedDict(
            Title=event['parent_title'],
            Publisher=event['publisher_name'],
            Publisher_ID=publisher_ids_to_str(event),
            Platform=event['platform'],
            DOI=event.get('doi', ''),
            Proprietary_ID=f"{event['platform']}:{event['parent_proprietary_id']}",
            Print_ISSN=extract_identifier(event['parent_item_identifiers'], 'Print_ISSN', ''),
            Online_ISSN=extract_identifier(event['parent_item_identifiers'], 'Online_ISSN', ''),
            URI=event['parent_uri'],
            Access_Type=event['access_type'],
            Metric_Type=metric_type,
            Reporting_Period_Total=result.total_count,
        )
        item.update(extract_stats_by_month(result.by_month))
        items.append(item)
    return items


def get_metric_type(event):
    is_unique = event['is_unique']
    is_request = event['is_request']
    if is_request:
        metric_type = "Unique_Item_Requests" if is_unique else "Total_Item_Requests"
    else:
        metric_type = "Unique_Item_Investigations" if is_unique else "Total_Item_Investigations"
    return metric_type


def typed_values_to_str(values: List[Tuple[str, str]]) -> str:
    return SEP.join(f'{t}={v}' for t, v in values)


def write_csv_header(csv_writer, header: ReportHeader) -> None:
    exceptions = SEP.join([make_exception_message(e) for e in header.Exceptions])
    reporting_period = [('Begin_Date', format_date(header.Begin_Date)),
                        ('End_Date', format_date(header.End_Date))]
    csv_writer.writerow(['Report_Name', header.Report_Name])
    csv_writer.writerow(['Report_ID', header.Report_ID])
    csv_writer.writerow(['Release', header.Release])
    csv_writer.writerow(['Institution_Name', header.Institution_Name])
    csv_writer.writerow(['Institution_ID', header.Institution_ID])
    csv_writer.writerow(['Metric_Types', SEP.join(header.Metric_Types)])
    csv_writer.writerow(['Report_Filters', typed_values_to_str(header.Report_Filters)])
    csv_writer.writerow(['Report_Attributes', typed_values_to_str(header.Report_Attributes)])
    csv_writer.writerow(['Exceptions', exceptions])
    csv_writer.writerow(['Reporting_Period', typed_values_to_str(reporting_period)])
    # noinspection PyArgumentList
    csv_writer.writerow(['Created', header.Created.isoformat(timespec='seconds') + 'Z'])
    csv_writer.writerow(['Created_By', header.Created_By])


def write_counter_csv(f: IO[str], header: ReportHeader, field_names: List[str],
                      rows: List[OrderedDict]) -> None:
    header_writer = csv.writer(f, 'excel')
    write_csv_header(header_writer, header)
    header_writer.writerow([])
    rows_writer = csv.DictWriter(f, field_names, dialect='excel')
    rows_writer.writeheader()
    rows_writer.writerows(rows)


def make_tr_j1_csv(f: IO[str], params: StandardViewParams) -> None:
    field_names = get_tr_j1_field_names(params)
    results = get_tr_j1_data(params)
    rows = tr_j1_query_results_data_to_csv_rows(results.results_data)
    write_counter_csv(f, results.header, field_names, rows)


def make_ir_a1_csv(f: IO[str], params: StandardViewParams) -> None:
    field_names = get_ir_a1_field_names(params)
    results = get_ir_a1_data(params)
    rows = ir_a1_query_results_data_to_csv_rows(results.results_data)
    write_counter_csv(f, results.header, field_names, rows)


def make_tr_j3_csv(f: IO[str], params: StandardViewParams) -> None:
    field_names = get_tr_j3_field_names(params)
    results = get_tr_j3_data(params)
    rows = tr_j3_query_results_data_to_csv_rows(results.results_data)
    write_counter_csv(f, results.header, field_names, rows)


def make_csv_report(report_code: str, f: IO[str], params: StandardViewParams) -> None:
    try:
        if report_code == 'TR_J1':
            make_tr_j1_csv(f, params)
        elif report_code == 'IR_A1':
            make_ir_a1_csv(f, params)
        elif report_code == 'TR_J3':
            make_tr_j3_csv(f, params)
        else:
            header = make_report_header(params, report_code, '', [], [])
            raise CounterReportException(header, ReportException(3000, 'Error',
                                                                 'Report Not Supported', ''))
    except CounterReportException as e:
        header_writer = csv.writer(f, 'excel')
        write_csv_header(header_writer, e.header)


def report_header_to_sushi(header: ReportHeader) -> dict:
    sushi_header = {
        'Created': header.Created.isoformat() + 'Z',
        'Created_By': header.Created_By,
        'Report_ID': header.Report_ID,
        'Report_Name': header.Report_Name,
        'Release': header.Release,
        'Institution_Name': header.Institution_Name,
        'Report_Filters': [{'Name': 'Begin_Date', 'Value': format_date(header.Begin_Date)},
                           {'Name': 'End_Date', 'Value': format_date(header.End_Date)}],
    }
    if header.Exceptions:
        sushi_header['Exceptions'] = []
        for exception in header.Exceptions:
            except_dict = {
                'Code': exception.Code,
                'Severity': exception.Severity,
                'Message': exception.Message,
            }
            if exception.Data:
                except_dict['Data'] = exception.Data
            sushi_header['Exceptions'].append(except_dict)
    return sushi_header


def sushi_period(begin_date: datetime.date, end_date: datetime.date) -> dict:
    return {'Begin_Date': format_date(begin_date), 'End_Date': format_date(end_date)}


def capitalize_keys(dicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result_dicts = []
    for d in dicts:
        capitalized_dict = {}
        for key, value in d.items():
            capitalized_key = '_'.join(w.capitalize() for w in key.split('_'))
            capitalized_dict[capitalized_key] = value
        result_dicts.append(capitalized_dict)
    return result_dicts


def make_sushi_performance(begin_date, end_date, metric_type, total):
    return {'Period': sushi_period(begin_date, end_date),
            'Instance': [{'Metric_Type': metric_type, 'Count': total}]}


def month_counts_to_performance(by_month: Optional[List[MonthCount]],
                                metric_type: str) -> List[Dict[str, Any]]:
    performance = []
    if by_month:
        months = [month for month in by_month if month.count]
        for month in months:
            first_day = month.month
            last_day = month.month + relativedelta.relativedelta(months=1, days=-1)
            performance.append(
                make_sushi_performance(first_day, last_day, metric_type, month.count))
    return performance


def result_data_to_sushi_title_usage(begin_date: datetime.date, end_date: datetime.date,
                                     result_data: QueryResultData) -> Tuple[str, dict]:
    """Return a tuple of (title id, title_usage) where title_usage is a dict that conforms to
    COUNTER_title_usage in the COUNTER_SUSHI schema.
    """
    event = result_data.top_event
    total = result_data.total_count
    metric_type = get_metric_type(event)
    performance = [make_sushi_performance(begin_date, end_date, metric_type, total)]
    performance.extend(month_counts_to_performance(result_data.by_month, metric_type))
    title_usage = {
        'Title': event['parent_title'],
        'Item_ID': capitalize_keys(event['parent_item_identifiers']),
        'Platform': event['platform'],
        'Publisher': event['publisher_name'],
        'Publisher_ID': capitalize_keys(event['publisher_identifiers']),
        'Data_Type': 'Journal',
        'Section_Type': 'Article',
        'Access_Type': event['access_type'],
        'Access_Method': event['access_method'],
        'Performance': performance,
    }
    if 'year_of_publication' in event:
        title_usage['YOP'] = event['year_of_publication']

    return event['parent_proprietary_id'], title_usage


def result_data_to_sushi_item_usage(begin_date: datetime.date, end_date: datetime.date,
                                    result_data: QueryResultData) -> Tuple[str, dict]:
    """Return a tuple of (title id, title_usage) where title_usage is a dict that conforms to
    COUNTER_title_usage in the COUNTER_SUSHI schema.
    """
    event = result_data.top_event
    total = result_data.total_count
    metric_type = get_metric_type(event)
    performance = [
        make_sushi_performance(begin_date, end_date, metric_type, total)
    ]
    performance.extend(month_counts_to_performance(result_data.by_month, metric_type))
    item_usage = {
        'Item': event['title'] or '-',
        'Item_ID': capitalize_keys(event['item_identifiers']),
        'Item_Contributors': capitalize_keys(event['item_contributors']),
        'Item_Dates': [{'Type': 'Publication_Date', 'Value': event['publication_date']}],
        'Platform': event['platform'],
        'Publisher': event['publisher_name'],
        'Publisher_ID': capitalize_keys(event['publisher_identifiers']),
        'Item_Parent': [{
            'Item_ID': capitalize_keys(event['parent_item_identifiers']),
            'Item_Name': event['parent_title'],
            'Data_Type': 'Journal',
        }],
        'Data_Type': 'Article',
        'Access_Type': event['access_type'],
        'Access_Method': event['access_method'],
        'Performance': performance,
    }
    if 'year_of_publication' in event:
        item_usage['YOP'] = event['year_of_publication']

    return event['proprietary_id'], item_usage


def period_key(performance: dict) -> Tuple[str, str]:
    period = performance['Period']
    return period['Begin_Date'], period['End_Date']


def merge_performances(list1: List[Dict], list2: List[dict]) -> List[Dict]:
    by_period = {period_key(performance): fast_copy(performance) for performance in list1}
    for performance_to_add in list2:
        key = period_key(performance_to_add)
        try:
            performance = by_period[key]
        except KeyError:
            by_period[key] = fast_copy(performance_to_add)
            continue
        instances = performance['Instance']
        for i in performance_to_add['Instance']:
            if i not in instances:
                instances.append(i)
    return list(by_period.values())


def group_performances_by_id(flat_title_usages: List[Tuple[str, dict]]) -> List[Dict]:
    grouped = {}
    for item_id, usage in flat_title_usages:
        try:
            append_to = grouped[item_id]
        except KeyError:
            grouped[item_id] = fast_copy(usage)
            continue
        append_to['Performance'] = merge_performances(append_to['Performance'],
                                                      usage['Performance'])
    return list(grouped.values())


SushiUsageMappingFunction = Callable[[datetime.date, datetime.date, QueryResultData],
                                     Tuple[str, dict]]


def query_results_data_to_sushi(results: QueryResults,
                                mapping_function: SushiUsageMappingFunction) -> dict:
    header = report_header_to_sushi(results.header)
    # this gives a flat list of usages (csv-like)
    flat_title_usages = [mapping_function(results.header.Begin_Date,
                                          results.header.End_Date, result_data)
                         for result_data in results.results_data]
    # but COUNTER_SUSHI requires that results are grouped by ID, with all metric types count
    # in the performance field
    title_usages = group_performances_by_id(flat_title_usages)
    return {
        'Report_Header': header,
        'Report_Items': title_usages,
    }


def make_tr_j1_sushi(params: StandardViewParams) -> dict:
    results = get_tr_j1_data(params)
    return query_results_data_to_sushi(results, result_data_to_sushi_title_usage)


def make_tr_j3_sushi(params: StandardViewParams) -> dict:
    results = get_tr_j3_data(params)
    return query_results_data_to_sushi(results, result_data_to_sushi_title_usage)


def make_ir_a1_sushi(params: StandardViewParams) -> dict:
    results = get_ir_a1_data(params)
    return query_results_data_to_sushi(results, result_data_to_sushi_item_usage)


def get_report_as_sushi_data(report_code: str, params: StandardViewParams) -> Dict[str, Any]:
    try:
        if report_code == 'TR_J1':
            data = make_tr_j1_sushi(params)
        elif report_code == 'IR_A1':
            data = make_ir_a1_sushi(params)
        elif report_code == 'TR_J3':
            data = make_tr_j3_sushi(params)
        else:
            header = make_report_header(params, report_code, '', [], [])
            raise CounterReportException(header, ReportException(3000, 'Error',
                                                                 'Report Not Supported', ''))
        return data

    except CounterReportException as e:
        sushi_header = report_header_to_sushi(e.header)
        return {'Report_Header': sushi_header, 'Report_Items': []}


def get_error_response_as_sushi(params: StandardViewParams, report_id: str,
                                exception: ReportException) -> dict:
    report_name = REPORT_NAMES[report_id]
    header = make_report_header(params, report_id, report_name, [], [])
    header = header._replace(Exceptions=[exception])
    sushi_header = report_header_to_sushi(header)
    return {'Report_Header': sushi_header, 'Report_Items': []}