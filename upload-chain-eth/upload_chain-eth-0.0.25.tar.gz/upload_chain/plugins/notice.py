#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
Author:       yuyongpeng@hotmail.com
Github:       https://github.com/yuyongpeng/
Date:         2019-04-17 17:25:06
LastEditors:  
LastEditTime: 2019-04-17 17:25:06
Description:  
"""

from upload_chain.plugins import Processor
import json
import peewee
import toolz
from upload_chain.setting import VAR
from upload_chain.queues import Rabbitmq, Kafka
from upload_chain import mail


@Processor.plugin_register('email')
class NoticeEmail(object):
    """
    处理 notice = email 的数据
    """
    def __init__(self):
        pass

    def before(self, body):
        self.smtp = VAR['MAIL_SMTP']
        self.mail_password = VAR['MAIL_PASSWORD']
        self.mail_user = VAR['MAIL_USER']
        self.success = body.get('success', False)
        self.email = body['send_email']  # list
        self.mail_subject = "上链成功" if self.success else "上链失败"

    def process(self, body):
        """
        处理 event=email 的函数
        :param body: 获得的event数据
        :return:
        """
        mail.send_email(mail_subject=self.mail_subject,
                        mail_host=self.smtp,
                        mail_pass=self.mail_password,
                        mail_receiver=self.email,
                        mail_body=self.queue_msg,
                        mail_sender=self.mail_user)

    def after(self, entry):
        pass


@Processor.plugin_register('database')
class NoticeDatabase(object):
    """
    处理 notice = email 的数据
    """
    def __init__(self):
        pass

    def update_mysql(self, success, *args, **kwargs):
        """
        更新数据库的状态
        :param success:  True: 成功上链，False: 上链失败
        :param args:
        :param kwargs:
        :return:
        """
        ip = kwargs.pop('ip', VAR['MYSQL_IP'])
        port = kwargs.pop('port', VAR['MYSQL_PORT'])
        user = kwargs.pop('user', VAR['MYSQL_USER'])
        password = kwargs.pop('password', VAR['MYSQL_PASSWORD'])
        charset = VAR['MYSQL_CHARSET']
        schema = kwargs.pop('schema', VAR['MYSQL_SCHEMA'])
        db = peewee.MySQLDatabase(
            host=ip,
            database=schema,
            port=port,
            user=user,
            passwd=password,
            charset=charset
        )
        sqls = kwargs.pop('sql')
        if sqls is not None:
            if success is True:
                with db.atomic():
                    for sql in sqls['success']:
                        # 执行多条
                        db.execute_sql(sql.replace('\n', ' ').replace('\t', ' '))
            else:
                with db.atomic():
                    for sql in sqls['fail']:
                        # 执行多条
                        db.execute_sql(sql.replace('\n', ' ').replace('\t', ' '))
        else:
            table = kwargs.pop('table')
            column = kwargs.pop('column')
            id_column = kwargs.pop('id_column')
            id = kwargs.pop('id')
            value = kwargs.pop('success_tag') if success else kwargs.pop('failed_tag')
            sql = "update {}.{} set {}=%s where {}=%s".format(schema, table, column, id_column)
            # sql = "update {}.{} set {}={} where {}={}".format(schema, table, column, value, id_column, id)
            print(sql)
            cursor = db.execute_sql(sql, (value, id))
            db.commit()
            cursor.close()
            db.close()

    def before(self, body):
        self.success = body.get('success', False)

    def process(self, body):
        """
        处理 event=database 的函数
        :param body: 获得的event数据
        :return:
        """
        database = body['send_database']
        self.update_mysql(success=self.success, **database['mysql'])

    def after(self, body):
        pass


@Processor.plugin_register('rabbitmq')
class NoticeRabbitmq(object):
    """
    处理 notice = email 的数据
    """
    def __init__(self):
        pass

    def before(self, body):
        self.queue_ip = body.get('queue_ip', VAR['QUEUE_IP'])
        self.queue_port = body.get('queue_port', VAR['QUEUE_PORT'])
        self.queue_user = body.get('queue_user', VAR['QUEUE_USER'])
        self.queue_password = body.get('queue_password', VAR['QUEUE_PASSWORD'])
        self.queue_name = toolz.get_in(['send_queue', 'queue_msg', 'queue_name'], body, VAR['QUEUE_NAME_NOTICE'])
        self.queue_vhost = body.get('queue_vhost', VAR['QUEUE_VHOST'])
        self.queue_msg = json.dumps(body)

    def process(self, body):
        """
        处理 event=rabbitmq 的函数
        :param body: 获得的event数据
        :return:
        """
        rabbitmq = Rabbitmq(queue_ip=self.queue_ip, queue_port=self.queue_port, queue_user=self.queue_user,
                            queue_password=self.queue_password, queue_name=self.queue_name, queue_vhost=self.queue_vhost)
        rabbitmq.send_msg(self.queue_msg)

    def after(self, body):
        pass


@Processor.plugin_register('kafka')
class NoticeKafka(object):
    """
    处理 notice = email 的数据
    """
    def __init__(self):
        pass

    def before(self, body):
        self.queue_ip = body.get('queue_ip', VAR['KAFKA_IP'])
        self.queue_port = body.get('queue_port', VAR['KAFKA_PORT'])
        self.queue_topic = body.get('queue_topic', VAR['QUEUE_TOPIC'])
        self.queue_msg = json.dumps(body)

    def process(self, body):
        """
        处理 event=kafka 的函数
        :param body: 获得的event数据
        :return:
        """
        kafka = Kafka(queue_ip=self.queue_ip, queue_port=self.queue_port, queue_topic=self.queue_topic)
        kafka.send_msg(self.queue_msg)

    def after(self, body):
        pass

