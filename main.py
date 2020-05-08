# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import jsonify
from google.cloud import storage
from flask import request
import werkzeug
import os
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print("Bucket {} created".format(bucket.name))

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    storage_client = storage.Client()
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        blob.make_public()
        print(blob.public_url)

def upload_image_to_cloud_storage(bucket_name, source_file_name, destination_blob_name, content_type):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name, content_type = content_type)
    blob.make_public()
    return blob.public_url

@app.route('/getLatestStories')
def getLatestStories():
    """Return a friendly HTTP greeting."""
    list_blobs("storia-temp1")
    return jsonify(["https://i.redd.it/v0zdmwnifvw21.jpg",
                    "https://cdn.wallpapersafari.com/37/67/zEny8K.jpg"])

@app.route('/uploadStory', methods = ['GET', 'POST'])
def uploadStory():
    """Return a friendly HTTP greeting."""
    uploaded_story_image_file = request.files['storia_image']
    uploaded_story_image_filename = werkzeug.utils.secure_filename(uploaded_story_image_file.filename)
    storage_client = storage.Client()
    bucket = storage_client.bucket("storia-temp1")
    blob = bucket.blob(uploaded_story_image_filename)
    blob.upload_from_string(
        uploaded_story_image_file.read(),
        content_type=uploaded_story_image_file.content_type
    )
    blob.make_public()
    return blob.public_url

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
