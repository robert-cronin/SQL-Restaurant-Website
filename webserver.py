from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_query import query
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = query("SELECT name FROM Restaurant")
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'> Make a new restaurant here </a><br></br>"
                output += "<table>"
                for restaurant in restaurants:
                    output += "<tr>"
                    output += "<td>%s</td>"%restaurant[0]
                    output += "<td><form enctype='multipart/form-data' action='/restaurants/edit'>edit</form></td>"
                    output += "<td><form href='/restaurants/delete/'>delete</form></td>"
                    output += "</tr>"
                output += "</table>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161 Hola ! <a href = '/hello' > Back to Hello"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Add a new restaurant name here</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += "</html></body>"
            self.wfile.write(output)
            print output
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s"%port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socker.close()

if __name__ == '__main__':
    main()
