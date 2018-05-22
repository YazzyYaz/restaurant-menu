from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                with session_scope() as session:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Add New Restaurant  <a href='/restaurants'>Go Back</a></h2>"
                    output += """<form method='POST' enctype='multipart/form-data' action='new-restaurant'>
                            <h2>Restaurant</h2><input name='name' type='text'>
                            <input type='submit' value='Submit'></form>"""
                    output += "</body></html>"
                    self.wfile.write(output.encode("utf-8"))
                    print(output)
                    return
            if self.path.endswith("/restaurants"):
                with session_scope() as session:

                    restaurants = session.query(Restaurant).all()
                    print(restaurants)
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h2><a href='/restaurants/new'>Add a Restaurant</a></h2><br>"
                    for restaurant in restaurants:
                        output += restaurant.name
                        output += f"<br><a href='/edit/{restaurant.id}'>Edit</a>"
                        output += f"<br><a href='/delete/{restaurant.id}'>Delete</a>"
                        output += "</br></br></br>"
                    output += "</body></html>"
                    self.wfile.write(output.encode("utf-8"))
                    print(output)
                    return
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                with session_scope() as session:
                    self.send_response(301)
                    self.end_headers()
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == "multipart/form-data":
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        restaurant_content = fields.get('name')
                    new_restaurant = Restaurant(name=f"{restaurant_content[0]}")
                    session.add(new_restaurant)
                    session.commit()


            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2>Ok, How about this?</h2>"
            output += "<h1> {} </h1>".format(messagecontent[0])
            output += """<form method='POST' enctype='multipart/form-data' action='hello'>
                      <h2>What would you like me to say?</h2><input name='message' type='text'>
                      <input type='submit' value='Submit'></form>"""
            output += "</body></html>"
            self.wfile.write(output.encode("utf-8"))
            print(output)


        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C Entered, stopping web server...")
        server.socket.close()


@contextmanager
def session_scope():
    engine = create_engine("sqlite:///restaurantmenu.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()
