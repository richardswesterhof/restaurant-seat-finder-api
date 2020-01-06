from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    house_number = db.Column(db.String(20))
    postcode = db.Column(db.String(10))  # the longest postcode is 10 chars
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    # Coordinate Latitude
    coord_lat = db.Column(db.Float())
    # Coordinate Longitude
    coord_lon = db.Column(db.Float())
    # Attributes of Address for creation, update and retrieve
    address_attrs = ['street', 'house_number', 'postcode', 'city', 'country', 'coord_lat', 'coord_lon']

    def to_dict(self) -> dict:
        """
         :return: Dict that contain only attributes with needed information
        """
        res = {}
        for attr in self.address_attrs:
            res[attr] = getattr(self, attr)
        # res = self.__dict__
        return res


class Place(db.Model):
    # --- Login ---
    username = db.Column(db.String(32), unique=True)
    # TODO add hashing!
    password = db.Column(db.String(128))
    # --- ---
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    # TODO cuisine = db.Column(db.String(255))
    type = db.Column(db.String(50), default='other')  # Can be: restaurant, cafe, bar, fast food, fast casual, other
    # TODO place_types = ['restaurant']
    total_seats = db.Column(db.Integer)
    free_seats = db.Column(db.Integer, default=0)
    email = db.Column(db.String(50))
    website = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    # One to one relationship with address
    address_id = db.Column(db.Integer, db.ForeignKey(Address.id))
    address = db.relationship(Address, backref='place', uselist=False)
    # Attributes of Place for creation, update and retrieve
    place_attrs = ['name', 'description', 'type', 'total_seats', 'free_seats', 'email', 'website', 'phone_number']
    additional_update_attrs = ['username', 'password']
    # Or try to use self.__table__.columns.keys()

    def to_dict(self) -> dict:
        """
        :return: Dict that contain only attributes with needed information
        """
        # + id and address
        res = {'id': self.id, 'address': self.address.to_dict()}
        for attr in self.place_attrs:
            res[attr] = getattr(self, attr)
        return res

    def update_info(self, data: dict):
        """
            Updates place with information given in json
            :param data: json with data
            :return: Place id
            :exception possible KeyError or TypeError if something is wrong with data
            """
        address = self.address
        # TODO check for data types - for now we suppose that all coming data is correct
        for attr in data.keys():
            # Setting all attributes
            if attr in (Place.place_attrs + Place.additional_update_attrs):
                setattr(self, attr, data[attr])
                # setattr(new_place, attr, None)
        if 'address' in data:
            for attr in data['address'].keys():
                # Setting all attributes
                if attr in Address.address_attrs:
                    setattr(address, attr, data['address'][attr])
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id

    def delete(self):
        """
        Deletes place from database
        :return: id
        """
        Address.query.filter_by(id=self.address.id).delete()
        Place.query.filter_by(id=self.id).delete()
        db.session.commit()
        return self.id
