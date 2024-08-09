from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Werkelijke afstanden van de planeten tot de zon in miljoenen kilometers
actual_distances = {
    'Mercury': 57.9,
    'Venus': 108.2,
    'Earth': 149.6,
    'Mars': 227.9,
    'Jupiter': 778.5,
    'Saturn': 1434,
    'Uranus': 2871,
    'Neptune': 4497.1
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sun_to_earth_distance = float(request.form['sun_to_earth'])
        scale_factor = sun_to_earth_distance / actual_distances['Earth']
        user_distances = {}
        errors = []
        
        for planet in actual_distances:
            if planet != 'Earth':
                try:
                    user_input = float(request.form[planet])
                    user_distances[planet] = user_input
                except ValueError:
                    errors.append(f"Invalid input for {planet}")
        
        accuracy = {}
        total_accuracy = 0
        count = 0
        
        for planet, actual_distance in actual_distances.items():
            if planet in user_distances:
                expected_distance = actual_distance * scale_factor
                accuracy[planet] = abs(expected_distance - user_distances[planet]) / expected_distance * 100
                total_accuracy += accuracy[planet]
                count += 1
        
        average_accuracy = total_accuracy / count if count > 0 else 0
        
        # Maak een grafiek
        planets = list(user_distances.keys())
        measured_distances = list(user_distances.values())
        expected_distances = [actual_distances[planet] * scale_factor for planet in planets]
        
        fig, ax = plt.subplots()
        ax.plot(planets, measured_distances, label="Measured Distances", marker='o')
        ax.plot(planets, expected_distances, label="Expected Distances", marker='x')
        ax.set_xlabel('Planets')
        ax.set_ylabel('Distance (in your model)')
        ax.set_title('Comparison of Measured and Expected Distances')
        ax.legend()
        
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)
        
        return render_template('results.html', accuracy=accuracy, errors=errors, 
                               average_accuracy=average_accuracy, graph_url=graph_url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
