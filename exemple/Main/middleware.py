class CorsPreFlightCheckMiddleware(object):

    """
    Pre flight check for CORS request. You can also extend this to
    add domain validation.
    """

    def process_request(self, request):
        '''
        If CORS preflight header, then create an empty body response
       (200 OK) and return it

       Django won't bother calling any other request view/exception
       middleware along with the requested view; it will call
       any response middlewares.
        '''
        print(1)
        if (request.method == 'OPTIONS' and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):
            return http.HttpResponse()

        return None

    def process_response(self, request, response):
        '''
        Add the respective CORS headers for pre-flight check
        '''
        print(1)
        #only do this in case of 'OPTIONS' request.
        if (request.method == 'OPTIONS' and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):

            #default entries
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

            #extract the client API Key
            response['Access-Control-Allow-Origin'] = '*'

        return response