from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from backend.database import LaserTagDatabase
from backend.config import DATABASE_CONFIG
import threading
import socket
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

db = LaserTagDatabase(**DATABASE_CONFIG)

udp_broadcast_socket = None
udp_receive_socket = None
current_network_address = "127.0.0.1"
broadcast_port = 7500
receive_port = 7501


#sets up udp sockets for broadcast and receieve
def setup_udp_sockets():
    global udp_broadcast_socket, udp_receive_socket
    
    try:
        udp_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.info(f"UDP broadcast socket created for port {broadcast_port}")
        
        udp_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_receive_socket.bind(('', receive_port))
        udp_receive_socket.settimeout(1.0)
        logger.info(f"UDP receive socket created for port {receive_port}")
        
        return True
    except Exception as e:
        logger.error(f"UDP setup failed: {e}")
        return False

#broadcasts equipment id to all devices on the network
def broadcast_equipment_id(equipment_id):
    global udp_broadcast_socket, current_network_address, broadcast_port
    
    try:
        if udp_broadcast_socket:
            message = str(equipment_id).encode()
            udp_broadcast_socket.sendto(message, (current_network_address, broadcast_port))
            logger.info(f"Broadcasted equipment ID: {equipment_id}")
            return True
    except Exception as e:
        logger.error(f"Broadcast failed for {equipment_id}: {e}")
        return False

#receives udp messages from other devices on the network
def udp_receiver_thread():
    global udp_receive_socket
    
    while True:
        try:
            if udp_receive_socket:
                data, addr = udp_receive_socket.recvfrom(1024)
                received_message = data.decode().strip()
                logger.info(f"Received UDP message: {received_message} from {addr}")
                process_received_udp_data(received_message)
                
        except socket.timeout:
            continue
        except Exception as e:
            logger.error(f"UDP receiver error: {e}")
            time.sleep(1)

#processes received udp data
def process_received_udp_data(message):
    try:
        if ':' in message:
            transmitting_id, hit_id = message.split(':')
            logger.info(f"Player {transmitting_id} hit player {hit_id}")
            broadcast_equipment_id(int(hit_id))
            
        elif message.isdigit():
            equipment_id = int(message)
            logger.info(f"Received single equipment ID: {equipment_id}")
            
            if equipment_id == 53:
                logger.info("Red base scored!")
            elif equipment_id == 43:
                logger.info("Green base scored!")
                
    except Exception as e:
        logger.error(f"Failed to process UDP data '{message}': {e}")

#gets all players from the database
@app.route('/players', methods=['GET'])
def get_all_players():
    try:
        if not db.test_connection():
            return jsonify({'error': 'Database connection failed'}), 500
            
        players = db.get_all_players()
        players_list = [{'id': pid, 'codename': codename} for pid, codename in players]
        
        return jsonify({
            'players': players_list,
            'count': len(players_list)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting all players: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#adds a player to the database
@app.route('/players', methods=['POST'])
def add_player():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        player_id = data.get('id')
        codename = data.get('codename')
        equipment_id = data.get('equipment_id')
        
        if player_id is None:
            return jsonify({'error': 'Player ID is required'}), 400
            
        if not isinstance(player_id, int):
            return jsonify({'error': 'Player ID must be an integer'}), 400
        
        existing_codename = db.get_player_by_id(player_id)
        
        if existing_codename and not codename:
            return jsonify({
                'id': player_id,
                'codename': existing_codename,
                'message': 'Player already exists'
            }), 200
            
        if not codename:
            return jsonify({'error': 'Codename is required for new players'}), 400
            
        if db.add_player(player_id, codename):
            if equipment_id:
                broadcast_equipment_id(equipment_id)
                
            return jsonify({
                'id': player_id,
                'codename': codename,
                'equipment_id': equipment_id,
                'message': 'Player added successfully'
            }), 201
        else:
            return jsonify({'error': 'Failed to add player to database'}), 500
            
    except Exception as e:
        logger.error(f"Error adding player: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#gets a player from the database
@app.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    try:
        codename = db.get_player_by_id(player_id)
        
        if codename:
            return jsonify({
                'id': player_id,
                'codename': codename
            }), 200
        else:
            return jsonify({'error': 'Player not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting player {player_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#clears all players from the database

@app.route('/players', methods=['DELETE'])
def clear_all_players():
    try:
        if db.clear_all_players():
            return jsonify({'message': 'All players cleared successfully'}), 200
        else:
            return jsonify({'error': 'Failed to clear players'}), 500
            
    except Exception as e:
        logger.error(f"Error clearing players: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#sets the network address for the udp sockets
@app.route('/network', methods=['POST'])
def set_network_address():
    global current_network_address
    
    try:
        data = request.get_json()
        new_address = data.get('address')
        
        if not new_address:
            return jsonify({'error': 'Network address is required'}), 400
            
        current_network_address = new_address
        logger.info(f"Network address changed to: {new_address}")
        
        return jsonify({
            'message': 'Network address updated',
            'address': current_network_address
        }), 200
        
    except Exception as e:
        logger.error(f"Error setting network address: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#gets the network address for the udp sockets
@app.route('/network', methods=['GET'])
def get_network_info():
    return jsonify({
        'address': current_network_address,
        'broadcast_port': broadcast_port,
        'receive_port': receive_port
    }), 200

#broadcasts an equipment id to the network
@app.route('/broadcast/<int:equipment_id>', methods=['POST'])
def broadcast_id(equipment_id):
    try:
        if broadcast_equipment_id(equipment_id):
            return jsonify({
                'message': f'Equipment ID {equipment_id} broadcasted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to broadcast equipment ID'}), 500
            
    except Exception as e:
        logger.error(f"Broadcast failed for {equipment_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


#starts the game
@app.route('/game/start', methods=['POST'])
def start_game():
    try:
        if broadcast_equipment_id(202):  # Game start code
            return jsonify({'message': 'Game started - code 202 broadcasted'}), 200
        else:
            return jsonify({'error': 'Failed to broadcast game start'}), 500
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#ends the game
@app.route('/game/end', methods=['POST'])
def end_game():
    try:
        # Broadcast code 221 three times as required
        for i in range(3):
            if not broadcast_equipment_id(221):
                return jsonify({'error': f'Failed to broadcast game end (attempt {i+1})'}), 500
            time.sleep(0.1)  # delay between broadcasts
            
        return jsonify({'message': 'Game ended - code 221 broadcasted 3 times'}), 200
    except Exception as e:
        logger.error(f"Error ending game: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#health checks
@app.route('/health', methods=['GET'])
def health_check():
    db_status = db.test_connection()
    return jsonify({
        'status': 'healthy' if db_status else 'unhealthy',
        'database': 'connected' if db_status else 'disconnected',
        'udp_sockets': 'active' if udp_broadcast_socket and udp_receive_socket else 'inactive'
    }), 200 if db_status else 503

#runs server
def start_server():
    # Verify database connectivity directly; avoid executing external scripts which
    # may require sudo or prompt for passwords when running the server.
    logger.info("Verifying database connectivity...")

    if not db.test_connection():
        logger.error("Failed to connect to database.")
        return False
    
    if not setup_udp_sockets():
        logger.error("Failed to set up UDP sockets.")
        return False
    
    udp_thread = threading.Thread(target=udp_receiver_thread, daemon=True)
    udp_thread.start()
    logger.info("UDP receiver thread started")
    
    logger.info("Starting Laser Tag API server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    return True

if __name__ == '__main__':
    start_server()
