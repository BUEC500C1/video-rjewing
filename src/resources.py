from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from worker import create_twitter_video

import uuid


class TwitterSummarizer(Resource):
    def __init__(self, p):
        self.p = p

    @use_args({"user": fields.Str(required=True)})
    def get(self, args):
        video_filename = args['user'] + '-' + uuid.uuid4().hex
        self.p.apply(create_twitter_video, args=(video_filename, args['user']))
        return {"response": f"Created video named {video_filename}.ogg.", "url": f"localhost:5000/display/{video_filename}"}, 200
