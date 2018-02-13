#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__= 'luhj'
import json
from web import models
import subprocess
from django.conf import settings
class MutiTaskManger(object):
    '''解析并触发批量任务'''
    def __init__(self,request):
        self.request = request
        self.call_task()

    def task_paser(self):
        '''解析参数'''
        self.task_data = json.loads(self.request.POST.get('task_data'))


    def call_task(self):
        self.task_paser()
        if self.task_data['task_type'] == 0:
            self.cmd_task()
        elif self.task_data['task_type'] == 1:
            self.file_transfer_task()


    def cmd_task(self):
        '''
        1.生成任务id
        2.触发任务
        3.返回任务id
        '''
        task_obj = models.Task.objects.create(user=self.request.user,
                                              task_type=self.task_data['task_type'],
                                              content=self.task_data['cmd'])

        sub_task_objs = []
        for host_id in self.task_data['select_host_ids']:
            sub_task_objs.append(models.TaskLogDetail(task=task_obj,bind_host_id=host_id,
                                                      result='init...',status=2))

        models.TaskLogDetail.objects.bulk_create(sub_task_objs)

        task_script_obj = subprocess.Popen('python %s %s'%(settings.MULTITASK_SCRIPT,task_obj.id),
                                           shell=True,stdout=subprocess.PIPE)
        self.task = task_obj




    def file_transfer_task(self):
        task_obj = models.Task.objects.create(user=self.request.user,
                                              task_type=self.task_data['task_type'],
                                              content=self.task_data['cmd'])
        sub_task_objs = []
        for host_id in  self.task_data['select_host_id']:
            sub_task_objs.append(models.TaskLogDetail(task=task_obj,bind_host_id=host_id,
                                                      result='init...',status=2))
        models.TaskLogDetail.objects.bulk_create(sub_task_objs)

        task_script_obj = subprocess.Popen('python %s %s'%(settings.MULTITASK_SCRIPT,task_obj.id),
                                           shell=True,stdout=subprocess.PIPE)

        self.task = task_obj