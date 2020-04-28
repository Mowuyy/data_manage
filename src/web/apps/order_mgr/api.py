# -*- coding: utf-8 -*-

from flask import current_app

from ..custom_views import APIView


class OrderUpload(APIView):

    def post(self, request):
        for key, value in request.req_args.items():
            print(key, value)

        print(current_app.db)
        return request.req_args






