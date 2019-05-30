from ipywidgets import widgets, HBox, VBox, Layout, Style
from traitlets import Unicode, Int, validate, Bool, HasTraits, observe, default, Dict, link
from IPython.display import display, HTML
from IPython import get_ipython
import boto3
import os
import json
from datetime import datetime
import time
import threading
from pathlib import Path
from shutil import copyfile

'''
// TODO MVP

x 1. modal dialog before calling api to create cluster
x 2. terminate cluster button
3. deployment from source
4. test script
5. Sample notebook with basic imports including athena and this widget for testing

IPython.core.display import Javascript
--- 
Enhancements
1. autopopulate inst type
2. add glue endpoint
3. glue endpoint
4. refactor new aws account
'''

response = {}
emr_client = boto3.client('emr')


def get_config_file():
    '''
    This function return path to sparkmagic config.json file.
    
    If file is not present it will generate a sample from a starter file.
    '''
    print('pwd :', Path.cwd())
    config_file = Path.home() / '.sparkmagic' / 'config.json'
    sample_file = Path.cwd() / 'example_config.json' 
    if config_file.exists() == False:
        copyfile(sample_file, config_file)
    
    return str(config_file)


def check_if_writable(file_name):
    if os.path.exists(file_name):
        # path exists
        if os.path.isfile(file_name): 
            return os.access(file_name, os.W_OK)
        else:
            return False
    pdir = os.path.dirname(file_name)
    if not pdir: pdir = '.'
    return os.access(pdir, os.W_OK)

def get_cluster_status(cluster_id):
    c_status = None
    try:
        response = emr_client.describe_cluster(ClusterId=cluster_id)
        c_status = response['Cluster']['Status']['State']
    except Exception as exc:
            print(f'It seems your AWS token has expired.  Create a new session with aws-azure-login and retry: {exc!r}')        
            exit
    return c_status

