
# Django core imports
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# Applications imports
from dj_blog.settings import BASE_DIR, DATABASES

from blog.models import Geo, Address, Post, Comment, Profile

# Built-in libs import
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

        self._clean_db()

        filename = options.get("filename")

        if type(options.get("filename")) == list:
            filename = options.get("filename")[0]

        file_path = os.path.join(BASE_DIR,filename)

        if not self._verify_json_file(file_path):
            raise CommandError("The path is invalid. Verify the path and use a file with format json.")

        content = self._load_file(file_path)

        profiles = content.get("users")
        posts = content.get("posts")
        comments = content.get("comments")

        self.stdout.write("Loading Profile data...")

        for profile in profiles:

            geo = self._handle_geo(profile)

            address = self._handle_address(profile, geo)

            self._handle_profiles(profile, address)

        else:
            self.stdout.write("Inserted {} profiles.".format(Profile.objects.all().count()))


        self.stdout.write("Loading Posts data...")

        for post in posts:

            profile_id = post.get("userId")

            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                raise CommandError("Profile doesn't exist. Insert before the related Profile. Id = {}".format(profile_id))

            self._handle_posts(post, profile)

        else:
            self.stdout.write("Inserted {} posts.".format(Post.objects.all().count()))

        self.stdout.write("Loading Comments data...")

        for comment in comments:
            
            post_id = comment.get("postId")

            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                raise CommandError("Post doesn't exist. Insert before the related Post. Id: {}".format(post_id))
                
            self._handle_comments(comment, post)

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
            "pk": data_object.get("id"),
            "title": data_object.get("title"),
            "body": data_object.get("body"),
            "profile": dependence
        }

        return Post.objects.create(**post_data)


    def _handle_comments(self,data_object, dependence):
        
        comment_data = {
            "pk": data_object.get("id"),
            "name": data_object.get("name"),
            "email": data_object.get("email"),
            "body": data_object.get("body"),
            "post": dependence
        }

        return Comment.objects.create(**comment_data)

    def _handle_profiles(self, data_object, dependence):
        
        name = data_object.get("name").strip()

        for part in name.split():
            if part in ["Mrs.","Mr."] or len(part) <= 3:
                name = name.replace(part,"")

        name = name.strip().split()

        first_name = name[0]
        last_name = name[-1]

        user_data = {
            "pk": data_object.get("id"),
            "username" : data_object.get("username"),
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : data_object.get("email")
        }

        #Passing the user dictionary
        user = User(**user_data)
        user.set_password(user.username + "2017")

        user.save()

        return Profile.objects.create(id=user_data["pk"],
                                      user=user,
                                      address=dependence)

    def _handle_address(self, data_object, dependence):
        
        address_data = {
            "pk": data_object.get("address").get("id"),
            "street": data_object.get("address").get("street"),
            "suite": data_object.get("address").get("suite"),
            "city": data_object.get("address").get("city"),
            "zipcode": data_object.get("address").get("zipcode"),
            "geo": dependence
        }

        return Address.objects.create(**address_data)

    def _handle_geo(self, data_object):

        geo_data = {
            "pk": data_object.get("address").get("geo").get("id"),
            "latitude": data_object.get("address").get("geo").get("lat"),
            "longitude": data_object.get("address").get("geo").get("lng")
        }

        return Geo.objects.create(**geo_data)

    def _clean_db(self):

        database_path = DATABASES.get("default").get("NAME")

        if os.path.exists(database_path):
            os.remove(database_path)
            
        call_command("migrate")
