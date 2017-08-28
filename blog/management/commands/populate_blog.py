from django.core.management.base import BaseCommand, CommandError
from dj_blog.settings import BASE_DIR

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

        print(content)

    def _load_file(self,path):
        file_json = open(path)
        file_content = json.load(file_json)

        return file_content

    def _verify_json_file(self,json_file):
        return os.path.lexists(json_file) and os.path.isfile(json_file)

    def _handle_users(self,data):
        pass

    def _handle_posts(self,data):
        pass
