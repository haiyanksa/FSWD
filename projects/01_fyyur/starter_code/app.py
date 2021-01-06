#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    #genres_id = db.Column(db.Integer, db.ForeignKey('Genres.id'), nullable=True)
    genres = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    #not sure about the below
    #past_shows_id = db.Column(db.Integer, db.ForeignKey('Show.id'), nullable=True)
    #upcoming_shows_id = db.Column(db.Integer, db.ForeignKey('Show.id'), nullable=True)
    past_shows_count = db.Column(db.Integer, nullable=True)
    upcoming_shows_count = db.Column(db.Integer, nullable=True)
    #is the below different than the above?
    num_upcoming_shows = db.Column(db.Integer, nullable=True)
    shows = db.relationship('Show', backref='Venue', lazy=True)

class Show(db.Model):
    __tablename__= 'Show'
    id = db.Column(db.Integer, primary_key=True)
    #not sure if I will need the below name
    #venue_name = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=True)


#class Genres(db.Model):
#    __tablename__ = 'Genres'
#    id = db.Column(db.Integer, primary_key=True)
#    name = name = db.Column(db.String(), nullable=False)
#    venues = db.relationship('venue', backref='Genre', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='Artist', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #data = Venue.query(Venue.city, Venue.state, Venue.name).all()
  #data = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  #data = db.session.query(Venue.city, Venue.state, [Venue.id, Venue.name] as venues).order_by(Venue.city, Venue.state).all()


  locals = []
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  for place in places:
      locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
        } for venue in venues if
            venue.city == place.city and venue.state == place.state]
      })

  #data = Venue.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  #.group_by("Venue.city", "Venue.state")
  #print('123')
  #print(data)

  #.group_by(Venue.city, Venue.state)

  data1=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]

  #return render_template('pages/venues.html', areas=data);
  return render_template('pages/venues.html', areas=locals);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_form_term = request.form.get('search_term', '')
  print (search_form_term)
  response = db.session.query(Venue.name).filter(Venue.name.contains(search_form_term))
  #response = db.session.query(func.count(Venue.name)).filter(Venue.name.contains(search_form_term)).all()

  #response.count = response.count()
  response1={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data_for_venue_id = db.session.query(Venue.id, Venue.name, Venue.genres, Venue.city, Venue.state, Venue.phone, Venue.website,  Venue.facebook_link, Venue.seeking_talent, Venue.seeking_description, Venue.image_link).filter(Venue.id == venue_id)
  past_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time < datetime.datetime.now())
  upcoming_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time > datetime.datetime.now())
  data = {}
  for entry_item in data_for_venue_id:
       data["id"] = entry_item.id
       data["name"] = entry_item.name
       data["genres"] = entry_item.genres
       data["city"] = entry_item.city
       data["state"] = entry_item.state
       data["phone"] = entry_item.phone
       data["website"] = entry_item.website
       data["facebook_link"] = entry_item.facebook_link
       data["seeking_talent"] = entry_item.seeking_talent
       data["seeking_description"] = entry_item.seeking_description
       data["image_link"] = entry_item.image_link
       data["past_shows"] = [{
         "artist_id" : item.artist_id,
         "artist_name" : item.artist_name,
         "artist_image_link" : item.artist_image_link,
         "start_time" : item.start_time
       } for item in past_shows_of_venue_id if entry_item.id == item.venue_id]
       data["upcoming_shows"] = [{
         "artist_id" : upitem.artist_id,
         "artist_name" : upitem.artist_name,
         "artist_image_link" : upitem.artist_image_link,
         "start_time" : upitem.start_time
       } for upitem in upcoming_shows_of_venue_id if entry_item.id == upitem.venue_id]


  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  #body = {}
  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    genres = request.form.get('genres', '')
    facebook_link = request.form.get('facebook_link', '')
    image_link = request.form.get('image_link', '')
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link)
    db.session.add(venue)
    db.session.commit()

    #description = request.get_json()['description']
    #list_id = request.get_json()['list_id']
    #todo = Todo(description=description)
    #active_list = TodoList.query.get(list_id)
    #todo.list = active_list
    #db.session.add(todo)
    #db.session.commit()
    #body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    #return jsonify(body)
    return render_template('pages/home.html')
  else:
    abort(500)


  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    db.session.query(Venue).filter(Venue.id == venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('Venue ' + str(venue_id) + ' could not be deleted!')
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + str(venue_id) + ' was successfully deleted!')
    #return jsonify(body)
    return render_template('pages/home.html')
    #return None
  else:
    abort(500)

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = db.session.query(Artist.id, Artist.name).all()

  data1=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_form_term = request.form.get('search_term', '')
  print (search_form_term)
  response = db.session.query(Artist.name).filter(Artist.name.contains(search_form_term))

  response1={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')

def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #data_for_artisit_id = db.session.query().filter(Artist.id == artist_id)
  #past_shows_of_artisit_id = db.session.query(Show.venue_id, ).filter(Show.id == artist_id)
  #past_shows_of_artisit_id = db.session.query(Show.venue_id, Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time < datetime.datetime.now())
  #upcoming_shows_of_artisit_id = db.session.query(Show.venue_id, Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time > datetime.datetime.now())
  print (datetime.datetime.now())
  print (datetime.datetime.utcnow())

  #data = []
  data_for_artisit_id = db.session.query(Artist.id, Artist.name, Artist.genres, Artist.city, Artist.state, Artist.phone, Artist.website,  Artist.facebook_link, Artist.seeking_venue, Artist.seeking_description, Artist.image_link).filter(Artist.id == artist_id)
  #print ('data_for_artisit_id: ', data_for_artisit_id)
  past_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time < datetime.datetime.now())
  upcoming_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time > datetime.datetime.now())
  data = {}
  # for entry_item in data_for_artisit_id:
  #     data.append({
  #          "id": entry_item.id,
  #          "name": entry_item.name,
  #          "genres": entry_item.genres,
  #          "city": entry_item.city,
  #          "state": entry_item.state,
  #          "phone": entry_item.phone,
  #          "website": entry_item.website,
  #          "facebook_link": entry_item.facebook_link,
  #          "seeking_venue": entry_item.seeking_venue,
  #          "seeking_description": entry_item.seeking_description,
  #          "image_link": entry_item.image_link
  #       })

  for entry_item in data_for_artisit_id:
       data["id"] = entry_item.id
       data["name"] = entry_item.name
       data["genres"] = entry_item.genres
       data["city"] = entry_item.city
       data["state"] = entry_item.state
       data["phone"] = entry_item.phone
       data["website"] = entry_item.website
       data["facebook_link"] = entry_item.facebook_link
       data["seeking_venue"] = entry_item.seeking_venue
       data["seeking_description"] = entry_item.seeking_description
       data["image_link"] = entry_item.image_link
       data["past_shows"] = [{
         "venue_id" : item.venue_id,
         "venue_name" : item.venue_name,
         "venue_image_link" : item.venue_image_link,
         "start_time" : item.start_time
       } for item in past_shows_of_artisit_id if entry_item.id == item.artist_id]
       data["upcoming_shows"] = [{
         "venue_id" : upitem.venue_id,
         "venue_name" : upitem.venue_name,
         "venue_image_link" : upitem.venue_image_link,
         "start_time" : upitem.start_time
       } for upitem in upcoming_shows_of_artisit_id if entry_item.id == upitem.artist_id]

  # for entry_item in data_for_artisit_id:
  #     data.append({
  #          "id": entry_item.id,
  #          "name": entry_item.name,
  #          "genres": entry_item.genres,
  #          "city": entry_item.city,
  #          "state": entry_item.state,
  #          "phone": entry_item.phone,
  #          "website": entry_item.website,
  #          "facebook_link": entry_item.facebook_link,
  #          "seeking_venue": entry_item.seeking_venue,
  #          "seeking_description": entry_item.seeking_description,
  #          "image_link": entry_item.image_link,
  #          "past_shows": [{
  #            "venue_id": item.venue_id,
  #            "venue_name": item.venue_name,
  #            "venue_image_link": item.venue_image_link,
  #            "start_time": item.start_time
  #          } for item in past_shows_of_artisit_id if entry_item.id == item.artist_id],
  #          "upcoming_shows": [{
  #            "venue_id": upitem.venue_id,
  #            "venue_name": upitem.venue_name,
  #            "venue_image_link": upitem.venue_image_link,
  #            "start_time": upitem.start_time
  #          } for upitem in upcoming_shows_of_artisit_id if entry_item.id == upitem.artist_id]
  #       })

     # for item in past_shows_of_artisit_id:
     #     data.append({
     #       "past_shows": {
     #       "venue_id": item.venue_id,
     #       "venue_name": item.venue_name,
     #       "venue_image_link": item.venue_image_link,
     #       "start_time": item.start_time
     #       } for entry_item in data_for_artisit_id if entry_item.id == item.artist_id
     #     })


 # locals = []
 # venues = Venue.query.all()
 # places = Venue.query.distinct(Venue.city, Venue.state).all()
 # for place in places:
 #     locals.append({
 #       'city': place.city,
 #       'state': place.state,
 #       'venues': [{
 #           'id': venue.id,
 #           'name': venue.name,
 #       } for venue in venues if
 #           venue.city == place.city and venue.state == place.state]
 #     })


  # for item in past_shows_of_artisit_id:
  #     data.append({
  #       "past_shows": {
  #       "venue_id": item.venue_id,
  #       "venue_name": item.venue_name,
  #       "venue_image_link": item.venue_image_link,
  #       "start_time": item.start_time
  #       } for entry_item in data_for_artisit_id if entry_item.id == item.artist_id
  #     })
  # for entry in upcoming_shows_of_artisit_id:
  #     data.append({
  #       "upcoming_shows": {
  #       "venue_id": entry.venue_id,
  #       "venue_name": entry.venue_name,
  #       "venue_image_link": entry.venue_image_link,
  #       "start_time": entry.start_time
  #       } for entry_item in data_for_artisit_id if entry_item.id == entry.artist_id
  #     })

  print ('**** Artist ****')
  print ('data_for_artisit_id: ', data_for_artisit_id)
  print ('**** Past ****')
  print ('past_shows_of_artisit_id: ', past_shows_of_artisit_id)
  print ('**** Upcoming ****')
  print ('upcoming_shows_of_artisit_id: ', upcoming_shows_of_artisit_id)
  print ('**** Count Past ****')
  print ('past_shows_of_artisit_id.count(): ', past_shows_of_artisit_id.count())
  print ('**** Count Upcoming ****')
  print ('upcoming_shows_of_artisit_id.count()', upcoming_shows_of_artisit_id.count())
  print ('**** Overall Data ****')
  print ('data: ', data)
  # print ('**** Overall Data[0] ****')
  # print ('data[0][name]: ', data[0]['name'])
  #print ('data[0].past_shows : ', data[0]['past_shows'])
  # print ('**** Overall data[1][upcoming_shows] ****')
  # print ('data[1].upcoming_shows : ', data[1]['upcoming_shows'])

  # Python3 program to Convert a
  # list to dictionary



  # data.append({
  #   "past_shows_count": past_shows_of_artisit_id.count(),
  #   "upcoming_shows_count": upcoming_shows_of_artisit_id.count()
  # })

  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  # def Convert(a):
  #   it = iter(a)
  #   res_dct = dict(zip(it, it))
  #   return res_dct
  # print ('*********** Convert(data) *********')
  # print (Convert(data))
  return render_template('pages/show_artist.html', artist=data)
  # return render_template('pages/show_artist.html', artist=Convert(data))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data_for_artisit_id = db.session.query(Artist.id, Artist.name, Artist.genres, Artist.city, Artist.state, Artist.phone, Artist.website,  Artist.facebook_link, Artist.seeking_venue, Artist.seeking_description, Artist.image_link).filter(Artist.id == artist_id)
  data ={}
  for entry_item in data_for_artisit_id:
    data["id"] = entry_item.id
    data["name"] = entry_item.name
    data["genres"] = entry_item.genres
    data["city"] = entry_item.city
    data["state"] = entry_item.state
    data["phone"] = entry_item.phone
    data["website"] = entry_item.website
    data["facebook_link"] = entry_item.facebook_link
    data["seeking_venue"] = entry_item.seeking_venue
    data["seeking_description"] = entry_item.seeking_description
    data["image_link"] = entry_item.image_link

  artist1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }

  print ('artist: ', data)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  print ('name: ', request.form.get('name', ''))

  error = False
  try:
    updated_artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    print ('updated_artist: ', updated_artist)
    updated_artist.name = request.form.get('name', '')
    print ('updated_artist.name: ', updated_artist.name)
    updated_artist.city = request.form.get('city', '')
    updated_artist.state = request.form.get('state', '')
    updated_artist.phone = request.form.get('phone', '')
    updated_artist.genres = request.form.get('genres', '')
    updated_artist.facebook_link = request.form.get('facebook_link', '')
    updated_artist.image_link = request.form.get('image_link', '')
    print ('updated_artist: ', updated_artist)
    #updated_artist = db.session.merge(updated_artist)
    #db.session.query(updated_artist).filter(Artist.id == artist_id)
    #db.session.add(updated_artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    #return render_template('pages/home.html')
  else:
    abort(500)


  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    #address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    genres = request.form.get('genres', '')
    facebook_link = request.form.get('facebook_link', '')
    image_link = request.form.get('image_link', '')
    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link)
    db.session.add(artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  else:
    abort(500)


  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.


  data = db.session.query(Show.venue_id, Show.artist_id, Venue.name.label("venue_name"), Artist.name.label("artist_name"), Artist.image_link, Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).all()
  #data = db.session.query(Show, Venue, Artist).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).all()
  print(type(str(Show.start_time)))
  print(Show.start_time)




  data1=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  try:
    artist_id = request.form.get('artist_id', '')
    venue_id = request.form.get('venue_id', '')
    start_time = request.form.get('start_time', '')

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    #flash('Artist ' + request.form['name'] + ' was successfully listed!')
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  else:
    abort(500)



  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
