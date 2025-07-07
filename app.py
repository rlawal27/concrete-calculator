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
            height = float(request.form['height'])

            # Calculate concrete volume
            volume = round(length * width * height, 2)
            result = volume

            # Estimate material quantities
            materials = {
                'cement': round(volume * 7, 2),     # bags
                'sand': round(volume * 0.5, 2),     # tons
                'granite': round(volume * 0.9, 2),  # tons
                'water': round(volume * 180, 2)     # liters
            }

            # Prices based on your inputs
            unit_prices = {
                'cement': 9500,     # per bag
                'sand': 700,        # per ton
                'granite': 20000,   # per ton
                'water': 5          # per liter
            }

            # Calculate individual and total cost
            costs = {
                'cement': round(materials['cement'] * unit_prices['cement'], 2),
                'sand': round(materials['sand'] * unit_prices['sand'], 2),
                'granite': round(materials['granite'] * unit_prices['granite'], 2),
                'water': round(materials['water'] * unit_prices['water'], 2)
            }

            total_cost = sum(costs.values())

        except ValueError:
            result = "Invalid input. Please enter numbers only."

    return render_template(
        'index.html',
        result=result,
        materials=materials,
        costs=costs,
        total_cost=total_cost
    )

if __name__ == '__main__':
    app.run(debug=True)


