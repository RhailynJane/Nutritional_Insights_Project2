"""
Nutritional Insights Backend API
Flask server that provides REST endpoints for nutritional data from CSV
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Path to CSV file
CSV_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'All_Diets.csv'
)

def load_nutrition_data():
    """Load and process nutrition data from CSV"""
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f"Error loading CSV: {e}")
        return None

def calculate_diet_summary(df):
    """Calculate average macronutrients and recipe counts by diet type"""
    summary = df.groupby('Diet_type').agg({
        'Protein(g)': 'mean',
        'Carbs(g)': 'mean',
        'Fat(g)': 'mean',
        'Recipe_name': 'count'
    }).reset_index()

    summary.columns = ['Diet_type', 'Protein', 'Carbs', 'Fat', 'recipes']

    return summary.to_dict('records')

def get_top_protein_recipes(df, limit=5):
    """Get top protein-rich recipes"""
    cols = ['Recipe_name', 'Protein(g)', 'Carbs(g)']
    top_recipes = df.nlargest(limit, 'Protein(g)')[cols]

    result = []
    for _, row in top_recipes.iterrows():
        result.append({
            'recipe': row['Recipe_name'],
            'protein': round(row['Protein(g)'], 1),
            'carbs': round(row['Carbs(g)'], 1)
        })

    return result

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Nutritional Insights API is running'
    })

@app.route('/api/nutrition/summary', methods=['GET'])
def get_nutrition_summary():
    """Get aggregated nutrition data by diet type"""
    df = load_nutrition_data()

    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500

    diet_summary = calculate_diet_summary(df)

    return jsonify({
        'status': 'success',
        'total_records': len(df),
        'diet_types': len(diet_summary),
        'data': diet_summary
    })

@app.route('/api/recipes/top-protein', methods=['GET'])
def get_top_protein():
    """Get top protein-rich recipes"""
    limit = request.args.get('limit', default=5, type=int)

    df = load_nutrition_data()

    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500

    top_recipes = get_top_protein_recipes(df, limit)

    return jsonify({
        'status': 'success',
        'count': len(top_recipes),
        'data': top_recipes
    })

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes with optional filtering"""
    df = load_nutrition_data()

    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500

    # Optional diet type filter
    diet_type = request.args.get('diet_type')
    if diet_type:
        df = df[df['Diet_type'].str.lower() == diet_type.lower()]

    # Calculate statistics
    stats = {
        'total_recipes': len(df),
        'avg_protein': round(df['Protein(g)'].mean(), 2),
        'avg_carbs': round(df['Carbs(g)'].mean(), 2),
        'avg_fat': round(df['Fat(g)'].mean(), 2)
    }

    return jsonify({
        'status': 'success',
        'statistics': stats
    })

@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    """Get cluster analysis of diet types"""
    df = load_nutrition_data()

    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500

    summary = calculate_diet_summary(df)

    # Simple clustering logic based on macronutrient profiles
    high_protein = [d['Diet_type'] for d in summary if d['Protein'] > 90]
    high_carb = [d['Diet_type'] for d in summary if d['Carbs'] > 200]
    balanced = [
        d['Diet_type'] for d in summary
        if d['Diet_type'] not in high_protein
        and d['Diet_type'] not in high_carb
    ]

    return jsonify({
        'status': 'success',
        'clusters_identified': 3,
        'high_protein_cluster': high_protein,
        'high_carb_cluster': high_carb,
        'balanced_cluster': balanced
    })

@app.route('/api/nutrition/all', methods=['GET'])
def get_all_data():
    """Get complete nutrition dataset with pagination"""
    df = load_nutrition_data()

    if df is None:
        return jsonify({'error': 'Failed to load data'}), 500

    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    total_records = len(df)
    total_pages = (total_records + per_page - 1) // per_page

    # Get page data
    page_data = df.iloc[start_idx:end_idx].to_dict('records')

    return jsonify({
        'status': 'success',
        'page': page,
        'per_page': per_page,
        'total_records': total_records,
        'total_pages': total_pages,
        'data': page_data
    })

if __name__ == '__main__':
    # Run the Flask app
    print("Starting Nutritional Insights API...")
    print(f"CSV Path: {CSV_PATH}")
    # Use environment variable to control debug mode
    # For production, set FLASK_ENV=production
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
