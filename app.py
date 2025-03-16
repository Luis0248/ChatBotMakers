from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import openai  # Importar la biblioteca de OpenAI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurar la API Key de OpenAI
openai.api_key = "tu_nueva_api_key"  # Reemplaza con tu nueva API Key

# Modelo de la base de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    caracteristicas = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "marca": self.marca,
            "modelo": self.modelo,
            "precio": self.precio,
            "caracteristicas": self.caracteristicas
        }

# Crear la base de datos y insertar datos de ejemplo (solo la primera vez)
with app.app_context():
    db.create_all()

    # Verificar si la tabla ya tiene datos
    if Producto.query.count() == 0:
        productos_ejemplo = productos_ejemplo = [
    Producto(categoria="Celular", marca="Samsung", modelo="Galaxy S23", precio=799.99, caracteristicas="128GB, buena cámara, 5G"),
    Producto(categoria="Celular", marca="Apple", modelo="iPhone 15", precio=999.99, caracteristicas="256GB, excelente cámara, 5G"),
    Producto(categoria="Celular", marca="Xiaomi", modelo="Redmi Note 12", precio=299.99, caracteristicas="128GB, buena cámara, 4G"),
    Producto(categoria="Celular", marca="Google", modelo="Pixel 7", precio=599.99, caracteristicas="128GB, excelente cámara, 5G"),
    Producto(categoria="Celular", marca="OnePlus", modelo="OnePlus 11", precio=699.99, caracteristicas="256GB, buena cámara, 5G"),
]
        db.session.bulk_save_objects(productos_ejemplo)
        db.session.commit()
        print("Datos de ejemplo insertados con éxito.")

# Función para buscar productos en la base de datos
def buscar_productos(categoria=None, marca=None):
    query = Producto.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    if marca:
        query = query.filter_by(marca=marca)
    productos = [producto.to_dict() for producto in query.all()]
    print("Productos encontrados:", productos)  # Depuración
    return productos

# Función para generar una respuesta usando OpenAI
def generar_respuesta_openai(mensaje):
    try:
        print("Enviando solicitud a OpenAI...")  # Depuración
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usar GPT-3.5-turbo
            messages=[
                {"role": "system", "content": "Eres un asistente virtual útil."},
                {"role": "user", "content": mensaje}
            ]
        )
        print("Respuesta de OpenAI recibida:", respuesta)  # Depuración
        return respuesta['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error al generar respuesta con OpenAI: {e}")  # Depuración
        return "Lo siento, hubo un error al procesar tu solicitud."

# Función de respuesta del ChatBot
def responder_usuario(mensaje):
    mensaje = mensaje.lower()
    print(f"Mensaje recibido: {mensaje}")  # Depuración

    # Saludo inicial
    if any(palabra in mensaje for palabra in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
        return "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

    # Consultar celulares disponibles
    if any(palabra in mensaje for palabra in ["celulares", "celular", "teléfonos", "móviles"]):
        productos = buscar_productos(categoria="Celular")
        if productos:
            detalles = "\n".join([f"{p['marca']} {p['modelo']} (${p['precio']})" for p in productos])
            return f"Tenemos estos celulares disponibles:\n{detalles}"
        else:
            return "No tenemos celulares disponibles en este momento."

    # Consultar computadoras disponibles
    if any(palabra in mensaje for palabra in ["computadoras", "computador", "pc", "ordenadores"]):
        productos = buscar_productos(categoria="Computadora")
        if productos:
            detalles = "\n".join([f"{p['marca']} {p['modelo']} (${p['precio']})" for p in productos])
            return f"Tenemos estas computadoras disponibles:\n{detalles}"
        else:
            return "No tenemos computadoras disponibles en este momento."

    # Consultar el precio de un producto específico
    if "precio" in mensaje:
        for producto in buscar_productos():
            if producto["marca"].lower() in mensaje or producto["modelo"].lower() in mensaje:
                return f"El {producto['marca']} {producto['modelo']} cuesta ${producto['precio']}. Características: {producto['caracteristicas']}."
        return "No encontré ese producto. ¿Puedes proporcionar más detalles?"

    # Consultar características específicas de un celular
    if any(palabra in mensaje for palabra in ["características", "especificaciones", "detalles"]):
        for producto in buscar_productos(categoria="Celular"):
            if producto["marca"].lower() in mensaje or producto["modelo"].lower() in mensaje:
                return f"Las características del {producto['marca']} {producto['modelo']} son: {producto['caracteristicas']}."
        return "No encontré ese celular. ¿Puedes proporcionar más detalles?"

    # Recomendar celulares según necesidades
    if any(palabra in mensaje for palabra in ["recomendar", "recomiéndame", "sugerir"]):
        if "almacenamiento" in mensaje or "espacio" in mensaje:
            productos = buscar_productos(categoria="Celular")
            recomendados = [p for p in productos if "256gb" in p["caracteristicas"].lower()]
            if recomendados:
                detalles = "\n".join([f"{p['marca']} {p['modelo']} (${p['precio']})" for p in recomendados])
                return f"Te recomiendo estos celulares con buen almacenamiento:\n{detalles}"
            else:
                return "No encontré celulares con buen almacenamiento."
        elif "cámara" in mensaje or "fotos" in mensaje:
            productos = buscar_productos(categoria="Celular")
            recomendados = [p for p in productos if "buena cámara" in p["caracteristicas"].lower()]
            if recomendados:
                detalles = "\n".join([f"{p['marca']} {p['modelo']} (${p['precio']})" for p in recomendados])
                return f"Te recomiendo estos celulares con buena cámara:\n{detalles}"
            else:
                return "No encontré celulares con buena cámara."
        else:
            return "¿Qué tipo de celular estás buscando? Por ejemplo, ¿uno con buen almacenamiento o buena cámara?"

    # Despedida
    if any(palabra in mensaje for palabra in ["adiós", "chao", "hasta luego", "salir"]):
        return "¡Gracias por usar nuestro servicio! Hasta luego."

    # Respuesta por defecto: Usar OpenAI para generar una respuesta
    return generar_respuesta_openai(mensaje)

# Rutas de la API
@app.route("/")
def home():
    return "¡Bienvenido al ChatBot! Usa la ruta /chat para enviar mensajes."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensaje_usuario = data.get("mensaje", "")
    respuesta = responder_usuario(mensaje_usuario)
    return jsonify({"respuesta": respuesta})

@socketio.on("mensaje")
def handle_message(data):
    mensaje_usuario = data.get("mensaje", "")
    respuesta = responder_usuario(mensaje_usuario)
    socketio.emit("respuesta", {"respuesta": respuesta})

if __name__ == "__main__":
    socketio.run(app, debug=True)