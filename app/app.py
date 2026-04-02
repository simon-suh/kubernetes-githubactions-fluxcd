from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "app": "kubernetes-githubactions-fluxcd",
        "status": "running",
        "version": "2.0.0"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "app": "kubernetes-githubactions-fluxcd",
        "message": "Pipeline deployed successfully",
        "version": "2.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
