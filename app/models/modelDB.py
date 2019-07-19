from flask import Flask, render_template, request, url_for, redirect

class Company(db.Model):
     __tablename__ = 'company'
     
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(60), index=True, unique=True)
     owner = db.Column(db.String(60), index=True, unique=True)
     cnpj = db.Column(db.String(22), index=True, unique=True)
     email = db.Column(db.String(60), index=True, unique=True)
     address = db.Column(db.String(60), index=True, unique=True)
     city = db.Column(db.String(60), index=True, unique=True)
     state = db.Column(db.String(60), index=True, unique=True)
     cep = db.Column(db.String(60), index=True, unique=True)       
     password_hash = db.Column(db.String(128))

     def __init__(self, name, owner, cnpj, email, address, city, state, cep, password):
          self.name = name
          self.owner = owner
          self.cnpj = cnpj
          self.email = email
          self.address = address
          self.city = city
          self.state = state
          self.cep = cep
          self.password = password

