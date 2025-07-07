from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_volume():
    result = None
    materials = {}
    costs = {}
    total_cost = 0

    if request.method == 'POST':
        try:
            length = float(request.form['length'])
            width = float(request.form['width'])
            depth = float(request.form['depth'])

            volume = round(length * width * depth, 2)

            # Material estimates per cubic meter
            materials = {
                'cement': round(volume * 7, 1),      # 7 bags of cement per m³
                'sand': round(volume * 0.5, 1),      # 0.5 tons per m³
                'granite': round(volume * 0.6, 1),   # 0.6 tons per m³
                'water': round(volume * 150, 1)      # 150 liters per m³
            }

            # Cost calculations
            costs = {
                'cement': materials['cement'] * 9500,     # ₦9,500 per bag
                'sand': materials['sand'] * 7000,         # ₦7,000 per ton
                'granite': materials['granite'] * 20000,  # ₦20,000 per ton
                'water': materials['water'] * 5           # ₦50,000 per 10,000L = ₦5/L
            }

            total_cost = sum(costs.values())

            result = {
                'volume': volume,
                'materials': materials,
                'costs': costs,
                'total_cost': total_cost
            }

        except ValueError:
            result = {'error': 'Please enter valid numbers for all fields.'}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


