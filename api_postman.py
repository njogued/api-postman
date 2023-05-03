import os
from flask import Flask, send_file, abort, request

app = Flask(__name__)

@app.route('/<folder>/<file>', methods=['GET'])
def download_and_remove(folder, file):

	# Check if the request method is GET
	if request.method == "GET":

		# Specify the directory to save the downloaded file
		downloads = "/path/to/downloads"

		# Specify the full path to save the downloaded file
		destination = os.path.join(downloads, folder, file)

		# Check if the file already exists in the destination directory
		if os.path.exists(destination):
			# If the file already exists, return a 400 error with a message
			abort(400, "File already downloaded")
        
		# If the file doesn't exist in the downloads directory, download it
		cmd = f"oc rsync podname:/path/{folder}/{file} {downloads} "
		os.system(cmd)
		
		# Remove the downloaded file from the remote server
		cmd = f"oc exec podname rm /app/Encrypted_PTR/{folder}/{file}"
		os.system(cmd)
		
		# Return the downloaded file to the client as an attachment
		return send_file(destination, as_attachment=True)
