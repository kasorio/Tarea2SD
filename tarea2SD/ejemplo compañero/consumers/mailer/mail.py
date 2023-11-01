import smtplib
import psycopg2
from email.mime.text import MIMEText

# Configuraci贸n de base de datos
DATABASE_CONFIG = {
    'dbname': 'proyecto', 
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

# Configuraci贸n de SMTP
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "MAMOCHI"
SMTP_PASSWORD = "password"

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

def send_verdict_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, tipo FROM usuario WHERE email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre = result
                subject = "Notificaci贸n de Veredicto"
                body = f"Hola {nombre},\n\nSe ha aprobado tu solicitud.\n\nSaludos,\nEquipo de MAMOCHI"
                send_email(subject, body, user_email)

def send_ingredient_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, ingrediente FROM usuario JOIN ingredientes ON usuario.email = ingredientes.id WHERE usuario_email.email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre, ingrediente = result
                subject = "Reposici贸n de Ingrediente"
                body = f"Hola {nombre},\n\nEl ingrediente: {ingrediente} ha sido reponido.\n\nSaludos,\nTu Equipo"
                send_email(subject, body, user_email)

def send_sales_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, cantidad, valor FROM usuario JOIN ventas ON usuario.email = ventas.id WHERE usuario_email.email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre, cantidad_vendida, ganancias = result
                subject = "Resumen de Ventas"
                body = f"Hola {nombre},\n\nCantidad Vendida: {cantidad_vendida}\nGanancias: ${ganancias}\n\nSaludos,\nTu Equipo"
                send_email(subject, body, user_email)