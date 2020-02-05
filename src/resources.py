from flask_restful import Resource

from webargs import fields
from webargs.flaskparser import use_args

import uuid


class TwitterSummarizer(Resource):
    def __init__(self, q):
        self.q = q

    @use_args({"user": fields.Str(required=True)})
    def get(self, args):
        video_filename = args['user'] + '-' + uuid.uuid4().hex
        self.q.put((video_filename, args['user']))
        self.q.join()
        return {"response": f"Created video named {video_filename}.ogg.", "url": f"localhost:5000/display/{video_filename}"}, 200
