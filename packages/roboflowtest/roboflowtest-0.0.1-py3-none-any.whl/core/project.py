import base64
import io
import json
import os
import urllib
import datetime
import warnings
import cv2
import requests
from PIL import Image
from roboflow.config import *
from roboflow.core.version import Version

#version class that should return
class Project():
    def __init__(self, api_key, a_project):
        self.__api_key = api_key
        self.annotation = a_project['annotation']
        self.classes = a_project['classes']
        self.colors = a_project['colors']
        self.created = datetime.datetime.fromtimestamp(a_project['created'])
        self.id = a_project['id']
        self.images = a_project['images']
        self.name = a_project['name']
        self.public = a_project['public']
        self.splits = a_project['splits']
        self.type = a_project['type']
        self.unannotated = a_project['unannotated']
        self.updated = datetime.datetime.fromtimestamp(a_project['updated'])

        temp = self.id.rsplit("/")
        self.__workspace = temp[0]
        self.__project_name = temp[1]

    def get_version_information(self):
        dataset_info = requests.get(API_URL + "/" + self.__workspace + "/" + self.__project_name + "?api_key=" + self.__api_key)

        # Throw error if dataset isn't valid/user doesn't have permissions to access the dataset
        if dataset_info.status_code != 200:
            raise RuntimeError(dataset_info.text)

        dataset_info = dataset_info.json()
        return dataset_info['versions']

    def list_versions(self):
        version_info = self.get_version_information()
        print(version_info)

    def versions(self):
        version_info = self.get_version_information()
        version_array = []
        for a_version in version_info:
            version_object = Version(a_version, (self.type if 'model' in a_version else None), self.__api_key, self.name, a_version['id'], local=False)
            version_array.append(version_object)
        return version_array

    def version(self, version_number):

        version_info = self.get_version_information()

        for version_object in version_info:

            current_version_num = os.path.basename(version_object['id'])
            if current_version_num == str(version_number):
                vers = Version(version_object, self.type, self.__api_key, self.name, current_version_num, local=False)
                return vers

        raise RuntimeError("Version number {} is not found.".format(version_number))

    def __image_upload(self, image_path, hosted_image=False, split="train"):

        # If image is not a hosted image
        if not hosted_image:

            project_name = self.id.rsplit("/")[1]
            image_name = os.path.basename(image_path)

            # Construct URL for local image upload

            self.image_upload_url = "".join([
                "https://api.roboflow.com/dataset/", project_name, "/upload",
                "?api_key=", self.__api_key,
                "&name=" + image_name,
                "&split=" + split
            ])

            # Convert to PIL Image
            img = cv2.imread(image_path)
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            pilImage = Image.fromarray(image)
            # Convert to JPEG Buffer
            buffered = io.BytesIO()
            pilImage.save(buffered, quality=100, format="JPEG")
            # Base 64 Encode
            img_str = base64.b64encode(buffered.getvalue())
            img_str = img_str.decode("ascii")
            # Post Base 64 Data to Upload API

            response = requests.post(self.image_upload_url, data=img_str, headers={
                "Content-Type": "application/x-www-form-urlencoded"
            })


        else:
            # Hosted image upload url
            project_name = self.id.rsplit("/")[1]

            upload_url = "".join([
                "https://api.roboflow.com/dataset/" + self.project_name + "/upload",
                "?api_key=" + self.__api_key,
                "&name=" + os.path.basename(image_path),
                "&split=" + split,
                "&image=" + urllib.parse.quote_plus(image_path)
            ])
            # Get response
            response = requests.post(upload_url)
        # Return response

        return response

    def __annotation_upload(self, annotation_path, image_id):
        # Get annotation string
        annotation_string = open(annotation_path, "r").read()
        # Set annotation upload url
        self.annotation_upload_url = "".join([
            "https://api.roboflow.com/dataset/", self.name, "/annotate/", image_id,
            "?api_key=", self.__api_key,
            "&name=" + os.path.basename(annotation_path)
        ])
        # Get annotation response
        annotation_response = requests.post(self.annotation_upload_url, data=annotation_string, headers={
            "Content-Type": "text/plain"
        })
        # Return annotation response
        return annotation_response

    def upload(self, image_path=None, annotation_path=None, hosted_image=False, image_id=None, split='train'):
        success = False
        # User gives image path
        if image_path is not None:
            # Upload Image Response
            response = self.__image_upload(image_path, hosted_image=hosted_image, split=split)
            # Get JSON response values
            try:
                success, image_id = response.json()['success'], response.json()['id']
            except Exception:
                # Image fails to upload
                success = False
            # Give user warning that image failed to upload
            if not success:
                warnings.warn("Image, " + image_path + ", failed to upload!")

            # Check if image uploaded successfully + check if there are annotations to upload
            if annotation_path is not None and image_id is not None and success:
                # Upload annotation to API
                annotation_response = self.__annotation_upload(annotation_path, image_id)
                try:
                    success = annotation_response.json()['success']
                except Exception:
                    success = False
            # Give user warning that annotation failed to upload
            if not success:
                warnings.warn("Annotation, " + annotation_path + ", failed to upload!")
        # Upload only annotations to image based on image Id (no image)
        elif annotation_path is not None and image_id is not None:
            # Get annotation upload response
            annotation_response = self.__annotation_upload(annotation_path, image_id)
            # Check if upload was a success
            try:
                success = annotation_response.json()['success']
            except Exception:
                success = False
        # Give user warning that annotation failed to upload
        if not success:
            warnings.warn("Annotation, " + annotation_path + ", failed to upload!")

    def __str__(self):
        # String representation of project
        json_str = {
            "name": self.name,
            "type": self.type,
            "workspace": self.__workspace,
        }

        return json.dumps(json_str, indent=2)
