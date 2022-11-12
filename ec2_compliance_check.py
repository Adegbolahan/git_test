import json
import boto3

client_ec2 = boto3.client('ec2')
paginator_ec2 = client_ec2.get_paginator('describe_instances')
approved_ami=['ami-08c40ec9ead489470']


def get_ec2_list():
    response_iterator = paginator_ec2.paginate(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running', 'pending', 'stopped'
                ]
            },
        ],
        InstanceIds=[],
        DryRun=False, 
    )
    print("*"*40)
    instance_list=[]
    for items in response_iterator:
        for each_item in items['Reservations']:
            for instance in each_item['Instances']:
                instance_id=instance['InstanceId']
                image_id=instance['ImageId']
                instance_list.append((instance_id,image_id))
                
    print("instance_list: ",instance_list)
        
    print("*"*40)
    return instance_list
    
def complainace_check(result):
    complaint_list=[]
    non_complaint=[]
    for item in result:
        if item[1] in approved_ami:
            complaint_list.append(item)
        else:
            non_complaint.append(item)
    
    print("*"*40)        
    print("Complaint List: ", complaint_list)
    print("Non complaint List: ", non_complaint)
    print("*"*40)
    return non_complaint
    
def remediate_non_compliant_instances(res):
    if len(res) > 0:
        for item in res:
            response = client_ec2.terminate_instances(
                InstanceIds=[
                    item[0],
                ],
            )
            print("-"*40)     
            print(f"{item[0]} is non_complaint and terminated")
            print("-"*40)    
    else:
        print("All instances are complaint")
    
def lambda_handler(event, context):
    # TODO implement
    '''
    Get all ec2 instances in the account.
    status report
    Upload to bucket 
    Check the ami parameter against the approved parameter
    terminated non compliance instances
    '''
    result=get_ec2_list()
    # status_report()
    # upload_bucket()
    res=complainace_check(result)
    remediate_non_compliant_instances(res)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


#def __name__ = '__main__':
    