from django.core.management.base import BaseCommand, CommandError
from dj_blog.settings import BASE_DIR

from blog.models import Geo, Address, User, Post, Comment

import os
import json

class Command(BaseCommand):

    help = "Import a specific data from json"

    def add_arguments(self,parser):

        parser.add_argument(
            '--filename',
            nargs=1,
            dest="filename",
            type=str,
            default="db.json",
            help="Filename from json to be loaded. Located at the root of the project.")

    def handle(self,*args,**options):

        filename = options.get("filename")

        if type(options.get("filename")) == list:
            filename = options.get("filename")[0]

        file_path = os.path.join(BASE_DIR,filename)

        if not self._verify_json_file(file_path):
            raise CommandError("The path is invalid. Verify the path.")

        content = self._load_file(file_path)

        users = content.get("users")
        posts = content.get("posts")
        comments = content.get("comments")

        for user in users:

            geo_data = {
                "latitude": user.get("address").get("geo").get("lat"),
                "longitude": user.get("address").get("geo").get("lng")
            }

            address_data = {
                "street": user.get("address").get("street"),
                "suite": user.get("address").get("suite"),
                "city": user.get("address").get("city"),
                "zipcode": user.get("address").get("zipcode")
            }

            user_data = {
                "name": user.get("name"),
                "email": user.get("email"),
            }

            geo_object = self._handle_geo(geo_data)

            address_object = self._handle_address(address_data, geo_object)

            user_object = self._handle_users(user_data, address_object)

        for post in posts:
            pass

        for comment in comments:
            pass

    def _load_file(self,path):
        file_json = open(path)
        file_content = json.load(file_json)

        return file_content

    def _verify_json_file(self,json_file):
        return os.path.lexists(json_file) and os.path.isfile(json_file)

    def _handle_posts(self,data_object, dependence):
        pass

    def _handle_comments(self,data_object, dependence):
        pass

    def _handle_users(self, data_object, dependence):
        
        data_object["address"] = dependence

        return User.objects.create(**data_object)

    def _handle_address(self, data_object, dependence):
        
        data_object["geo"] = dependence

        return Address.objects.create(**data_object)

    def _handle_geo(self, data_object):
        return Geo.objects.create(**data_object)
