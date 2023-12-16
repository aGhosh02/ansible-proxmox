import requests

headers = {
    "X-Api-Key": "8be13f8473ac4344b7f038d94ee9fbaf"
}

# API endpoint URL
indexer_status = "http://10.0.200.2:9696/api/v1/indexerStatus"
get_indexer = "http://10.0.200.2:9696/api/v1/indexer/{}"
get_urls = "http://10.0.200.2:9696/api/v1/indexer/action/getUrls"
test_indexer = "http://10.0.200.2:9696/api/v1/indexer/test"

# Get all errored indexers
error_indexers = requests.get(indexer_status, headers=headers)

for error_indexer in error_indexers.json():

    # Get indexer details
    indexer_details_url = get_indexer.format(error_indexer["indexerId"])
    indexer = requests.get(indexer_details_url, headers=headers).json()
    urls = requests.post(get_urls, json=indexer, headers=headers).json()

    is_fixed = False
    i = 0

    while len(urls["options"]) > i and not is_fixed:

        url = urls["options"][i]

        # Update new url
        for field in indexer["fields"]:
            if field['name'] == 'baseUrl':
                field['value'] = url['value']

        # Test new url
        try:
            print('[{0}] : Testing {1} \n'.format(
                indexer["name"], url))

            test_result = requests.post(
                test_indexer, json=indexer, headers=headers)

            if test_result.status_code == 200:
                is_fixed = True
                result = requests.put(indexer_details_url,
                                      json=indexer, headers=headers)
                print('[{0}] : Using {1} , Result {2} \n'.format(
                    indexer["name"], url, result.status_code))
        except:
            pass
        i = i+1

    if not is_fixed:
        print('[{0}] : Not Fixed \n'.format(indexer["name"]))
