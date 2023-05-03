import requests
from secret import zabbix_token
import json

class RequestWorker:
    token = zabbix_token
    basic_params = {"jsonrpc": "2.0",
                    "method": "problem.get",
                    "auth": token,
                    "id": "1",
                    "params":
                        {}
                    }
    headers = {"Content-Type": "application/json"}

    def get_problems(self, problems_params):
        request_params = self.basic_params.copy()
        request_params['params'] = problems_params
        response = requests.post(url='http://docs.m-g-s.ru:21088/api_jsonrpc.php', data=json.dumps(request_params), headers=self.headers)
        print(response.json())
        request_params['method'] = "item.get"
        request_params['params'] = {'itemids': [problem['objectid'] if problem['object'] == '4' else 0 for problem in response.json()['result']]}
        response_host = requests.post(url='http://docs.m-g-s.ru:21088/api_jsonrpc.php', data=json.dumps(request_params), headers=self.headers)
        res = response_host.json()['result']
        request_params['method'] = "trigger.get"
        request_params['params'] = {'triggerids': [problem['objectid'] if problem['object'] == '0' else 0 for problem in response.json()['result']]}
        response_host = requests.post(url='http://docs.m-g-s.ru:21088/api_jsonrpc.php', data=json.dumps(request_params), headers=self.headers)
        res += response_host.json()['result']
        request_params['method'] = "discoveryrule.get"
        request_params['params'] = {'itemids': [problem['objectid'] if problem['object'] == '5' else 0 for problem in response.json()['result'] ]}
        response_host = requests.post(url='http://docs.m-g-s.ru:21088/api_jsonrpc.php', data=json.dumps(request_params), headers=self.headers)
        res += response_host.json()['result']
        print(len(res))
        print(len(response.json()['result']))
        return response.json()['result']