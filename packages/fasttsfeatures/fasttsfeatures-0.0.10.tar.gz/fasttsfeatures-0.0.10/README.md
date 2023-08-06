# FastTSFeatures
> Time-series feature extraction as a service. FastTSFeatures is an SDK to compute static, temporal and calendar variables as a service.


The package serves as a wrapper for [tsfresh](https://github.com/blue-yonder/tsfresh), [tsfeatures](https://github.com/Nixtla/tsfeatures) and [holidays](https://github.com/dr-prodigy/python-holidays). Since we take care of the whole infrastructure, feature extraction becomes as easy as running a line in your python nootebooks or calling an API.

## Why?

We build FastTSFeatures because we wanted an easy and fast way to extract Time Series Features without having to think about infrastructure and deployment. Now we want to see if other Data Scientists find it useful too.

## Table of contents

- [FastTSFeatures](#fasttsfeatures)
  * [Install](#install)
  * [How to use](#how-to-use)
    + [Data Format](#data-format)
    + [1. Request free trial](#1-request-free-trial)
    + [2. Run `fasttsfeatures` on a private S3 Bucket](#2-run--fasttsfeatures--on-a-private-s3-bucket)
      - [2.1 Upload to S3 from python](#21-upload-to-s3-from-python)
      - [2.2 Run the features extraction process](#22-run-the-features-extraction-process)
      - [2.3 Download your results from s3](#23-download-your-results-from-s3)

## Available Features (More than 600)

- 40+ Features: https://github.com/Nixtla/tsfeatures
- 600+ Temporal Features: https://github.com/blue-yonder/tsfresh/
- 10 Temporal Features (lags, mean lags, std_lags) [Currently just supported for daily data]
Calendar Features (distance in minutes to holidays)
- Calendar features for 83 Countries https://github.com/dr-prodigy/python-holidays


## Install

`pip install fasttsfeatures`

## How to use

You can use FastTSFeatures by either using a completely public S3 bucket or by uploading a file to your own S3 bucket provided by us.  

### Data Format

Currently we only support `.csv` files. These files must include at least 3 columns, with a unique_id (identifier of each time-series) a date stamp and a value.

### 1. Request free trial

Request a free trial sending an email to: fede.garza.ramirez@gmail.com and get your `BUCKET_NAME`, `API_ID` and `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

### 2. Run `fasttsfeatures` on a private S3 Bucket

If you don´t want other people to potentially have access to your data you can run `fasttsfeatures` on a private S3 Bucket. For that you have to upload your data to a private S3 Bucket that we will provide for you; you can do this inside of python.

#### 2.1 Upload to S3 from python

You will need the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` that we provided.


- Import and Instantiate `TSFeatures` introducing your `BUCKET_NAME`, `API_ID` and `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

```python
from fasttsfeatures.core import TSFeatures

tsfeatures = TSFeatures(bucket_name='<BUCKET_NAME>',
                        api_id='<API_ID>',
                        api_key='<API_KEY>',
                        aws_access_key_id='<AWS_ACCESS_KEY_ID>',
                        aws_secret_access_key='<AWS_SECRET_ACCESS_KEY>')
```

- Upload your local file introducing its name.

```python
s3_uri = tsfeatures.upload_to_s3(file='<YOUR FILE NAME>')
```

- Run the features extraction process

You can run temporal, static or calendar features on the data you uploaded.
To run the process specify:
- `s3_uri`: S3 uri provided after calling `tsfeatures.upload_to_s3()`.
- `freq`: Integer where  
> {'Hourly':24, 'Daily': 7, 'Monthly': 12, 'Quarterly': 4, 'Weekly':52, 'Yearly': 1}.- `ds_column`: Name of the unique id column.
- `y_column`: Name of the target column.

In the case of calendar variable you have to specify the country using the [ISO](https://pypi.org/project/holidays/) code.

```python

#Run Temporal Features
response_tmp_ft = tsfeatures.calculate_temporal_features_from_s3_uri(
                    s3_uri="<PRIVATE S3 URI HERE>",
                    freq=7, # For the moment only works for Daily data.
                    unique_id_column="<NAME OF ID COLUMN>",
                    ds_column= "<NAME OF DATESTAMP COLUMN>",
                    y_column="<NAME OF TARGET COLUMN>"
                  )

#Run Static Features
response_static_ft = tsfeatures.calculate_static_features_from_s3_uri(
                      s3_uri=s3_uri,
                      freq=7,
                      unique_id_column="<NAME OF ID COLUMN>",
                      ds_column= "<NAME OF DATESTAMP COLUMN>",
                      y_column="<NAME OF TARGET COLUMN>"
                    )

#Run Calendar Features
response_cal_ft = tsfeatures.calculate_calendar_features_from_s3_uri(
                    s3_uri=s3_uri,
                    country="<ISO>",
                    unique_id_column="<NAME OF ID COLUMN>",
                    ds_column= "<NAME OF DATESTAMP COLUMN>",
                    y_column="<NAME OF TARGET COLUMN>"
                  )
```

```python
response_tmp_ft
```


|    |   status | body                                          | id_job                               | message                                           |
|---:|---------:|:----------------------------------------------|:-------------------------------------|:--------------------------------------------------|
|  0 |      200 | "s3://nixtla-user-test/features/features.csv" | f7bdb6dc-dcdb-4d87-87e8-b5428e4c98db | Check job status at GET /tsfeatures/jobs/{job_id} |


- Monitor the process with the following code. Once it's done, access to your bucket to download the generated features.

```python
job_id = response_tmp_ft['id_job'].item()
```

```python
tsfeatures.get_status(job_id)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>status</th>
      <th>processing_time_seconds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>InProgress</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>


#### 2.2 Download your results from s3

Once the process is done you can download the results from s3.

```python
s3_uri_results = response_tmp_ft['dest_url'].item()
tsfeatures.download_from_s3(s3_url=s3_uri_results)
```


## ToDos

- Optimizing writing and reading speed with Parquet files
- Making temporal features available for different granularities
- Fill zeros (For Data where 0 values are not reported, e.g. Retail Data)
- Empirical benchmarking of model improvement
- Nan Handling
- Check data integrity before Upload
- Informative error messages
- Informative Status
- Optional parameter y in calendar