@widgets.register
class EMRWidget(VBox):
    selected_tab = Int(0, help="Tab selected").tag(sync=True)
   
    def __init__(self):
        self.select_tab = None
        self.log_items = []
        self.status_thread = None
        self.inst_type = widgets.Select(
            options=['m4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge'],
            value='m4.large',
            description='Inst. Type:',
            disabled=False
        )
        self.emr_no_nodes = widgets.BoundedIntText(
            value=3,
            min=1,
            max=20,
            step=1,
            description='No of Nodes:',
            disabled=False
        )
        self.no_of_dpu = widgets.BoundedIntText(
            value=2,
            min=1,
            max=100,
            step=1,
            description='No of DPU:',
            disabled=False
        )
        self.cluster_owner = widgets.Text(
            value='Adams',
            placeholder='Type something',
            description='Name:',
            disabled=False
        )

        self.config_file = widgets.Text(
            # value='/Users/aaliu/.sparkmagic/config.json',
            value=get_config_file(),
            placeholder='Type something',
            description='File Name:',
            disabled=False
        )
        self.config_ip_address = widgets.Text(
            value='localhost',
            placeholder='Type something',
            description='Master IP:',
            disabled=False
        )
        self.config_cluster_id = widgets.Text(
            value='j-1AEX4HFLF6C52',
            placeholder='Type something',
            description='Cluster ID:',
            disabled=False
        )

        @observe('self.config_cluster_id')
        def _update_cluster_id(self, change):
            pass
        
        self.update_button = widgets.Button(
            description='Update SparkMagic',
            button_style='info',
            disabled=False
        )
        self.config_cancel_button = widgets.Button(
            description='Cancel',
            button_style='danger',
            disabled=False
        )
        self.launch_button = widgets.Button(
            description='Launch Cluster',
            button_style='info'
        )
        self.terminate_button = widgets.Button(
            description='Terminate Cluster',
            button_style='info',
            disabled=False
        )
        self.confirm_label = widgets.HTML(value="")
        self.continue_button = widgets.Button(
            description='Continue',
            button_style='success',
            disabled=False
        )
        self.confirm_cancel_button = widgets.Button(
            description='Cancel',
            button_style='danger',
            disabled=False
        )
        self.cancel_button = widgets.Button(
            description='Cancel',
            button_style='danger'
        )
        self.confirm_prompt = VBox(children=[self.confirm_label])
        self.confirm_buttons = HBox(children=[self.continue_button, self.confirm_cancel_button])
        self.confirm_tab = VBox([self.confirm_prompt, widgets.Label(), self.confirm_buttons])
        
        label_layout = Layout( visibility='hidden')
        self.cluster_label = widgets.Label(value="Cluster " + self.config_cluster_id.value + ' has been launched', layout=label_layout)
        self.tab1 = VBox(children=[self.inst_type,
                            self.emr_no_nodes,
                            self.cluster_owner
                            ])
        self.tab2 = VBox(children=[self.config_cluster_id
                            ])
        self.tab4 = VBox(children=[self.cluster_owner
                            ])
        self.tab3 = VBox(children=[self.config_file, self.config_ip_address, self.config_cluster_id,
                            ])
        self.button_box = HBox(children=[self.launch_button, self.terminate_button, self.update_button, 
                            self.cancel_button])
        self.tab = widgets.Tab(children=[self.tab1, self.tab2, self.tab3, self.tab4])
        self.tab.set_title(0, 'Start EMR')
        self.tab.set_title(1, 'Terminate EMR')
        self.tab.set_title(2, 'Update SparkMagic')
        self.tab.set_title(3, 'Configure EMR')
        self.status_box = VBox()

        
        self.launch_button.on_click(self.get_confirmation)
        self.cancel_button.on_click(self.launch_cancelled)
        self.confirm_cancel_button.on_click(self.go_back)
        self.update_button.on_click(self.get_confirmation)
        self.terminate_button.on_click(self.get_confirmation)
        self.continue_button.on_click(self.confirmation_continues)
        super(EMRWidget, self).__init__(children=[self.tab, self.button_box, self.cluster_label, self.status_box])

    def get_confirmation(self, b):
        if self.tab.selected_index == 0:
            if b.description != 'Launch Cluster':
                print('please select Start EMR tab and retry')
                return None
 
            msg = "<h3>Please confirm: </h3> <br/><h4>You have selected to create <b>" +\
                str(self.emr_no_nodes.value) + "</b> nodes  <b>" + str(self.inst_type.value) +\
                 "</b> EMR cluster.  Click " + f"<b><font color='green'size='+2' >" + 'Continue'  + '</font></b>' +\
                      " to launch the cluster or " + f"<b><font color='red'size='+2' >" + 'Cancel' + '</font></b>' + " to abort.<br/><br/></h4>"
            self.select_tab = 0
        elif self.tab.selected_index == 1:
            self.continue_button.disabled = False
            if b.description != 'Terminate Cluster':
                print('please select Terminate Cluster tab and retry')
                return None
            msg = "<h3>Please confirm: </h3> <br/><h4>You have selected to terminate cluster " + str(self.config_cluster_id.value) +'.</b>' +\
                '<br/><br/>Note that this is an uncoverable step.  To proceed, click ' + f"<b><font color='green'size='+2' >" + 'Continue'  + '</font></b>' +\
                      " to terminate your cluster or " + f"<b><font color='red'size='+2' >" + 'Cancel' + '</font></b>' + " to abort.<br/><br/></h4>"
            self.select_tab = 1
        elif self.tab.selected_index == 2:
            if b.description != 'Update SparkMagic':
                print('please select Start EMR tab and retry')
                return None
            msg = "<h3>Please confirm: </h3> <br/><h4>" + "You have selected to update your sparkmagic configuration. <br>" +\
                '<br/><br/>To proceed, click ' + f"<b><font color='green'size='+2' >" + 'Continue'  + '</font></b>' +\
                      " or " + f"<b><font color='red'size='+2' >" + 'Cancel' + '</font></b>' + " to abort.<br/><br/></h4>"
            self.select_tab = 2      
        self.confirm_label.value = msg
        self.save_children = self.tab.children
        self.layout.visibility='hidden'
        self.tab.children = (self.confirm_tab,)
        self.layout.visibility='visible'
        self.button_box.layout.visibility='hidden'
   
    def confirmation_continues(self, b):
        if self.select_tab == 0:
            self.launch_emr()
        elif self.select_tab == 1:
            self.terminate_emr()
        elif self.select_tab == 2:
            self._modify_config()

    def launch_emr(self):     
        resp = {}
        if self.tab.selected_index != 0:
            print('Please select tab Start EMR and retry')
            return None

        try:
            resp = self._launch_emr()
            self.config_cluster_id.value = resp['JobFlowId']
            # // TODO add to status bar
            msg = datetime.now().strftime("%Y-%m-%d %H:%M") +' : Cluster ' + self.config_cluster_id.value  + ' has been launched.'
            self.cluster_label.value = msg
            self.cluster_label.layout.visibility = 'visible'
        except Exception as exc:
                print(f'The EMR launch raised an exception: {exc!r}')
        self.status_thread = threading.Thread(target=self.wait_for_emr_to_boot)
        self.status_thread.start()

    def launch_cancelled(self, b=None):
        self._reset_UI()

    def go_back(self, b):
        global save_chidren
        if self.status_thread != None:
            if self.status_thread.isAlive() and self.tab.selected_index == 0:
                # create cluster running
                self._reset_UI()
                self.launch_button.disabled = True
            else:
                self._reset_UI()
        else:
            self._reset_UI()

    def _reset_UI(self):
        self.layout.visibility='visible'
        self.button_box.layout.visibility='visible'
        self.status_box.layout.visibility='visible'
        self.tab.children = self.save_children
        self.cluster_label.layout.visibility = 'hidden'

    def _launch_glue(self):
        pass

    def terminate_emr(self):
        resp = {}
        try:
            c_status = get_cluster_status(self.config_cluster_id.value)
            if c_status == 'TERMINATED':
                print('Cluster terminated already')
                return None
            resp = self._terminate_emr()
            msg = datetime.now().strftime("%Y-%m-%d %H:%M") +' : Cluster ' +  self.config_cluster_id.value + ' is terminating.'
            self.cluster_label.value = msg
            self.cluster_label.layout.visibility = 'visible'
        except Exception as launch_exp:
            print(launch_exp.args)
            print(launch_exp)
        msg = datetime.now().strftime("%Y-%m-%d %H:%M") +' : Cluster ' + self.config_cluster_id.value + ' is ' + r'\(\color{red} {' + 'Terminating'  + '}\)'
        self.cluster_label.value = msg
        self.status_thread = threading.Thread(target=self.wait_for_emr_to_terminate)
        self.status_thread.start()
    
    def add_status_line(self):
        pass
    
    def get_client(self):
        emr_client = boto3.client('emr')
        return emr_client

    def _terminate_glue(self):
        pass

    def _terminate_emr(self):
        try:
            
            emr_client.set_termination_protection(JobFlowIds=[self.config_cluster_id.value,], TerminationProtected=False)
            response = emr_client.terminate_job_flows(JobFlowIds=[self.config_cluster_id.value, ])

        except Exception as terminate_exp:
            print(terminate_exp.args)
            print(terminate_exp)
        
    def _launch_emr(self):
        config_file = 'event.json'
        with open(config_file) as f:
            event = json.load(f)
        event['master-inst-type'] = self.inst_type.value
        event['slave-inst-type'] = self.inst_type.value
        event['instance-count'] = self.emr_no_nodes.value

        try:
            instances = {
                "MasterInstanceType": event["master-inst-type"],
                "SlaveInstanceType": event["slave-inst-type"],
                "InstanceCount": event["instance-count"],
                "Ec2KeyName": event['ec2keyname'],
                "ServiceAccessSecurityGroup": event['ServiceAccessSecurityGroup'],
                "Ec2SubnetId": event['Ec2SubnetId'],
                "EmrManagedMasterSecurityGroup": event['EmrManagedMasterSecurityGroup'],
                "EmrManagedSlaveSecurityGroup": event['EmrManagedSlaveSecurityGroup'],
                "KeepJobFlowAliveWhenNoSteps": True,
                "TerminationProtected": True,
            }

            configurations = [
                {
                    "Classification": "spark-env",
                    "Configurations": [
                        {
                            "Classification": "export",
                            "Properties": {
                                "PYSPARK_PYTHON": "/usr/bin/python3"
                            }
                        }
                    ]
                },
                {
                    "Classification": "yarn-env",
                    "Properties": {},
                    "Configurations": [
                        {
                            "Classification": "export",
                            "Properties": {
                                "PYSPARK_PYTHON": "/usr/bin/python3",
                            }
                        }
                    ]
                },
                {
                    "Classification": "spark-hive-site",
                    "Properties": {
                        "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                    }
                },
                {
                    "Classification": "hive-site",
                    "Properties": {
                        "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                    }
                },
                {
                    "Classification": "oozie-site",
                    "Properties": {
                        "oozie.service.ELService.ext.functions.workflow": "toUpperCase=com.manheim.dataservices.oozie.util.StrFunctions#toUpperCase",
                        "oozie.service.ELService.ext.functions.workflow": "toLowerCase=com.manheim.dataservices.oozie.util.StrFunctions#toLowerCase",
                        "oozie.action.subworkflow.max.depth": "150"
                    }
                }
            ]
            
            
            tags = event['tags']
            tags.append({"Key": "etl-project", "Value": "ovt"})
            applications = [{"Name": "Spark"}, {"Name": "Livy"}]
            if self.cluster_owner.value != '':
                c_name = 'SAGEMAKER-ENDPOINT' + '-' + self.cluster_owner.value
            else:
                c_name = 'SAGEMAKER-ENDPOINT'
            
            response = emr_client.run_job_flow(
                Name=c_name.upper(),
                LogUri=event['loguri'],
                ReleaseLabel=event['release-label'],
                Instances=instances,
                VisibleToAllUsers=True,
                Configurations=configurations,
                Tags=tags,
                Applications=applications,
                ServiceRole=event['servicerole'],
                JobFlowRole=event['jobflowrole'],
                AutoScalingRole=event['autoscalingrole'],
                ScaleDownBehavior="TERMINATE_AT_TASK_COMPLETION",
            )

        except emr_client.exceptions.ExpiredTokenException as client_exc:
            print(f'It seems your AWS token has expired.  Create a new session with aws-azure-login and retry: {client_exc!r}')
            exit
        except Exception as exc:
            print(exc.args)
            print(exc)
            exit
        return response
    
    def _modify_config(self): 
        self.config_file.layout.visibility = 'visible'
        file_path = self.config_file.value
        print('the file to update is: ', file_path)
        try:
            #self.config_cluster_id = self.config_cluster_id.value
            desc_response = emr_client.describe_cluster(
                ClusterId=self.config_cluster_id.value
            )
            master_dns = desc_response['Cluster']['MasterPublicDnsName']
            print("master dns", master_dns)
            exists = check_if_writable(file_path)
            print("file exists", exists)
            config = {}
            if exists:
                with open(file_path) as f:
                    config = json.load(f)
                print(config)
                config['kernel_python_credentials']['url'] = 'http://' + master_dns + ':8998'
                config['kernel_scala_credentials']['url'] = 'http://' + master_dns + ':8998'
                config['kernel_r_credentials']['url'] = 'http://' + master_dns + ':8998'
            else:
                print("Invalid sparkmagic configuration file specified or file not writable.  Please enter a valid path and try again")
            
            
        except FileNotFoundError as file_exception:
            print(file_exception.args)
            print(file_exception)
        except Exception as exc:
            print(exc.args)

        try:
            with open(file_path, 'w') as outfile:
                json.dump(config, outfile)
        except Exception as write_exception:
            print(write_exception.args)
            print(write_exception)

    def wait_for_emr_to_boot(self, max_attempts=15):
        self.confirm_cancel_button.description = 'Go Back'
        sleep_seconds = 60
        num_attempts = 0
        
        while True:
            c_status = get_cluster_status(self.config_cluster_id.value)
            num_attempts += 1
            if  c_status != 'WAITING':
                if 0 < max_attempts <= num_attempts:
                    raise Exception(
                        'Max attempts exceeded while waiting for AWS EMR to boot. Last response:\n'
                        + json.dumps(response, indent=3, default=str)
                    )
                time.sleep(sleep_seconds)
                item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{red} {' + c_status  + '}\)')
            elif  c_status != 'TERMINATING':
                time.sleep(sleep_seconds)
                item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{red} {' + c_status  + '}\)')
                break
            else:
                item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{green} {' + c_status  + '}\)')
                break
            item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{green} {' + c_status  + '}\)')
            self.log_items = (*self.log_items, item)
            self.status_box.children = self.log_items
        self.log_items = (*self.log_items, item)
        self.status_box.children = self.log_items
        return c_status

    def wait_for_emr_to_terminate(self, max_attempts=15):
        self.confirm_cancel_button.description = 'Go Back'
        sleep_seconds = 60
        num_attempts = 0
        while True:
            c_status = get_cluster_status(self.config_cluster_id.value)
            num_attempts += 1
            if  c_status != 'TERMINATED':
                if 0 < max_attempts <= num_attempts:
                    raise Exception(
                        'Max attempts exceeded while waiting for EMR to terminated. Last response:\n'
                        + json.dumps(response, indent=3, default=str)
                    )
                time.sleep(sleep_seconds)
                item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{red} {' + c_status  + '}\)')
            else:
                item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{green} {' + c_status  + '}\)')
                break
            item = widgets.Label(datetime.now().strftime("%Y-%m-%d %H:%M") +' : Your Cluster ' + self.config_cluster_id.value + ' is booting up and the status is ' +\
                        r'\(\color{green} {' + c_status  + '}\)')
            self.log_items = (*self.log_items, item)
            self.status_box.children = self.log_items
            self.launch_button.disabled = False
        self.log_items = (*self.log_items, item)
        self.status_box.children = self.log_items
        return c_status