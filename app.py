from flask import Flask, render_template, request, send_file
import math
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("CALCULATION TRIGGERED")
        try:
            length = float(request.form['length'])
            width = float(request.form['width'])
            depth = float(request.form['depth'])

            volume = round(length * width * depth, 2)

            # Material estimates
            cement_bags = math.ceil(volume * 7)
            sand = round(volume * 0.5, 2)
            granite = round(volume * 1.0, 2)
            water = round(volume * 150, 2)

            # Prices (as provided)
            prices = {
                'cement': 9500,
                'sand': 7000,
                'granite': 20000,
                'water': 5  # per litre
            }

            total = (
                cement_bags * prices['cement'] +
                sand * prices['sand'] +
                granite * prices['granite'] +
                water * prices['water']
            )

            materials = {
                'cement': cement_bags,
                'sand': sand,
                'granite': granite,
                'water': water,
                'total': total
            }

            return render_template(
                'index.html',
                result=volume,
                materials=materials,
                prices=prices,
                length=length,
                width=width,
                depth=depth
            )
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    length = float(request.form['length'])
    width = float(request.form['width'])
    depth = float(request.form['depth'])

    volume = round(length * width * depth, 2)
    cement_bags = math.ceil(volume * 7)
    sand = round(volume * 0.5, 2)
    granite = round(volume * 1.0, 2)
    water = round(volume * 150, 2)

    prices = {
        'cement': 9500,
        'sand': 7000,
        'granite': 20000,
        'water': 5
    }

    total = (
        cement_bags * prices['cement'] +
        sand * prices['sand'] +
        granite * prices['granite'] +
        water * prices['water']
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Concrete Volume & Estimate Report")
    pdf.drawString(100, 730, f"Volume: {volume} m³")
    pdf.drawString(100, 710, f"Cement: {cement_bags} bags (₦{cement_bags * prices['cement']})")
    pdf.drawString(100, 690, f"Sand: {sand} tons (₦{int(sand * prices['sand'])})")
    pdf.drawString(100, 670, f"Granite: {granite} tons (₦{int(granite * prices['granite'])})")
    pdf.drawString(100, 650, f"Water: {water} litres (₦{int(water * prices['water'])})")
    pdf.drawString(100, 620, f"Total Estimate: ₦{int(total)}")
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='estimate.pdf', mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)

