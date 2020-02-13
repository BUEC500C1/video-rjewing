from flask_restful import Resource
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from worker import work_queue, work_progress
from config import Config
import uuid


class TwitterSummarizer(Resource):
    @use_args({"user": fields.Str(required=True),
               "format": fields.Str(required=False, missing='ogg'),
               "email": fields.Str(required=False, missing=None)
               })
    def get(self, args):
        video_id = args['user'] + '-' + uuid.uuid4().hex
        work_progress[video_id] = {
            "video_id": video_id,
            "status": "In queue",
            "finished": False
        }
        work_queue.put((video_id, args['user'], args['email'], args['format']))
        return jsonify({"response": f"Created video named {video_id}.{args['format']}.", "url": f"http://{Config.API_PUBLIC_IP}:{Config.API_PORT}/progress/{video_id}"})


class VideoProgress(Resource):
    def get(self, video_id):
        return work_progress[video_id]
