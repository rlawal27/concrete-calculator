from flask import Flask, render_template, request, send_file
import math
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_volume():
    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        depth = float(request.form['depth'])

        volume = round(length * width * depth, 2)

        # Estimations
        cement_bags = math.ceil(volume * 7)
        sand = round(volume * 0.5, 2)
        granite = round(volume * 1.0, 2)
        water = round(volume * 150, 2)

        materials = {
            'cement': cement_bags,
            'sand': sand,
            'granite': granite,
            'water': water
        }

        return render_template('index.html', result=volume, materials=materials)

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

    total = (
        cement_bags * 9500 +
        sand * 7000 +
        granite * 20000 +
        water * 5
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Concrete Volume Estimate")
    pdf.drawString(100, 730, f"Volume: {volume} m³")
    pdf.drawString(100, 710, f"Cement: {cement_bags} bags (₦{cement_bags * 9500})")
    pdf.drawString(100, 690, f"Sand: {sand} tons (₦{int(sand * 7000)})")
    pdf.drawString(100, 670, f"Granite: {granite} tons (₦{int(granite * 20000)})")
    pdf.drawString(100, 650, f"Water: {water} litres (₦{int(water * 5)})")
    pdf.drawString(100, 630, f"Total Estimated Cost: ₦{int(total)}")
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='estimate.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

