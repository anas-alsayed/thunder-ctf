from flask import render_template
def main(request):
	import google.oauth2.service_account
	from google.oauth2.credentials import Credentials
	from google.cloud import logging
	from google.cloud.logging import DESCENDING
	import os
	
	
	# Set the project ID
	PROJECT_ID = os.environ['GCP_PROJECT']
	FUNCTION_REGION = os.environ['FUNCTION_REGION']
	NONCE = os.environ.get('NONCE', 'Specified environment variable is not set.')
	RESOURCE_PREFIX = os.environ.get('RESOURCE_PREFIX', 'Specified environment variable is not set.')
	LEVEL_NAME = os.environ.get('LEVEL_NAME', 'Specified environment variable is not set.')

	# Get credential of cloud function account
	credentials, project_id = google.auth.default()


	#score function url
	surl  = f'https://europe-west1-{PROJECT_ID}.cloudfunctions.net/scores-f-{NONCE}'
	
	
	err=[]
	resources = []
	try:
		#Build logging REST API python object
		client = logging.Client(credentials=credentials )
		# filter = f"projects.setIamPolicy AND {NONCE} AND log_name=projects/{PROJECT_ID}/logs/cloudaudit.googleapis.com%2Factivity"
		# entries = client.list_entries(order_by="timestamp desc", filter_=filter)
		logname = "cloudaudit.googleapis.com%2Factivity"
		filter =f"projects.setIamPolicy AND {NONCE}"
		logger = client.logger(logname)
		#entry = list(logger.list_entries(order_by=DESCENDING, filter_=filter))[0]
		entries = logger.list_entries(order_by=DESCENDING, filter_=filter)
		for entry in entries:
			resources.append(entry)
			if len(resources) >0:
				break

	except Exception as e:
		resources.append('Insufficient privilege!') 
		err.append(str(e))
	
	url=f'https://europe-west1-{PROJECT_ID}.cloudfunctions.net/{RESOURCE_PREFIX}-f-check-{NONCE}'
	
	
	return render_template(f'{RESOURCE_PREFIX}-access.html', resources=resources, url=url, err=err,prefix=RESOURCE_PREFIX, level_name=LEVEL_NAME,nonce=NONCE, surl=surl)

	

