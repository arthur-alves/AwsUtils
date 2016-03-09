#AwsUtils Tool

AwsUtils is a simple and basic tool to automate some tasks in AwsEC2 using python *boto* lib by AWS.

###Configure AwsUtils over scripts

To create a automate script in **AWS** you must to do some basic config. First, we going to config a file .boto and credentials.
This files are mandatory to login in AWS over the scripts. A **boto** lib automatically get in this files the credentials
to comunicate with EC2.

Obs: See *boto_example* file to create your own.

###Requirements:

1. Config credentials inside the AWS console (Check this out on Google/AWS if you don't know.)
2. All dependencies is listed on requirements.txt of project.

###.boto file.

- Create a file with name **.boto** on root path of your user.
- Copy boto_example file ovewriting *access key* e *secret key* by your credenciais.


###File .aws/credentials

- Create a folder with name **.aws** on root path of your user, and create a **credentials** file.
- Edit and put the same content of **.boto** in **credentials** file.


After that, see the file [aws_control.py](aws/aws_control.py).
This file have an example script that you can use, or improve if you need, is very basic.


Check this [link Github aws/boto](https://github.com/boto/boto/blob/4f66311f2918aacd4bd7fefff9e0c8ed7bc2813e/docs/source/boto_config_tut.rst) if *boto* config change or outdate.
