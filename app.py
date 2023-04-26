from curses import flash
import os.path
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

import subprocess
import docker
import boto3
import json
import jenkins
import jenkinsapi
import jenkinscfg
#background-image: url("/home/amit/Desktop/project-2-vscode/Main-Project/static/images/im.jpeg");

import os
import time
# global public_ip
public_ip = 0
password = os.environ.get('MYPASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __str__(self):
        return f"Name:{self.first_name}, Last:{self.last_name}"





# remove all the names that signup to the website  
@app.route("/remove_all")
def remove_all():
    Profile.query.delete()
    db.session.commit()
    return 'Remove all from DB'
    # return redirect('/homepage')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        password = request.form.get("password")
        email = request.form.get("email")
        p = Profile(first_name=first_name, last_name=last_name, password=password, email=email)
        db.session.add(p)
        db.session.commit()
        return redirect('/homepage')
        
    return render_template("signup.html")

@app.route('/')
def root():
    return redirect('/signup')

@app.route("/homepage")
def homepage():
    # users_data = Profile.query.all()
    return render_template("homepage.html")
client = docker.from_env()
@app.route('/docker', methods=['GET', 'POST'])
def docker():
    if request.method == 'POST':
        image_name = request.form.get('image_name')  
        dockerfile_path = 'Dockerfile'
        buildimage = client.images.build(path='.', dockerfile=dockerfile_path, tag=f'porto23/flaskproject:{image_name}')
        client.login(username='porto23', password=password)
        client.images.push('porto23/flaskproject', tag={image_name})
        return f'Docker image created and pushed to Docker Hub'
    else:
        return render_template('docker.html')

@app.route('/aws')
def aws():
    return render_template('aws.html')

ec2 = boto3.client('ec2', region_name='us-east-1')
# @app.route('/create_ec2_instance', methods=['POST'])
@app.route('/aws', methods=['POST'])
def create_ec2_instance():
    ami_id_value = request.form['ami_id']
    instance_type = request.form['instance_type']
    name = request.form['instance_name']
    # security_group_id = request.form['security_group_id']
    # use_default_security_group = 'default_security_group' in request.form
    
    security_group_id = request.form.get('security_group_id')
    default_security_group = request.form.get('default_security_group')
    num_instances = int(request.form.get('num_instances'))


    if default_security_group == 'true':
     SecurityGroupIds = ['default']
    else:
     SecurityGroupIds = [security_group_id]
    
    install_docker = 'docker' in request.form
    install_jenkins ='jenkins' in request.form 
    # install_flask = 'flask' in request.form

    if not name:
        name = "EC2 Instance"

    user_data = "#!/bin/bash\n"
    
    if install_docker:
        user_data += "sudo apt-get update && sudo apt-get -y install docker.io\n"

    if install_jenkins:
        user_data += "sudo docker pull jenkins/jenkins:lts && sudo docker run -d -p 8080:8080 -p 50000:50000 --name Jenkins_master -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts"
   
    # if install_flask:
    #     user_data += "sudo apt install python3-flask\n"
    
    # key_name = request.form.get('key_name')
    # create_key_pair = request.form.get('create_key_pair') == 'true'

    # if create_key_pair:
    #     key_pair = ec2.create_key_pair(KeyName=key_name)
    #     private_key = key_pair['KeyMaterial']
    #     with open(f'{key_name}.pem', 'w') as f:
    #         f.write(private_key)

    response = ec2.run_instances(
    ImageId=ami_id_value,
    InstanceType=instance_type,
    SecurityGroupIds=SecurityGroupIds,
    MaxCount=num_instances,
    MinCount=1,
    # KeyName=key_name if not create_key_pair else None,
    KeyName='amit',
    UserData=user_data,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{
            'Key': 'Name',
            'Value': name
        }]
    }],
    
)
    

    instances = []
    for instance in response['Instances']:
        instance_data = {
        'id': instance['InstanceId'],
        'name': name,
        'public_ip': instance.get('PublicIpAddress')
    }
        
        global public_ip 
        public_ip = instance.get('PublicIpAddress')
        instances.append(instance_data)
        
        config = jenkinscfg.Config(f"http://{public_ip}:8080")
        config.plugins.install('configuration-as-code')
        config.apply({
        '        unclassified': {
            'globalSecurityConfig': {
                'useSecurity': True,
                'disableSignup': True
            },
            'setupWizard': {
                'isWizardPerformed': True
            }
        }
    })
        
        # Get the instance ID of the instance you just launched
    for instance in instances:
        while instances[0]['public_ip'] is None:
         print(f"Waiting for public IP address for instance {instance['id']}...")
         time.sleep(5)
         instance_info = ec2.describe_instances(InstanceIds=[instance['id']])
         instance['public_ip'] = instance_info['Reservations'][0]['Instances'][0].get('PublicIpAddress')
         
       
    return  instances



