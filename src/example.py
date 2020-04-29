import boto3
s3 = boto3.client('s3')


if __name__ == '__main__':
    r = s3.select_object_content(
            Bucket='repo-minciencia-datos-covid19',
            Key='output/producto1/Covid-19_std.csv',
            ExpressionType='SQL',
            # Expression="select * from s3object s ",
            # Expression="select * from s3object s where s.Fecha like '%2020-04-24%'",
            # Expression="select * from s3object s where s.Fecha = '2020-04-24'",
            # Expression="select * from s3object s where s.Fecha = '2020-04-24' and s.Region = 'Aysén'",
            # Expression="select * from s3object s where s.Fecha >= '2020-04-20' and s.Region = 'Aysén'",
            Expression="select * from s3object s where s.Fecha >= '2020-04-20' and s.Region = 'Aysén' and s.\"Casos confirmados\" > '0.0'",
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