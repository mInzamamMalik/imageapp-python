# deploy on Google App Engine


`gcloud config set app/cloud_build_timeout 900` (seconds) to increase buildtime limit in flex env, this will not work in standard env, default value 600seconds

deploy: `sudo gcloud app deploy --project read-me-a-story3`

view app in browser: `gcloud app browse --project=read-me-a-story3`
view logs: `gcloud app logs tail -s default`



<hr>

App Engine free quota in free tier
28 hours per day of "F" instances
9 hours per day of "B" instances
1 GB of egress per day
The Google Cloud Free Tier is available only for the Standard Environment.

Learn more (https://cloud.google.com/appengine/pricing)




# deploy on Google Compute Engine

https://amanranjanverma.medium.com/run-flask-app-on-gcp-compute-engine-vm-instance-de4aea60a6fe

after creating the machine open ssh in browser window and run following command to setup machine for the first time:

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
sudo apt-get install python3-pip

git clone https://github.com/mInzamamMalik/google-app-engine-flask-hello-world.git
cd google-app-engine-flask-hello-world/

pip install -r ./requirements.txt
python3 main.py


copy external ip of instance and open it in new browser tab like this `http://104.999.999.222:3003/` ans see flask app running in production

extras:
to download any file from internet in ssh terminal, goto folder where you wanted it to be downloaded and run following command:

wget -O fileName.txt https://firebasestorage.googleapis.com/v0/b/sysborg-air.appspot.com/o/model%2Fpytorch_model.bin?alt=media&token=5eaa3b0d-cc85-4abf-aff5-8a1d2799dd78


