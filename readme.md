

`gcloud config set app/cloud_build_timeout 900` (seconds) to increase buildtime limit in flex env, this will not work in standard env, default value 600seconds

deploy: `sudo gcloud app deploy --project read-me-a-story3`

view app in browser: `gcloud app browse --project=read-me-a-story3`
view logs: `gcloud app logs tail -s default`


