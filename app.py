from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

# Material prices
CEMENT_BAG_PRICE = 9500
SAND_TRIP_PRICE = 70000  # 10 tons
GRANITE_TON_PRICE = 20000
WATER_10000L_PRICE = 50000

# Cement usage rates (bags per m³)
CEMENT_RATES = {
    'slab': 7,
    'column': 9,
    'beam': 8,
    'footing': 6.5
}

@app.route('/', methods=['GET', 'POST'])
def calculate_volume():
    if request.method == 'POST':
        length = float(request.form['length'])
        width = float(request.form['width'])
        depth = float(request.form['depth'])
        work_type = request.form['work_type']

        volume = round(length * width * depth, 2)
        cement_bags = round(volume * CEMENT_RATES[work_type])
        sand_price = "{:,.0f}".format(SAND_TRIP_PRICE)
        granite_price = "{:,.0f}".format(volume * 1.5 * GRANITE_TON_PRICE)
        water_price = "{:,.0f}".format(WATER_10000L_PRICE)

        result = {
            'volume': volume,
            'cement': cement_bags,
            'sand_price': sand_price,
            'granite_price': granite_price,
            'water_price': water_price,
            'work_type': work_type
        }

        return render_template('index.html', result=result)

    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_pdf():
    work_type = request.form['work_type']
    volume = request.form['volume']
    cement = request.form['cement']
    sand_price = request.form['sand_price']
    granite_price = request.form['granite_price']
    water_price = request.form['water_price']

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Concrete Estimate Summary", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Civil Work Type: {work_type.title()}", ln=True)
    pdf.cell(200, 10, txt=f"Volume: {volume} m³", ln=True)
    pdf.cell(200, 10, txt=f"Cement Bags: {cement} bags", ln=True)
    pdf.cell(200, 10, txt=f"Sand Cost: ₦{sand_price}", ln=True)
    pdf.cell(200, 10, txt=f"Granite Cost: ₦{granite_price}", ln=True)
    pdf.cell(200, 10, txt=f"Water Cost: ₦{water_price}", ln=True)

    filepath = "estimate.pdf"
    pdf.output(filepath)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
