import falcon
from falcon_jinja2 import FalconTemplate
from src import api

falcon_template = FalconTemplate()


class IndexResource:
    @falcon_template.render('index.html')
    def on_get(self, req, resp):
        photos = api.get_photos()
        resp.context = {'photoA': photos[0], 'photoB': photos[1]}


class VoteResource:
    def on_get(self, req, resp):
        photo_id = req.params['id']
        api.add_winner(photo_id)
        raise falcon.HTTPTemporaryRedirect('/')


app = falcon.API()
app.add_route('/', IndexResource())
app.add_route('/vote', VoteResource())
api.init()
