import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

STATE_FILE = 'data/game_state.json'
SCORES_FILE = 'data/scores.json'


def load_json(path, default):
    """Read JSON from a file, or return default if the file doesn't exist."""
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Save Python data as JSON into a file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def home():
    return "Welcome to Saving Benny!"


@app.route('/api/scores', methods=['GET'])
def get_scores():
    scores = load_json(SCORES_FILE, [])
    return jsonify(scores)


@app.route('/api/start', methods=['POST'])
def start_game():
    state = {
        'stage': 'park',
        'lives': 3,
        'collar_checkpoint': False,
        'has_flashlight': False,
        'has_benny': False,
        'status': 'playing',
        'message': 'Benny is chasing a squirrel in the park!'
    }
    save_json(STATE_FILE, state)
    return jsonify(state)


@app.route('/api/collect', methods=['POST'])
def collect_item():
    item = (request.get_json(silent=True) or {}).get('item')
    state = load_json(STATE_FILE, {})

    if item == 'collar':
        state['collar_checkpoint'] = True
        state['message'] = "Found Benny's collar! Checkpoint saved."
    elif item == 'flashlight':
        state['has_flashlight'] = True
        state['message'] = 'Collected the flashlight!'

    save_json(STATE_FILE, state)
    return jsonify(state)


@app.route('/api/choice', methods=['POST'])
def make_choice():
    choice = (request.get_json(silent=True) or {}).get('choice')
    state = load_json(STATE_FILE, {})

    if choice == 'beach':
        state['lives'] -= 1
        if state['lives'] <= 0:
            state['status'] = 'game_over'
            state['message'] = 'You died at the beach! Out of lives.'
        else:
            state['stage'] = 'collar_checkpoint'
            state['message'] = 'Wrong route! Respawned at the collar checkpoint.'

    elif choice == 'cave':
        state['stage'] = 'cave'
        state['message'] = 'Entered the cave! Watch for skulls and grab the flashlight.'

    elif choice == 'cavemen':
        state['lives'] -= 1
        if state['lives'] <= 0:
            state['status'] = 'game_over'
            state['message'] = 'Caught by the cavemen! Game Over.'
        else:
            state['message'] = 'Cavemen route! You lost a life—try the other way.'

    elif choice == 'shortcut':
        state['has_benny'] = True
        state['stage'] = 'return'
        state['message'] = 'You got Benny! Now run back!'

    elif choice == 'hole':
        state['lives'] = max(0, state['lives'] - 1)
        state['status'] = 'game_over'
        state['message'] = 'You fell into the hole! Game Over.'

    elif choice == 'forest':
        state['status'] = 'victory'
        state['message'] = 'Well done! You saved Benny and cleared the game!'
        scores = load_json(SCORES_FILE, [])
        scores.append({
            'lives_left': state['lives'],
            'flashlight': state['has_flashlight']
        })
        save_json(SCORES_FILE, scores)

    save_json(STATE_FILE, state)
    return jsonify(state)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)