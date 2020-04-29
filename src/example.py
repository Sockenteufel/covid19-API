import boto3
s3 = boto3.client('s3')


if __name__ == '__main__':
    r = s3.select_object_content(
            Bucket='repo-minciencia-datos-covid19',
            Key='output/producto1/Covid-19_std.csv',
            ExpressionType='SQL',
            Expression="select * from s3object s ",
            InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}},
            OutputSerialization = {'CSV': {}},
    )

    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")
            print(statsDetails['BytesScanned'])
            print("Stats details bytesProcessed: ")
            print(statsDetails['BytesProcessed'])