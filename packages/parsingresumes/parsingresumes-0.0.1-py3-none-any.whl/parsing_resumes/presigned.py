import aws
import logging
import boto3
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        print("no resume found with this name: ", object_name, '\n')
        return None

    # The response contains the presigned URL
    return response

# 'resume-test-bucket-fcg', 'S3 Ex object.rtf'

# s3 = boto3.resource('s3')
# bucket = s3.Bucket('resume-test-bucket-fcg')
# bucket_keys = []
# test_s3_uri = 's3://resume-test-bucket-fcg/16388_JULIANNA_KUHN_13516_Kuhn_Principal_GISAnalyst_Letter.pdf'
# for object in bucket.objects.all():
#     print(object.key)
#     bucket_keys.append(object.key)
#     if object.key in test_s3_uri:
#         print("FOUND the uri in object: ", object, '\n')
#         print("the key for found object is: ", object.key, '\n')
#         print("the presigned url for this object is: \n")
#         print(create_presigned_url('resume-test-bucket-fcg', object.key))
