from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

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
            raise CommandError("The path is invalid. Verify the path and use a file with format json.")

        content = self._load_file(file_path)

        users = content.get("users")
        posts = content.get("posts")
        comments = content.get("comments")

        self.stdout.write("Loading Users data...")

        for user in users:

            try:
                geo = self._handle_geo(user)

                address = self._handle_address(user, geo)

                self._handle_users(user, address)

            except IntegrityError:
                raise CommandError("Data already was loaded previously.")
        else:
            self.stdout.write("Inserted {} users.".format(User.objects.all().count()))


        self.stdout.write("Loading Posts data...")

        for post in posts:

            user_id = post.get("userId")

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise CommandError("User doesn't exist. Insert before the related User. Id = {}".format(user_id))

            try:
                
                self._handle_posts(post, user)

            except IntegrityError:
                raise CommandError("Data already was loaded previously.")
        else:
            self.stdout.write("Inserted {} posts.".format(Post.objects.all().count()))

        self.stdout.write("Loading Comments data...")

        for comment in comments:
            
            post_id = comment.get("postId")
            
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                raise CommandError("Post doesn't exist. Insert before the related Post. Id: {}".format(post_id))

            try:
                
                self._handle_comments(comment, post)

            except IntegrityError:
                raise CommandError("Data already was loaded previously.")
        else:
            self.stdout.write("Inserted {} comments.".format(Comment.objects.all().count()))
            
        self.stdout.write("Data from {} was loaded successful.".format(filename))


    def _load_file(self,path):
        file_json = open(path)
        file_content = json.load(file_json)

        return file_content

    def _verify_json_file(self,json_file):
        return os.path.lexists(json_file) and os.path.isfile(json_file)

    def _handle_posts(self,data_object, dependence):

        post_data = {
            "title": data_object.get("title"),
            "body": data_object.get("body"),
        }

        post_data["user"] = dependence

        Post.objects.create(**post_data)


    def _handle_comments(self,data_object, dependence):
        
        comment_data = {
            "pk": data_object.get("id"),
            "name": data_object.get("name"),
            "email": data_object.get("email"),
            "body": data_object.get("body"),
        }

        comment_data["post"] = dependence

        Comment.objects.create(**comment_data)

    def _handle_users(self, data_object, dependence):
        
        user_data = {
            "pk": data_object.get("id"),
            "name": data_object.get("name"),
            "email": data_object.get("email"),
        }

        user_data["address"] = dependence

        return User.objects.create(**user_data)

    def _handle_address(self, data_object, dependence):
        
        address_data = {
            "pk": data_object.get("address").get("id"),
            "street": data_object.get("address").get("street"),
            "suite": data_object.get("address").get("suite"),
            "city": data_object.get("address").get("city"),
            "zipcode": data_object.get("address").get("zipcode")
        }

        address_data["geo"] = dependence

        return Address.objects.create(**address_data)

    def _handle_geo(self, data_object):

        geo_data = {
            "pk": data_object.get("address").get("geo").get("id"),
            "latitude": data_object.get("address").get("geo").get("lat"),
            "longitude": data_object.get("address").get("geo").get("lng")
        }

        return Geo.objects.create(**geo_data)
