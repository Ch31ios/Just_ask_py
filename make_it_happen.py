
import pymysql # pip install PyMySQL
import os

# Función para limpiar consola

def limpiar_consola():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
# Clase para crear la conexión de la base de datos ('wishes')
    
class DataBase:
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        
        self.connection = pymysql.connect(
            
            host='localhost',
            user='root',
            password='2004',
            db='wishes'
        )
        
        self.cursor = self.connection.cursor()
    
    def close(self):
    
        if self.connection:
            self.connection.close()
            
            
            
    # Método para insertar un usuario en la tabla (register_a_wisher)
    
    def register_a_wisher(self, user_id, first_name, last_name, email, phone_number):
        
        try:

            self.cursor.execute("SELECT user_id FROM register_a_wisher WHERE user_id = %s", (user_id,))
            
            existing_user = self.cursor.fetchone()

            if existing_user:
                
                print("\n" + f"El usuario con identifiación: {user_id}, ya esta en uso. Por favor, crea otra identifiación.")
            else:
                
                self.cursor.execute(
                    
                    "INSERT INTO register_a_wisher (user_id, first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s, %s)", 
                    (user_id, first_name, last_name, email, phone_number)
                )
                
                self.connection.commit()
                
                print("\n" + "Has registrado un usuario con exito.")
                
        except pymysql.Error as e:
            
            print("\n" + f"Error al registrar al usuario. {e}")
            
            
    # Método para registrar un deseo en la tabla (make_a_wish)
                
    def make_a_wish(self, full_name, describe_your_wish, when_you_want_it_to_happen):
        
        try:

            self.cursor.execute(
                
                "INSERT INTO make_a_wish (full_name, describe_your_wish, when_you_want_it_to_happen) VALUES (%s, %s, %s)", 
                (full_name, describe_your_wish, when_you_want_it_to_happen)
            )            
        
            self.connection.commit()
                
        except pymysql.Error as e:
            
            print(f"Error al pedir un deseo. {e}")
            
    # Método para verificar si un usuario existe en la base de datos
    
    def check_user_existence(self, first_name, last_name):
        
        try:
            
            self.cursor.execute(
                
                "SELECT user_id FROM register_a_wisher WHERE first_name = %s AND last_name = %s",
                (first_name, last_name)
            )
            
            existing_user = self.cursor.fetchone()
            
            if existing_user:
                return True
            else:
                return False
            
        except pymysql.Error as e:
            
            print("\n" + f"Error al verificar la existencia del usuario. {e}")

dataBase = DataBase()


# Clase para el usuario

class User:
    
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def set_password(self, password):
        self.__password = password

    def login(self, entered_password):
        return self.__password == entered_password

    def __str__(self):
        return f'User: {self.__username}'
    
    
# Clase para el administrador, hereda del 'usuario'

class Administrador(User):
    
    def __init__(self, username, password):
        super().__init__(username, password)

    def __str__(self):
        return f'Administrador: {self.get_username()}'

class Usuario(User):
    
    def __init__(self, username, password):
        super().__init__(username, password)

    def __str__(self):
        return f'Usuario: {self.get_username()}'


# Callback para imprimir la información del usuario

def imprimir_informacion_usuario(Usuario):
    
    print(Usuario)
    
    
# Lambda para verificar si el usuario es administrador

es_admin = lambda Usuario: isinstance(Usuario, Administrador)


# Definímos los diferentes usuarios

admin = Administrador("admin", "111")
user = Usuario("usuario", "111")

def menu():

    print("\n" + " ------------- LOGIN -------------- ")
    print("|                                  |")
    print("|  1. Iniciar (admin o usuario)    |")
    print("|  2. Salir                        |")
    print("|                                  |")
    print(" -------------- ---- -------------- \n")


def menu_login():
    
    limpiar_consola()
    
    while True:
        
        menu()
        
        opcion = input("Elije una opción: ")
        
        if opcion == "1":
            
            limpiar_consola()
            
            print("Ingresa como admin o usuario")
            
            username = input("\n" + "Nombre: ")
            password = input("Contraseña: ")
            
            limpiar_consola()
            
            # Datos del administrador
            
            if admin.get_username() == username and admin.login(password):
                
                dataBase.connect() # Activa la conexión a la base de datos
                
                limpiar_consola()
                
                print("\n" + f"Bienvenido {username}!")
                
                while True:
                    
                    opcion_admin = input("\n" + "¿Desea agregar un usuario? (s/n): ").lower()
                    
                    if opcion_admin == "s":
                        
                        limpiar_consola()
                        
                        user_id = input("\n" + "Identificación del usuario: ")
                        first_name = input("Primer nombre del usuario: ")
                                                   
                        # Validación del primer nombre (no debe estar vacío)
                        
                        while not first_name:
                            
                            print("\n" + "El primer nombre no puede estar vacío. \n")
                            first_name = input("Primer nombre del usuario: ")
                            
                        last_name = input("Apellidos del usuario: ")
                        
                        # Validación del primer apellido (no debe estar vacío)
                        
                        while not last_name:
                            
                            print("\n" + "El apellido no puede estar vacío. \n")
                            last_name = input("Apellidos del usuario: ")
                        
                        email = input("Correo electronico del usuario: ")
                        phone_number = input("Numero de telefono del usuario: ")
                        
                        dataBase.register_a_wisher(user_id, first_name, last_name, email, phone_number)
                        
                    elif opcion_admin == "n":
                        
                        limpiar_consola()
                        print("Nos vemos pronto...\n")
                        break
                    
                    else: 
                        
                        limpiar_consola()
                        print("Ingrese una opción valida. \n")
                        
            # Datos del usuario
                        
            elif user.get_username() == username and user.login(password):
                
                dataBase.connect() # Activa la conexión a la base de datos
                
                print("\n" + f"Bienvenido {username}!")
                
                while True:
                    
                    opcion_user = input("\n" + "¿Deseas pedir un deseo? (s/n): ").lower()
                    
                    if opcion_user == "s":
                        
                        limpiar_consola()
                        full_name = input("\n" + "Ingresa tu nombre completo: ")
                        
                        # Validación del nombre completo (debe contener al menos un espacio)
                        
                        if " " in full_name:
                            
                            first_name, last_name = full_name.split(" ", 1)
                            
                            if dataBase.check_user_existence(first_name, last_name):
                                
                                describe_your_wish = input("Describe tu deseo: ")
                                when_you_want_it_to_happen = input("¿Cuándo quieres que pase?: ")
                                dataBase.make_a_wish(full_name, describe_your_wish, when_you_want_it_to_happen)
                                
                                limpiar_consola()
                                print("\n" + f"Querid@ {full_name}, próximamente se cumplirá tu deseo...")
                                break
                            
                            else:
                                
                                limpiar_consola()
                                print("\n" + "El usuario no está registrado, pídele al administrador que te registre...")
                        else:
                            
                            limpiar_consola()
                            print("\n" + "Ingresa tu nombre y apellidos.")
                            continue
                        
                    elif opcion_user == "n":
                        
                        limpiar_consola()
                        print("Nos vemos pronto...\n")
                        break
                    
                    else:
                        limpiar_consola()
                        print("\n" + "Por favor, ingresa una opción válida (s/n). \n")
                    
                dataBase.close()
            
            else:
                
                print("\n" + "Nombre de usuario o contraseña incorrectos. \n")
                
        elif opcion == "2":
            
            limpiar_consola()
            
            print("Nos veremos en otra ocasión... \n")
            break
        
        else:
            
            limpiar_consola()
            print("Ingrese una opción valida. \n")
            
menu_login()
