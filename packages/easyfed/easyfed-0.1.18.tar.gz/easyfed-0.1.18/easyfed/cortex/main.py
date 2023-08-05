from easyfed.utils.functions import *
import os
import time
import torch
class server():
    def __init__(self,bdir,port=16668):
        self.bdir=bdir
        self.port=port
    def run(self):
        path=os.path.join(self.bdir,'effront','manage.py')
        os.system("python %s migrate && python %s runserver 0.0.0.0:%s"%(path,path,self.port))

class client():
    def __init__(self,clientName,host):
        self.clientname=clientName
        self.host=host
        self.key=None
    def login(self):
        result=client_login(self.host,self.clientname)
        while int(result['result'])!=1:
            print('Client %s request to login.'%(self.clientname))
            result=client_login(self.host,self.clientname)
            if int(result['result'])!=1:
                time.sleep(5)
        self.key=result['key']
        print('Client %s login successful.'%(self.clientname),'key',self.key)
    def submit(self,model,loss=None):
        req=get_status(self.host,self.key)
        state,clientstatus,url=req['result'],req['clientstatus'],req['modelurl']
        save_path=''
        while int(state)!=0:
            if int(clientstatus)==0:
                send_model(self.host,self.key,model,loss)
            req=get_status(self.host,self.key)
            if int(req['clientstatus'])!=0:
                print('waiting for other clients...')
            state,clientstatus,url=req['result'],req['clientstatus'],req['modelurl']
            if url:
                save_path=download_model(self.host,req['modelurl'],self.key)
                break
            time.sleep(5)
        if save_path:
            model.load_state_dict(torch.load(save_path))
            print('model weights updated...')
        return model