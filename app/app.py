from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "app": "kubernetes-githubactions-fluxcd",
        "status": "running"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "app": "kubernetes-githubactions-fluxcd",
        "message": "Pipeline deployed successfully"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
