gcloud auth login

gcloud builds submit --config build.yaml
#! Remember to change the image name if you fix the code
gcloud run deploy compass-utd-api --region=us-central1 --allow-unauthenticated --image=us-central1-docker.pkg.dev/aerobic-gantry-387923/compass-utd/vertex-agent-api
