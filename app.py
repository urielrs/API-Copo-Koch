# app.py
from flask import Flask, render_template, jsonify
import matplotlib.pyplot as plt
import io
import base64
import math

app = Flask(__name__)

# Esta es la función de la curva de Koch que ya conoces
def koch_curve(order, length=1.0, start=(0, 0), angle=0):
    if order == 0:
        rad = math.radians(angle)
        x_end = start[0] + length * math.cos(rad)
        y_end = start[1] + length * math.sin(rad)
        return [start, (x_end, y_end)]
    
    length /= 3.0
    
    points = []
    points += koch_curve(order - 1, length, start, angle)[:-1]
    
    p2 = (start[0] + length * math.cos(math.radians(angle)),
          start[1] + length * math.sin(math.radians(angle)))
    points += koch_curve(order - 1, length, p2, angle + 60)[:-1]
    
    p3 = (p2[0] + length * math.cos(math.radians(angle + 60)),
          p2[1] + length * math.sin(math.radians(angle + 60)))
    points += koch_curve(order - 1, length, p3, angle - 60)[:-1]
    
    p4 = (p3[0] + length * math.cos(math.radians(angle - 60)),
          p3[1] + length * math.sin(math.radians(angle - 60)))
    points += koch_curve(order - 1, length, p4, angle)
    
    return points

# Ruta para mostrar la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de la API que genera la imagen
@app.route('/generate_koch')
def generate_koch():
    order = 5 # Nivel de detalle de la curva
    
    # Genera la curva de Koch
    points = koch_curve(order, length=1.0)
    x, y = zip(*points)
    
    # Crea el gráfico en memoria
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, color="blue")
    ax.set_title(f"Copo de Koch ")
    ax.axis("equal")
    ax.axis("off")
    
    # Guarda el gráfico en un buffer en memoria en formato PNG
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)  # Cierra la figura para liberar memoria
    
    # Codifica la imagen a base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Devuelve la imagen como una respuesta JSON
    return jsonify({'image': image_base64})

if __name__ == '__main__':
    app.run(debug=True)



