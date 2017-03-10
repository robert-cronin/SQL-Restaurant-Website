from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_query import query, commit
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = query("SELECT name, id FROM Restaurant")
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'> Make a new restaurant here </a><br></br>"
                output += "<table>"
                for restaurant in restaurants:
                    output += "<tr>"
                    output += "<td>%s</td>"%restaurant[0]
                    output += "<td><a href='/restaurants/%s/edit'>Edit</a></td>"%restaurant[1]
                    output += "<td><a href='/restaurants/%s/delete'>Delete</a></td>"%restaurant[1]
                    output += "</tr>"
                    output += "<tr></tr>"
                output += "</table>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = query("SELECT name FROM Restaurant WHERE id = %s"%restaurantIDPath)
                for name in myRestaurantQuery:
                    name = name
                name = str(name[0])
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Current Restaurant Name: %s</h1>"%name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>"%restaurantIDPath
                    output += "<input name='editRestaurantName' type='text' placeholder='%s'>"%name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</html></body>"
                    self.wfile.write(output)
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
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = query("SELECT name FROM Restaurant WHERE id = %s"%restaurantIDPath)
                for name in myRestaurantQuery:
                    name = name
                name = str(name[0])
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Are you sure you want to delete %s ?</h1>"%name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>"%restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"
                    output += "</html></body>"
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.end_headers()

                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                output = ""
                output += "<html><body>"
                output += "<h2> New restaurant name: </h2>"
                output += "<h3> %s </h3>" % messagecontent[0]
                output += "<a href='/restaurants'>Return to Restaurants</a>"
                output += "</html></body>"
                commit("INSERT into Restaurant (name) VALUES ('%s')"%messagecontent[0])
                self.wfile.write(output)

            if self.path.endswith("/edit"):
                self.send_response(301)
                self.end_headers()
                restaurantIDPath = self.path.split("/")[2]

                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('editRestaurantName')

                output = ""
                output += "<html><body>"
                output += "<h2> Renamed restaurant name: </h2>"
                output += "<h3> %s </h3>" % messagecontent[0]
                output += "<a href='/restaurants'>Return to Restaurants</a>"
                output += "</html></body>"
                commit("UPDATE Restaurant SET name='%s' WHERE id=%s"%(messagecontent[0], restaurantIDPath))
                self.wfile.write(output)

            if self.path.endswith("/delete"):
                self.send_response(301)
                self.end_headers()
                restaurantIDPath = self.path.split("/")[2]

                output = ""
                output += "<html><body>"
                output += "<h2>Restaurant Deleted!</h2>"
                output += "<a href='/restaurants'>Return to Restaurants</a>"
                output += "</html></body>"
                commit("DELETE FROM Restaurant WHERE id=%s"%restaurantIDPath)
                self.wfile.write(output)

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
