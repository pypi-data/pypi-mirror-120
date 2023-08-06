# TSBenchmarks
> Time-series benchmarking a service. TSBenchmarks is an SDK for benchmarking models on public datasets.

 Since we take care of the whole infrastructure, benchmarking becomes as easy as running a line in your python nootebooks or calling an API.
## Why?

We build TSBenchmarks because we wanted a standarized solution for benchmarking time-series forecasting models. We evaluate provided forecasts on well known public datasets against benchmark models.
## Table of contents

- [TSBenchmarks](#tsbenchmarks)
  * [Install](#install)
  * [How to use](#how-to-use)
    + [Data Format](#data-format)
    + [1. Request free trial](#1-request-free-trial)
    + [2. Run `tsbenchmarks` on a private S3 Bucket](#2-run--fasttsfeatures--on-a-private-s3-bucket)
      - [2.1 Upload to S3 from python](#21-upload-to-s3-from-python)
      - [2.2 Run the evaluation process](#22-run-the-features-extraction-process)
      - [2.3 Download your results from s3](#23-download-your-results-from-s3)

## Available Benchmark Datasets

- M4-Daily

## Available Benchmark models

- Naive1
- Naive2
- ETS
- Theta
- ARIMA
- MLP
- RNN
- ESRNN
- FFORMA
- NBEATS

## Available Metrics and Plots

- MASE
- sMAPE
- Average loss by time-series
- Average loss by timestamp

## Install

`pip install tsbenchmarks`

## How to use

You can use TSBenchmarks by either using a completely public S3 bucket or by uploading a file to your own S3 bucket provided by us.  

### Data Format

Currently we only support `.csv` files. These files must include at least 3 columns, with a unique_id (identifier of each time-series) a date stamp and a value. The unique_id and ds must coincide with the test set of the selected benchmark dataset.

### 1. Request free trial

Request a free trial sending an email to: fede.garza.ramirez@gmail.com and get your `BUCKET_NAME`, `API_ID` and `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

### 2. Run `tsbenchmarks` on a private S3 Bucket

If you don´t want other people to potentially have access to your data you can run `tsbenchmarks` on a private S3 Bucket. For that you have to upload your data to a private S3 Bucket that we will provide for you; you can do this inside of python.

#### 2.1 Upload to S3 from python

You will need the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` that we provided.


- Import and Instantiate `TSBenchmarks` introducing your `BUCKET_NAME`, `API_ID` and `API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.

```python
from tsbenchmarks.core import TSBenchmarks

tsbenchmarks = TSBenchmarks(bucket_name='<BUCKET_NAME>',
                            api_id='<API_ID>',
                            api_key='<API_KEY>',
                            aws_access_key_id='<AWS_ACCESS_KEY_ID>',
                            aws_secret_access_key='<AWS_SECRET_ACCESS_KEY>')
```

- Upload your local file introducing its name.

```python
s3_uri = tsbenchmarks.upload_to_s3(file='<YOUR FILE NAME>')
```

- Run the evaluation process

To run the process specify:
- `s3_uri`: S3 uri provided after calling `tsbenchmarks.upload_to_s3()`.
- `dataset`: Name of dataset
- `ds_column`: Name of the unique id column.
- `y_column`: Name of the target column.

```python

#Run Evaluation
response_tmp_ft = tsbenchmarks.evaluate_my_model(
                    s3_uri="<PRIVATE S3 URI HERE>",
                    dataset='M4-Daily',
                    unique_id_column="<NAME OF ID COLUMN>",
                    ds_column= "<NAME OF DATESTAMP COLUMN>",
                    y_column="<NAME OF TARGET COLUMN>"
                  )
```

```python
response_tmp_ft
```


|    |   status | message                                          | id_job                               | dest_url                                           |
|---:|---------:|:----------------------------------------------|:-------------------------------------|:--------------------------------------------------|
|  0 |      200 | Check job status at GET /tsbenchmarks/jobs/{jo...	 | d8d2ae2f-ac53-4b81-87f5-49520782365a | s3://ts-benchmarks-api-public/M4-Daily-benchma...
 |


- Monitor the process with the following code. Once it's done, access to your bucket to download the generated features.

```python
job_id = response_tmp_ft['id_job'].item()
```

```python
tsbenchmarks.get_status(job_id)
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

Once the process is done you can explore and download the results from s3.


## ToDos

- Optimizing writing and reading speed with Parquet files
- Nan Handling
- Check data integrity before Upload
- Informative error messages
- Informative Status