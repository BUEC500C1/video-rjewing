import uuid

from flask import jsonify

from config import Config
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from worker import work_progress, work_queue


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
        return jsonify({"response": f"Creating video named {video_id}.{args['format']}.", 
                        "display_url": f"http://{Config.API_PUBLIC_IP}:{Config.API_PORT}/display/{video_id}",
                        "progress_url": f"http://{Config.API_PUBLIC_IP}:{Config.API_PORT}/progress/{video_id}"})


class VideoProgress(Resource):
    def get(self, video_id):
        return work_progress[video_id]
