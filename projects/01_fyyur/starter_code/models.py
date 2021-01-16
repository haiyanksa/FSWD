from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    # genres = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
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
    # genres = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    shows = db.relationship('Show', backref='Artist', lazy=True)
