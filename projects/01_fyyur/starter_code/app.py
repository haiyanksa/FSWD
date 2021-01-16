#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request, Response,
    flash,
    redirect,
    url_for,
    abort
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from models import db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://haiyanalsaiyed@localhost:5432/fyyur'

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



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


  #return render_template('pages/venues.html', areas=data);
  return render_template('pages/venues.html', areas=locals);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_form_term = request.form.get('search_term', '')
  print (search_form_term)
  #response = db.session.query(Venue.name).filter(Venue.name.contains(search_form_term))
  # use ilike("%" + search_form_term + "%") instead of contains(search_form_term) as it's not a case sensitive
  response = db.session.query(Venue.name).filter(Venue.name.ilike("%" + search_form_term + "%"))


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data_for_venue_id = db.session.query(Venue.id, Venue.name, Venue.genres, Venue.city, Venue.state, Venue.phone, Venue.website,  Venue.facebook_link, Venue.seeking_talent, Venue.seeking_description, Venue.image_link).filter(Venue.id == venue_id)
  #past_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time < datetime.now())
  past_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Venue.id == venue_id, Show.start_time < datetime.now()).all()
  #upcoming_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time > datetime.now())
  upcoming_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Venue.id == venue_id, Show.start_time > datetime.now()).all()
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
       data["past_shows_count"] : len(past_shows_of_venue_id)
       data["upcoming_shows_count"]: len(upcoming_shows_of_venue_id)


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
  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    #please note that genres = request.form.get does NOT work. We have to use getlist
    genres = request.form.getlist('genres')
    print ('Venue genres:>>>>>>>> ', genres)
    facebook_link = request.form.get('facebook_link', '')
    image_link = request.form.get('image_link', '')
    website = request.form.get('website', '')
    if request.form.get('seeking_talent'):
        seeking_talent = True
    else:
        seeking_talent = False
    seeking_description = request.form.get('seeking_description', '')
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
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
  print (datetime.now())
  print (datetime.utcnow())

# data_for_venue_id = db.session.query(Venue.id, Venue.name, Venue.genres, Venue.city, Venue.state, Venue.phone, Venue.website,  Venue.facebook_link, Venue.seeking_talent, Venue.seeking_description, Venue.image_link).filter(Venue.id == venue_id)
# #past_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time < datetime.now())
# past_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Venue.id == venue_id, Show.start_time < datetime.now()).all()
# #upcoming_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Venue.id == venue_id).filter(Show.start_time > datetime.now())
# upcoming_shows_of_venue_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link"), Show.start_time).join(Show).join(Venue).filter(Show.venue_id == venue_id, Show.artist_id == Artist.id, Venue.id == venue_id, Show.start_time > datetime.now()).all()




  data_for_artisit_id = db.session.query(Artist.id, Artist.name, Artist.genres, Artist.city, Artist.state, Artist.phone, Artist.website,  Artist.facebook_link, Artist.seeking_venue, Artist.seeking_description, Artist.image_link).filter(Artist.id == artist_id)
  #past_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time < datetime.now())
  past_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).join(Show).join(Artist).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time < datetime.now())

  #upcoming_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time > datetime.now())
  upcoming_shows_of_artisit_id = db.session.query(Show.venue_id, Show.artist_id.label("artist_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link"), Show.start_time).join(Show).join(Artist).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).filter(Show.id == artist_id).filter(Show.start_time > datetime.now())

  data = {}

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
       data["past_shows_count"] : len(past_shows_of_artisit_id)
       data["upcoming_shows_count"]: len(upcoming_shows_of_artisit_id)





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


  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  return render_template('pages/show_artist.html', artist=data)

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
    #please note that genres = request.form.get does NOT work. We have to use getlist
    updated_artist.genres = request.form.getlist('genres')
    updated_artist.facebook_link = request.form.get('facebook_link', '')
    updated_artist.image_link = request.form.get('image_link', '')
    updated_artist.website = request.form.get('website', '')
    if request.form.get('seeking_venue'):
        updated_artist.seeking_venue = True
    else:
        updated_artist.seeking_venue = False
    updated_artist.seeking_description = request.form.get('seeking_description', '')
    print ('updated_artist: ', updated_artist)
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

  data_for_venue_id = db.session.query(Venue.id, Venue.name, Venue.address, Venue.genres, Venue.city, Venue.state, Venue.phone, Venue.website,  Venue.facebook_link, Venue.seeking_talent, Venue.seeking_description, Venue.image_link).filter(Venue.id == venue_id)
  data ={}
  for entry_item in data_for_venue_id:
    data["id"] = entry_item.id
    data["name"] = entry_item.name
    data["genres"] = entry_item.genres
    data["address"] = entry_item.address
    data["city"] = entry_item.city
    data["state"] = entry_item.state
    data["phone"] = entry_item.phone
    data["website"] = entry_item.website
    data["facebook_link"] = entry_item.facebook_link
    data["seeking_talent"] = entry_item.seeking_talent
    data["seeking_description"] = entry_item.seeking_description
    data["image_link"] = entry_item.image_link


  # TODO: populate form with values from venue with ID <venue_id>

  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  error = False
  try:
    updated_venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    print ('updated_venue: ', updated_venue)
    updated_venue.name = request.form.get('name', '')
    print ('updated_venue.name: ', updated_venue.name)
    updated_venue.city = request.form.get('city', '')
    updated_venue.address = request.form.get('address', '')
    updated_venue.state = request.form.get('state', '')
    updated_venue.phone = request.form.get('phone', '')
    #please note that genres = request.form.get does NOT work. We have to use getlist
    updated_venue.genres = request.form.getlist('genres')
    updated_venue.facebook_link = request.form.get('facebook_link', '')
    updated_venue.image_link = request.form.get('image_link', '')
    updated_venue.website = request.form.get('website', '')
    if request.form.get('seeking_talent'):
        updated_venue.seeking_talent = True
    else:
        updated_venue.seeking_talent = False
    updated_venue.seeking_description = request.form.get('seeking_description', '')
    print ('updated_venue: ', updated_venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    #return render_template('pages/home.html')
  else:
    abort(500)





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
    #please note that genres = request.form.get does NOT work. We have to use getlist
    genres = request.form.getlist('genres')
    print ('Artist genres:>>>>>>: ', genres)
    facebook_link = request.form.get('facebook_link', '')
    image_link = request.form.get('image_link', '')
    website = request.form.get('website', '')
    if request.form.get('seeking_venue'):
        seeking_venue = True
    else:
        seeking_venue = False
    seeking_description = request.form.get('seeking_description', '')
    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
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
  print(type(str(Show.start_time)))
  print(Show.start_time)

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
