import boto3
import pandas as pd


class awscliService:
    def __init__(self, access_key:str, secret_access_key:str) -> None:
        self.ACCESS_KEY_ID = access_key
        self.SECRET_ACCESS_KEY = secret_access_key
        pass

    ACCESS_KEY_ID = ''
    SECRET_ACCESS_KEY = ''

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
                        print("instance Name: ", name)
                        print("PrivateIpAddress", instance['PrivateIpAddress'])
                        name, group, tag = self.change_instance_name(name)
                        data.append({
                            'Groups':group,
                            'Label': name,
                            'Hostname/IP': instance['PrivateIpAddress'],
                            'Tags':tag,
                            'Protocol': 'ssh',
                            'Port': '22'
                        })
                except Exception as e : 
                    print(e)
        df = pd.DataFrame(data, columns=['Groups', 'Label', 'Tags', 'Hostname/IP', 'Protocol', 'Port'])
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
        
        return name, group, tag

    
cli = awscliService(access_key="", secret_access_key="")
cli.get_information()