from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

@app.route('/')
def home():
    # Renders your HTML file from the templates folder
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_grades():
    data = request.get_json()
    grades = data.get('grades', [])
    
    # Validate
    valid_grades = [g for g in grades if isinstance(g, (int, float)) and 0 <= g <= 100]
    if not valid_grades:
        return jsonify({'error': 'No valid grades provided.'}), 400

    sorted_grades = quick_sort(valid_grades)

    # Make simple bins (for chart)
    bins = [0] * 21
    for g in sorted_grades:
        bins[g // 5] += 1

    return jsonify({
        'sorted': sorted_grades,
        'distribution': bins
    })

if __name__ == '__main__':
    app.run(debug=True)
