from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

# Prices
CEMENT_BAG_PRICE = 9500
SAND_TRIP_PRICE = 70000  # per 10-ton trip
GRANITE_TON_PRICE = 20000
WATER_TRIP_PRICE = 50000  # per 10,000 litres

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        length = float(request.form.get('length') or 0)
        width = float(request.form.get('width') or 0)
        thickness = float(request.form.get('thickness') or 0)

        volume = (length * width * thickness) / 1000000  # m³

        # Material estimates
        cement_bags = volume * 6.5
        sand_trips = volume * 0.5
        granite_tons = volume * 1.2
        water_trips = volume * 0.05

        # Cost estimates
        cement_cost = cement_bags * CEMENT_BAG_PRICE
        sand_cost = sand_trips * SAND_TRIP_PRICE
        granite_cost = granite_tons * GRANITE_TON_PRICE
        water_cost = water_trips * WATER_TRIP_PRICE
        total_cost = cement_cost + sand_cost + granite_cost + water_cost

        result = round(volume, 2)
        materials = {
            "Cement (bags)": (round(cement_bags, 1), round(cement_cost, 2)),
            "Sand (10-ton trips)": (round(sand_trips, 2), round(sand_cost, 2)),
            "Granite (tons)": (round(granite_tons, 2), round(granite_cost, 2)),
            "Water (10,000L trips)": (round(water_trips, 2), round(water_cost, 2)),
            "Total Estimate": ("", round(total_cost, 2))
        }

        if request.form.get('generate_pdf') == 'yes':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Concrete Estimate", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(200, 10, f"Volume: {result} m³", ln=True)
            for material, (qty, cost) in materials.items():
                if material != "Total Estimate":
                    pdf.cell(200, 10, f"{material}: {qty} units - ₦{cost:,.2f}", ln=True)
            pdf.cell(200, 10, f"Total Cost: ₦{materials['Total Estimate'][1]:,.2f}", ln=True)
            filename = "concrete_estimate.pdf"
            pdf.output(filename)
            return send_file(filename, as_attachment=True)

        return render_template("index.html", result=result, materials=materials)

    return render_template("index.html")

@app.route('/civil-quotation', methods=['GET', 'POST'])
def civil_quotation():
    if request.method == 'POST':
        excavation = float(request.form.get('excavation') or 0)
        blockwork = float(request.form.get('blockwork') or 0)
        plastering = float(request.form.get('plastering') or 0)
        concrete = float(request.form.get('concrete') or 0)
        formwork = float(request.form.get('formwork') or 0)
        labour = float(request.form.get('labour') or 0)

        rates = {
            'Excavation': 3000,
            'Blockwork': 2500,
            'Plastering': 1800,
            'Concrete': 40000,
            'Formwork': 1500,
            'Labour': 1
        }

        result = [
            {'name': 'Excavation', 'qty': excavation, 'rate': rates['Excavation'], 'total': excavation * rates['Excavation']},
            {'name': 'Blockwork', 'qty': blockwork, 'rate': rates['Blockwork'], 'total': blockwork * rates['Blockwork']},
            {'name': 'Plastering', 'qty': plastering, 'rate': rates['Plastering'], 'total': plastering * rates['Plastering']},
            {'name': 'Concrete', 'qty': concrete, 'rate': rates['Concrete'], 'total': concrete * rates['Concrete']},
            {'name': 'Formwork', 'qty': formwork, 'rate': rates['Formwork'], 'total': formwork * rates['Formwork']},
            {'name': 'Labour', 'qty': labour, 'rate': 1, 'total': labour},
        ]

        total = sum(item['total'] for item in result)

        return render_template('civil_works.html', result=result, total=round(total, 2))

    return render_template('civil_works.html')

if __name__ == '__main__':
    app.run(debug=True)
