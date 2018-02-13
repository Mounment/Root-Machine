
from web import models
from django.contrib.auth import authenticate
import subprocess
import uuid
class HostManager(object):
    '''用户登录堡垒机的程序'''
    def __init__(self):
        self.user = None
    

    def get_session_id(self,bind_host_obj,tag):
        session_obj = models.Session(user_id=self.user.id,bind_host=bind_host_obj,tag=tag)
        session_obj.save()
        return session_obj


    def interactive(self):
        '''交互脚本'''
        count = 0
        while count < 3:
            username = input('username:').strip()
            password = input('password:').strip()
            user = authenticate(username=username,password=password)
            if user:
                print('Welcome %s'.center(50,'-')%username)
                self.user = user
                break
            else:
                print('wrong username')
            count += 1
        else:
            exit('too many attempt,bye')


        if self.user:
            while True:
                for index,host_group in enumerate(self.user.hosts_groups.all()):
                    print('%s.\t%s[%s]'%(index,host_group.name,host_group.bind_hosts.count()))
                print('z.\t未分组主机[%s]'%(self.user.bind_hosts.count()))

                choice = input('%s>>'%self.user.name).strip()
                if len(choice) == 0: continue
                selected_host_group = None

                if choice.isdigit():
                    choice = int(choice)
                    if choice >=0 and choice <= index:
                        selected_host_group = self.user.hosts_groups.all()[choice]

                elif choice == 'z':
                    selected_host_group = self.user

                if selected_host_group:
                    while True:
                        for index, bind_host in enumerate(selected_host_group.bind_hosts.all()):
                            print('%s.\t[%s]' % (index, bind_host))

                        choice = input('%s>>' % self.user.name).strip()
                        if choice.isdigit():
                            choice = int(choice)
                            if choice >= 0 and choice <= index:
                                print('going to logon', selected_host_group.bind_hosts.all()[choice])
                                bind_host = selected_host_group.bind_hosts.all()[choice]
                                ssh_tag = uuid.uuid4()
                                session_obj = self.get_session_id(bind_host,ssh_tag)
                                moniter_script = subprocess.Popen('sh /home/crazy_audit/CrazyEye/backend/session_tracker.sh %s %s' %(ssh_tag,session_obj.id), shell=True,
                                                                  stdout=subprocess.PIPE)
                                subprocess.run('sshpass -p %s ssh %s@%s -E %s -o  StrictHostKeyChecking=no' % (bind_host.remote_user.password,
                                                                            bind_host.remote_user.username,
                                                                            bind_host.host.ip_addr,ssh_tag),shell=True)
                        elif choice == 'b':
                            break




