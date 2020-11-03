from flask import Response, request,render_template,make_response
from database.models import Movie
from flask_restful import Resource

class MoviesApi(Resource):
    def get(self):
        movies = Movie.objects().to_json()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)

    def post(self):
        body = request.get_json()
        movie= Movie(**body).save()
        id=movie.id 
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)


class MovieApi(Resource):
    def put(self,id):
        body = request.get_json()
        Movie.objects.get(id=id).update(**body)
        return '',200

    def delete(self, id):
        movie = Movie.objects.get(id=id).delete()
        return '', 200

    def get(self, id):
        movies = Movie.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)