import boto3
import pandas as pd


class awscliService:
    def __init__(self, access_key:str, secret_access_key:str) -> None:
        self.ACCESS_KEY_ID = access_key
        self.SECRET_ACCESS_KEY = secret_access_key
        pass

    ACCESS_KEY_ID = ''
    SECRET_ACCESS_KEY = ''

# |Good parts:
# |- The code uses the boto3 library to interact with the AWS EC2 service and retrieve information about running instances.
# |- It filters the instances that are in a "running" state and extracts their name and private IP address.
# |- It then formats this information into a list of dictionaries, which is used to create a Pandas DataFrame.
# |- The DataFrame is then exported to a CSV file.
# |
# |Bad parts:
# |- The code does not handle exceptions in a specific way, it just prints the error message to the console. This can make it difficult to debug issues.
# |- The code assumes that all instances have a "Name" tag, which may not always be the case.
# |- The code does not provide any options for filtering or sorting the instances based on different criteria.
    def get_information(self):
        session = boto3.Session(
            aws_access_key_id=self.ACCESS_KEY_ID,
            aws_secret_access_key=self.SECRET_ACCESS_KEY
        )

        ec2 = session.client('ec2')

        response = ec2.describe_instances()

        data = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                try:
                    if instance['State']['Name'] == 'running' :
                        name = ''
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                        name, group, tag = self.change_instance_name(name)
                        print("instance Name: ", name)
                        print("PrivateIpAddress", instance['PrivateIpAddress'])
                        data.append({
                            'Groups':group,
                            'Label': name,
                            'Hostname/IP': instance['PrivateIpAddress'],
                            'Tags':tag,
                            'Protocol': 'ssh',
                            'Port': '22'
                        })
                except KeyError as e:
                    print(f"An error occurred: {type(e).__name__}: {str(e)}")
                except Exception as e:
                    print(f"An error occurred: {type(e).__name__}: {str(e)}")


        # 람다를 쓰면 안에서 변수를 못만들기 떄문에 다 고쳐야되서 그냥 안씀
        # data = [{
        #     'Groups': instance['SecurityGroups'][0]['GroupName'],
        #     'Label': next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), ''),
        #     'Hostname/IP': instance['PrivateIpAddress'],
        #     'Tags': instance['Tags'],
        #     'Protocol': 'ssh',
        #     'Port': '22'
        # } for reservation in response.get('Reservations', []) for instance in reservation.get('Instances', []) if instance.get('State', {}).get('Name', '') == 'running']

                    
        df = pd.DataFrame(data, columns=['Groups', 'Label', 'Tags', 'Hostname/IP', 'Protocol', 'Port'])
        # utf-8 로저장하면 한글이 깨지는데 정작 terminus에서는 제대로 인식함
        df.to_csv('terminus_import.csv', index=False, encoding='utf-8')

    def change_instance_name(self, name:str):    
        if name.startswith(' '):
            name = name.strip()
        group = 'HiAir'
        tag = ''
        if '개발' in name :
            tag = 'Dev'        
        elif 'WEB' in name:
            tag = 'WEB'
        elif 'IBE' in name:
            tag = 'IBE'
        elif 'Kiosk' in name:
            tag = 'Kiosk'
        elif 'Onepass' in name:
            tag = 'Onepass'
        elif 'OTA' in name:
            tag = 'OTA'
        elif 'PAY' in name:
            tag = 'PAY'
        elif '메세지' in name:
            tag = 'mtma'
        elif '홈페이지' in name:
            tag = 'hcws'
        elif 'Admin' in name : 
            tag = 'hims'
        elif '모바일' in name :
            tag = 'hmws'
        elif '배치' in name :
            tag = 'bpms'
        elif '관리' in name :
            tag = 'Manage'
        else :
            tag = 'ETC'  

        if '11' in name :
            name += ' 1호기'
        elif '21' in name :
            name += ' 2호기'
        elif '12' in name :
            name += ' 3호기'
        elif '22' in name :
            name += ' 4호기'
        
        return name, group, tag

    
cli = awscliService(access_key="", secret_access_key="")
cli.get_information()
