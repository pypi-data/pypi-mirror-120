# FastTSFeatures
> Time-series feature extraction as a service. 
FastTSFeatures is an SDK to compute static, temporal and calendar variables as a service.

The package serves as a wraper for [tsfresh](https://github.com/blue-yonder/tsfresh) and [tsfeatures](https://github.com/Nixtla/fasttsfeatures). Since we take care of the whole infrastructure, feature extraction becomes as easy as running a line in your python nootebooks or calling an API.

## Why?
We build FastTSFeatures because we wanted and easy and fast way to extract Time Series Features without having to think about infrastructure and deployment. Now we want to see if other Data Scientists find it useful too. 


## Avaiable Features (More than 600)
Static Features
- 40+ Features: https://github.com/Nixtla/tsfeatures
- 600+ https://github.com/blue-yonder/tsfresh/
Temporal Features 
- 10 Temporal Features (lags, mean lags, std_lags) [Currently just supported for daily data]
Calendar Features (distance in minutes to holidays)
- Calendar features for 83 Countries https://github.com/dr-prodigy/python-holidays



## API
For api documantation  visit [PENDING]


## Install

`pip install fasttsfeatures`

## How to use


### 1. Request free trial 

Request a free trial sending an email to: fede.garza.ramirez@gmail.com and get your API_KEY, API_ID and private URI

#### 2. Run fasttsfeatures on a public S3 Bucket (Reading and writing permissions needed)

- Import and Instantiate `TSFeatures`.  Introduce your `API_ID` and `API_KEY`.

```python
from fasttsfeatures.core import TSFeatures

tsfeatures = TSFeatures(api_id=os.environ['API_ID'], 
                        api_key=os.environ['API_KEY'])
```

- Run the process introducing the public S3 uri. 

```python

#Run Temporal Features
response_tmp_ft = tsfeatures.calculate_temporal_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     freq=7))

#Run Static Features
response_static_ft = tsfeatures.calculate_static_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE", freq=7)

#Run Calendar Features
response_cal_ft = tsfeatures.calculate_calendar_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     country="USA")
```

```python
display_df(response)
```


|    |   status | body                                          | id                                   | message                                           |
|---:|---------:|:----------------------------------------------|:-------------------------------------|:--------------------------------------------------|
|  0 |      200 | "s3://nixtla-user-test/features/features.csv" | f7bdb6dc-dcdb-4d87-87e8-b5428e4c98db | Check job status at GET /tsfeatures/jobs/{job_id} |


- Monitor the process with the following code. Once it's done, access to your bucket to download the generated features.

```python
job_id = response['id'].item()
```

```python
display(tsfeatures.get_status(job_id))
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

Once the process is done you will find a file for each process you ran in the URI we provied.


### 3. Run fasttsfeatures on a private S3 Bucket 

To run fasttsfeatures on a private S3 Bucket you have to upload your data to a private S3 Bucket that we will provide for you, you can do this either inside of python or with the AWS Console. 

#### 3.1 Case 1: Upload to S3 from python

You will need the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY that we provided. 


- Import and Instantiate `TSFeatures` introduce your `API_ID` and `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

```python
from fasttsfeatures.core import TSFeatures

tsfeatures = TSFeatures(api_id=os.environ['API_ID'], 
                        api_key=os.environ['API_KEY'],
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
```

- Upload your local file introducing its name and the bucket's name (provided by `Nixtla`).

```python
s3_uri = tsfeatures.upload_to_s3('../train.csv', 'PROVIDED URI GOES HERE')
```

- Run the process introducing the public S3 uri. 

```python

#Run Temporal Features
response_tmp_ft = tsfeatures.calculate_temporal_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     freq=7))

#Run Static Features
response_static_ft = tsfeatures.calculate_static_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE", freq=7)

#Run Calendar Features
response_cal_ft = tsfeatures.calculate_calendar_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     country="USA")
```
Once the process is done you will find a file for each process you ran in the URI we provied.


#### 3.2 Case 2: Upload to S3 Manually using the S3 Console

##### A. Upload your dataset

- Access the url provided by `Nixtla`. You'll see a login page like the following. Just enter your user and paswsword.

<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/console-login-aws.png">

- Next you'll see the bucket where you can upload your dataset:


<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/bucket.png">


- Upload your dataset and copy its S3 URI.


<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/s3-uri.png">


##### B. Run the process



- Import the library.

```python
from fasttsfeatures.core import TSFeatures
```

- Instantiate `TSFeatures` introduce your `api_id` and `api_key`.

```python
tsfeatures = TSFeatures(api_id=os.environ['API_ID'], 
                        api_key=os.environ['API_KEY'])
```

- Run the process introducing the public S3 uri. 

```python

#Run Temporal Features
response_tmp_ft = tsfeatures.calculate_temporal_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     freq=7))

#Run Static Features
response_static_ft = tsfeatures.calculate_static_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE", freq=7)

#Run Calendar Features
response_cal_ft = tsfeatures.calculate_calendar_features_from_s3_uri(s3_uri="PUBLIC S3 URI HERE",
                                                     country="USA")
```

```python
display_df(response)
```


|    |   status | body                                               | id                                   | message                                           |
|---:|---------:|:---------------------------------------------------|:-------------------------------------|:--------------------------------------------------|
|  0 |      200 | "s3://tsfeatures-api-public/features/features.csv" | 740a410a-d138-41b4-8373-581710f020f8 | Check job status at GET /tsfeatures/jobs/{job_id} |


- Monitor the process with the following code. Once it's done, access to your bucket to download the generated features.

```python
job_id = response['id'].item()
```

```python
display(tsfeatures.get_status(job_id))
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
      <td>20</td>
    </tr>
  </tbody>
</table>
</div>

Once the process is done you will find a file for each process you ran in the URI we provied.

## ToDos
- Optimizing writing and reading speed with Parquet files
- Making temporal features available for different granularities
- Fill zeros (For Data where 0 values are not reported, e.g. Retail Data)
- Empirical benchamarking of model improvement
