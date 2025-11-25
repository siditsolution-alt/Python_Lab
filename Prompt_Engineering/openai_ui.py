from flask import Flask, render_template, request, jsonify
from openai_api_service import OpenAIService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize OpenAI Service
try:
    openai_service = OpenAIService()
except ValueError as e:
    logger.error(f"Failed to initialize OpenAI service: {e}")
    openai_service = None


@app.route('/')
def index():
    """Render the main UI page."""
    return render_template('openai_ui.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """API endpoint to generate completion from prompt."""
    try:
        if not openai_service:
            return jsonify({'error': 'OpenAI service not initialized'}), 500
        
        data = request.get_json()
        
        # Validate required fields
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        # Extract parameters with defaults
        model = data.get('model', 'gpt-4o-mini')
        temperature = float(data.get('temperature', 0.7))
        top_p = float(data.get('top_p', 0.9))
        max_tokens = int(data.get('max_tokens', 1000))
        
        # Validate parameter ranges
        if not (0 <= temperature <= 2):
            return jsonify({'error': 'Temperature must be between 0 and 2'}), 400
        if not (0 <= top_p <= 1):
            return jsonify({'error': 'Top P must be between 0 and 1'}), 400
        if max_tokens < 1 or max_tokens > 4096:
            return jsonify({'error': 'Max tokens must be between 1 and 4096'}), 400
        
        logger.info(f"Generating completion for prompt: {prompt[:50]}...")
        
        # Generate completion
        response = openai_service.create_completion(
            prompt=prompt,
            model=model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'model': model,
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        return jsonify({'error': f'Error generating completion: {str(e)}'}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Return available models."""
    models = [
        'gpt-4o',
        'gpt-4o-mini',
        'gpt-4-turbo',
        'gpt-3.5-turbo'
    ]
    return jsonify({'models': models}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
