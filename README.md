Salesforce Extractor
=============

1. No state store
2. No Prometheus metrics
3. Added extraction pipeline in config

## Prerequisites

- Poetry

## ToDo

- Install / update dependent Python packages

```
poetry install
```

or

```
poetry update
```

## configure .env

### Cognite Data Fusion credential
- `COGNITE_PROJECT`
- `COGNITE_TOKEN_URL`
- `COGNITE_CLIENT_ID`
- `COGNITE_CLIENT_SECRET`
- `COGNITE_BASE_URL` (can be omitted if your project is hosted at `https://api.cognitedata.com`)

### Salesforce.com credential and Query String
- `SFDC_USERNAME`
- `SFDC_PASSWORD`
- `SFDC_SECURITY_TOKEN`
- `SFDC_QUERY_STRING`

### CDF RAW DB & tabel name
 
- `DESTINATION_DB`
- `DESTINATION_TABLE`

## Run the extractor

```
poetry run salesforce_extractor
```