iam = boto3.client('iam')
# @app.route('/create_iam_user', methods=['GET', 'POST'])
@app.route('/aws', methods=['GET', 'POST'])

def create_iam_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "iam:CreateServiceLinkedRole",
                    "Resource": "arn:aws:iam::*:role/aws-service-role/apprunner.amazonaws.com/AWSServiceRoleForAppRunner",
                    "Condition": {
                        "StringLike": {
                            "iam:AWSServiceName": "apprunner.amazonaws.com"
                        }
                    }
                },
                {
                    "Effect": "Allow",
                    "Action": "iam:PassRole",
                    "Resource": "*",
                    "Condition": {
                        "StringLike": {
                            "iam:PassedToService": "apprunner.amazonaws.com"
                        }
                    }
                },
                {
                    "Sid": "AppRunnerAdminAccess",
                    "Effect": "Allow",
                    "Action": "apprunner:*",
                    "Resource": "*"
                }
            ]
        }

        
        response = iam.create_user(
            UserName=username
        )

        
        response = iam.create_login_profile(
            UserName=username,
            Password=password,
            PasswordResetRequired=True
        )

        
        policy_name = f"{username}-policy"
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )

       
        response = iam.attach_user_policy(
            UserName=username,
            PolicyArn=response['Policy']['Arn']
        )
 
        return f'IAM user created: {username} <br> <a href="/homepage"><button>Back to Homepage</button></a>'

    return render_template('create_iam_user.html')


@app.route("/jenkins", methods=["GET", "POST"])

def jenkins_create_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        mail = request.form.get("mail")
        fullname = request.form.get("fullname")
        
        # Connect to Jenkins server
        # server = jenkins.Jenkins(f'{public_ip}', username='admin', password='admin')
        server = Jenkins('http://54.163.81.172:8080/', username='admin', password='admin')
        
        # Define the new user credentials
        new_user = {
            'username': username,
            'password': password,
            'fullName': fullname,
            'email': mail
        }
        
        # Create the new user
        # server.create_user(username, password, fullname, mail)
        if not server.has_user(username):
            server.create_user(username, password, fullname, mail)
    return render_template('jenkins.html')


@app.route('/create-jenkins-job', methods=['GET', 'POST'])
def create_job():
    if request.method == "POST":
        
        job_name = request.form.get('job_test')
        server = jenkins.Jenkins('http://54.227.6.84:8080/', username='admin', password='admin')
        with open('templates/jenkins_job.xml', 'r') as f:
             job_config_xml = f.read()
        server.create_job(job_name, job_config_xml)
        return 'Job created successfully!'
    # else:
        # Return an error message if the job name is not provided
         
        # return redirect("/hompage")
    # return render_template("create-jenkins-job.html")


@app.route('/create_jenkins_pipe_job', methods=['GET', 'POST'])
def create_jenkins_pipe_job():
    if request.method == "POST":
        
        job_name_1 = request.form.get('job_test_1')
        server = jenkins.Jenkins('http://54.197.10.86:8080/', username='admin', password='admin')
        with open('templates/create_pip_job_1.xml', 'r') as f:
             job_config_xml_1 = f.read()
        server.create_job(job_name_1, job_config_xml_1)
        time.sleep(3)
        server.build_job(job_name_1)
        return 'Job created successfully!'
   
    # return render_template("/create-jenkins-pipe-job")

# @app.route('/upload_result_dynamodb', methods=['GET', 'POST'])
# def upload_dynamo():
    

    

if __name__ == "__main__":
    app.run(debug=True)
    
    

