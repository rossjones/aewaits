import requests
import requests_cache

from lxml.html import fromstring 

requests_cache.install_cache('scrape-cache', expire_after=240)

def fetch_data():
    page = requests.get('http://www.choosewellwales.org.uk/aewaits')
    content = page.content 

    result = []

    doc = fromstring(content)
    for row in doc.cssselect('.hosp-row'):
        record = {}
        record['hospital'] = row.cssselect('h3.text-gray')[0].text 
        record['is_open'] = len(row.cssselect('.row_closed')) == 0

        if record['is_open']:
            record['waiting_time'] = row.cssselect('div.col-xs-11.col-sm-11 div.row div.col-xs-12.col-sm-4 div.row.clearfix div.col-xs-12.col-sm-12 span.aevaluebig')[0].text 
            record['current_patients'] = row.cssselect('div.col-xs-11.col-sm-11 div.row div.col-xs-12.col-sm-4.hosp-col-patient div.clearfix.aevalue div.clearfix')[0].text 
            if record['current_patients'] != 'No data':
                record['current_patients'] = record['current_patients'].split(' ')[0]
            else:
                record['current_patients'] = ''
            record['busier_than_usual'] = len(row.cssselect('.text-danger')) > 0
        else:
            record['waiting_time'] = ''
            record['current_patients'] = 0
            record['busier_than_usual'] = False 

        result.append(record)

    return result 
