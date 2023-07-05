from controllers.godtrack import GodTrack

from flask import jsonify


class Routes:
    def index(self):
        return (jsonify(dict(
            status=200,
            message="OK"
        )), 200)


def register_routes(server):
    routes = Routes()
    godtrack = GodTrack()

    server.register_routes('/', 'index', routes.index)
    server.register_routes('/godtrack', 'godtrack',
                           godtrack.facebook_group_scraper)
