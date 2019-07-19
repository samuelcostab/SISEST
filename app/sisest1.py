from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db3.sqlite'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

db.metadata.clear()
#models
class Company(db.Model):    
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60))
    owner = db.Column(db.String(60))
    cnpj = db.Column(db.String(22))
    email = db.Column(db.String(60))
    address = db.Column(db.String(60))
    city = db.Column(db.String(60))
    state = db.Column(db.String(60))
    cep = db.Column(db.String(60))
    password = db.Column(db.String(128))

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

class ticketEstacionamento(db.Model):
    __tablename__ = 'ticketEstacionamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vaga = db.Column(db.Integer)
    vehicle_plate = db.Column(db.String(10))
    arrival_time = db.Column(db.DateTime)
    cust = db.Column(db.Float)

    def __init__(self, local_estacionado):
        self.id_vaga = local_estacionado.id
        self.arrival_time = local_estacionado.arrival_time
        self.cust = 1.0
        self.vehicle_plate = local_estacionado.vehicle.vehicle_plate
        self.vehicle = local_estacionado.vehicle

    def is_empty(self):
        return self.vehicle == None

    def duration_time_parked(self):
        if(self.is_empty()):
            raise ValueError()
        return (datetime.now() - self.arrival_time).total_seconds()

    def get_cost(self):
        hours = self.duration_time_parked() / 3600
        return self.vehicle.get_cost_hour() * hours

class Vehicle:
    '''__tablename__ = 'vehicle'
    placaVehicle = db.Column(db.String(9), primary_key=True)
    typeVehicle = db.Column(db.String(20))
    client = Column(Integer, ForeignKey('client.id'))'''

    def __init__(self, placaVehicle, typeVehicle, client):
        self.vehicle_plate = placaVehicle
        self.type_vehicle = typeVehicle
        self.client = client

    def get_cost_hour(self):
        if self.type_vehicle == "Motocicleta":
            return 5
        if self.type_vehicle == "Automóvel":
            return 10

class Client:
    '''__tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60))
    phone = db.Column(db.String(60))
    email = db.Column(db.String(60))'''

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

class Local:

    def __init__(self, id, vehicle, arrival_time):
        self.id = id
        self.vehicle = vehicle
        self.arrival_time = arrival_time

    def is_empty(self):
        return self.vehicle == None

class LocalManager:
    def __init__(self, size):
        self.locals = []
        for i in range(size):
            self.locals.append(Local(i, None, None))
        
    def insert_vehicles(self, vehicle):
        for local in self.locals:
            if not local.is_empty:
                continue
            local.vehicle = vehicle
            local.arrival_time = datetime.now()
            return local

    def remove_vehicle(self, vehicle_id):
        for local in self.locals:
            if not local.is_empty() and local.vehicle.vehicle_plate == vehicle_id:
                value = local.get_cost()
                local.arrival_time = None
                local.vehicle = None
                return value
    def free_locals(self):
        count = 0
        for local in self.locals:
            if local.is_empty():
                count += 1
        return count

db.create_all()

#Rotas

userOn = False ##Identificar usuário logado
companySelect = None ##Empresa logada atualmente
gerenciador_de_local = None
@app.route('/')
def index():
	return render_template('index.html', user=userOn)

@app.route('/cadastrar')
def cadastrar():
	return render_template('main/pag-cadastro.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == 'POST':
        default_name = '0'
        ncompany = request.form.get('inputNomeEmpresa',default_name)
        owner = request.form.get('inputProprietario',default_name)
        cnpj = request.form.get('inputCNPJ',default_name)
        email = request.form.get('inputEmail',default_name)
        address = request.form.get('inputEndereco',default_name)
        city = request.form.get('inputCidade',default_name)
        state = request.form.get('inputEstado',default_name)
        cep = request.form.get('inputCEP',default_name)
        password = request.form.get('inputSenha',default_name)
        confirmPassword = request.form.get('inputConfirmSenha',default_name)

        gerenciador_de_local = LocalManager(20) ##Cria um gerenciador que organiza um espaço com 20 locais para estacionar
        
        if ncompany and owner and cnpj  and email and email and address and city and state and cep and password:
            comp = Company(ncompany,owner,cnpj,email,address,city,state,cep,password)
            db.session.add(comp)
            db.session.commit()
    return redirect(url_for('index'))

@app.route('/userLogado', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        default_name = '0'
        emailCompany = request.form.get('inputEmail',default_name)
        senhaCompany = request.form.get('inputSenha',default_name)

        empresas = Company.query.all()
        for empresa in empresas:
            if empresa.email == emailCompany:
                if empresa.password == senhaCompany:
                    userOn = True
                    companySelect = empresa
                    return render_template('index.html', user=userOn, company=companySelect)
        
        return redirect(url_for('index'))


@app.route('/controleEstacionamento')
def controleEstacionamento():
    ticketsBD = ticketEstacionamento.query.all()
    return render_template('main/pag-gerencEstacionamento.html', user=userOn, company=companySelect, tickets= ticketsBD)

@app.route('/controleEstacionamento', methods=["GET", "POST"])
def adicionaTicket():
    if request.method == 'POST':
        default_name = '0'
        nameClient = request.form.get('inputNomeCliente',default_name)
        phoneClient = request.form.get('inputNumeroContato',default_name)
        emailClient = request.form.get('inputEmail',default_name)
        tipoVeiculo = request.form.get('inputTipoVeiculo',default_name)
        placaVehicle = request.form.get('inputPlacaVeiculo',default_name)
        client = Client(nameClient,emailClient,phoneClient)
        vehicles = Vehicle(placaVehicle, tipoVeiculo, client)
        local_estacionado = gerenciador_de_local.insert_vehicles(vehicles)

        if local_estacionado != None:
           itemTicket = ticketEstacionamento(local_estacionado)
           db.session.add(itemTicket)
           db.session.commit()

        return redirect(url_for('controleEstacionamento'))

@app.route('/excluir/<int:idTicket>')
def excluiTicket(idTicket, gerenciador_de_local):
    ticket = ticketEstacionamento.query.filter_by(id=idTicket).first()

    ticketDeleted = ticketEstacionamento(Local(None,None,None))
    ticketDeleted.arrival_time = ticket.arrival_time

    ##gerenciador_de_local.remove_vehicle(self, vehicle_id)

    db.session.delete(ticket)
    db.session.commit()

    return redirect(url_for('controleEstacionamento'))


if __name__ == '__main__':
    app.run(debug=True)

