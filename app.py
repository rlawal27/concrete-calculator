from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_volume():
    result = None
    materials = []
    length = width = depth = 0

    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        depth = float(request.form['depth'])

        volume = length * width * depth
        result = round(volume, 2)

        # Material estimations
        cement_bags = int(volume * 7)
        sand_trips = round(volume / 5, 2)
        granite_tons = round(volume * 1.5, 2)
        water_trips = round(volume / 10, 2)

        # Prices
        cement_price = 9500
        sand_price = 70000
        granite_price = 20000
        water_price = 50000

        materials = [
            f"Cement: {cement_bags} bags (₦{cement_bags * cement_price:,.0f})",
            f"Sand: {sand_trips} trips (₦{sand_trips * sand_price:,.0f})",
            f"Granite: {granite_tons} tons (₦{granite_tons * granite_price:,.0f})",
            f"Water: {water_trips} trips (₦{water_trips * water_price:,.0f})"
        ]

    return render_template('index.html', result=result, materials=materials,
                           length=length, width=width, depth=depth)

@app.route('/download', methods=['POST'])
def download_pdf():
    length = float(request.form['length'])
    width = float(request.form['width'])
    depth = float(request.form['depth'])

    volume = length * width * depth
    volume = round(volume, 2)

    cement_bags = int(volume * 7)
    sand_trips = round(volume / 5, 2)
    granite_tons = round(volume * 1.5, 2)
    water_trips = round(volume / 10, 2)

    cement_price = 9500
    sand_price = 70000
    granite_price = 20000
    water_price = 50000

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "Concrete Volume and Material Estimate - Adillux Technologies")
    p.drawString(100, 780, f"Volume: {volume} m³")
    p.drawString(100, 760, f"Cement: {cement_bags} bags (₦{cement_bags * cement_price:,.0f})")
    p.drawString(100, 740, f"Sand: {sand_trips} trips (₦{sand_trips * sand_price:,.0f})")
    p.drawString(100, 720, f"Granite: {granite_tons} tons (₦{granite_tons * granite_price:,.0f})")
    p.drawString(100, 700, f"Water: {water_trips} trips (₦{water_trips * water_price:,.0f})")

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="estimate.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
