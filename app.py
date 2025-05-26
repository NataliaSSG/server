from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime
from flask_cors import CORS

load_dotenv()
url = os.getenv("URL")
key = os.getenv("KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    response = supabase.table('mensajes').select('*').execute()
    print(response.data)  
    return jsonify(response.data), 200


@app.route('/post-message', methods=['POST'])
def post_message():
    data = request.get_json()

    # Validate required fields
    if not data or 'usuario' not in data or 'mensaje' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    current_time = datetime.now()
    fecha = current_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    try:
        # Insert into Supabase
        response = supabase.table('mensajes').insert({
            'usuario': data['usuario'],
            'mensaje': data['mensaje'],
            'fecha': fecha
        }).execute()

        # Check if response contains data (successful insert)
        if response.data:
            return jsonify({'message': 'Message inserted successfully', 'data': response.data}), 201
        else:
            return jsonify({'error': 'Failed to insert message', 'details': 'No data returned'}), 500

    except Exception as e:
        # Handle any errors from Supabase
        return jsonify({'error': 'Failed to insert message', 'details': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)