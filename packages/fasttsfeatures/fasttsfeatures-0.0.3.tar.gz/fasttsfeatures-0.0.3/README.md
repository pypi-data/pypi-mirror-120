# FastTSFeatures
> Compute static or temporal time-series features at scale.


## Install

`pip install fasttsfeatures`

## How to use

### 1. Request free trial 

Request a free trial sending an email to: fede.garza.ramirez@gmail.com.

### 2. Required information

To use `fasttsfeatures` you need:

- An AWS url provided by `Nixtla`. You'll upload your dataset here.
- An user and a password to enter the previous url.
- An API Key to interact with the scalable API.
- An API ID to interact with the scalable API.

### 3. Upload your dataset

- Access the url provided by `Nixtla`. You'll see a login page like the following. Just enter your user and paswsword.

<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/console-login-aws.png">

- Next you'll see the bucket where you can upload your dataset:


<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/bucket.png">


- Upload your dataset and copy its S3 URI.


<img src="https://raw.githubusercontent.com/Nixtla/fasttsfeatures/main/.github/images/s3-uri.png">


### 4. Run the process

- Import the library.

```python
from fasttsfeatures.core import TSFeatures
```

- Instantiate `TSFeatures` introduce your `api_id` and `api_key`.

```python
tsfeatures = TSFeatures(api_id=os.environ['API_ID'], 
                        api_key=os.environ['API_KEY'])
```

- Run the process introducing your previous copied S3 uri. 

```python
response = tsfeatures.calculate_features_from_s3_uri(s3_uri='s3://tsfeatures-api-public/train.csv',
                                                     freq=7)
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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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

