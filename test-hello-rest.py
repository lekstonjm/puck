#!/usr/bin/env python
import web

urls = (
    '/hello/(.*)', 'hello'
)

app = web.application(urls, globals())

class hello:        
    def GET(self, user):
        output  = '{response:"hello'+user+'"}';
        return output

if __name__ == "__main__":
    app.run()