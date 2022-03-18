Getting Start - Personal Device

Here is your IAM user account:mega:

Console URL:console link
Account ID: 224454369402
User name: perDevice
Password : @perDevice18745
Development Environment

Install Python:

Official Website
Tutorial
Required Python Package:

Boto 3:

pip3 install boto3
dotenv:

pip3 install python-dotenv
Install AWS-CLI:

Official Website
Configuring your AWS credential
Type aws configure in your terminal
Provide your “Access key ID” and “Secret access key” when prompted. Use “us-west-2” for “Default region name” and “json” for “Default output format”.
You can find your team’s key infromation in the sharefolder


How to upload file to S3

Make sure your are in the aws.py directory

1. Using our provide script (aws.py)

python3 aws.py --upload "${Bucket_Name}" --file_path "${file_path}"
(run python3 aws.py --help for more useful command arguments)

Example:

python3 aws.py --upload 18745-kiosk --file_path testFolder/test_kiosk 
ScreentShot–Check Upload file or Bucket by logging into the console


2. Using AWS-CLI

aws s3 sync . s3://18745-kiosk/testFolder/
The above command will copies the files from the current directory to an S3 bucket:18745-kiosk

Check for more information

How to download file from S3

Make sure your are in the aws.py directory
If you want to download files into loacl directory, please make sure directory is valid !!

1. Using our provide script (aws.py)

python3 aws.py --download "${Bucket_Name}" --file_path "${file_path}" --dst_path "${destionation_path}"
(run python3 aws.py --help for more useful command arguments)

Example:

$python3 aws.py --download 18745-kiosk --file_path testFolder/test_kiosk --dst_path test/test1
ScreenShot–Check files in the local directory or not:



2. Using AWS-CLI

aws s3 cp s3://18745-kiosk/testFolder ./ --recursive
The above command will copy all the files from bucket:18745-kiosk to current directory
