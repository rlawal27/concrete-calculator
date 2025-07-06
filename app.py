from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_volume():
    result = None
    materials = {}
    
    if request.method == 'POST':
        try:
            length = float(request.form['length'])
            width = float(request.form['width'])
            height = float(request.form['height'])
            volume = length * width * height
            result = f"{volume:.2f} cubic meters (m³)"

            # Material estimate calculations (for 1:2:4 mix)
            dry_volume = volume * 1.54
            cement_bags = round(dry_volume * 7)
            sand_m3 = round(dry_volume * 0.44, 2)
            granite_m3 = round(dry_volume * 0.88, 2)
            water_litres = round(volume * 180)

            materials = {
                "Cement (bags)": cement_bags,
                "Sand (m³)": sand_m3,
                "Granite (m³)": granite_m3,
                "Water (litres)": water_litres
            }

        except:
            result = "Invalid input. Please enter numbers only."

    return render_template('index.html', result=result, materials=materials)

if __name__ == '__main__':
    app.run(debug=True)
