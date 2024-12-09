from flask import Flask, render_template, Response
import subprocess
import os

app = Flask(__name__)

def capture_image():
    # Capture image from the camera using raspistill (legacy camera stack)
    image_path = '/tmp/capture.jpg'
    command = ['raspistill', '-o', image_path]
    
    # Run the command to capture the image
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error capturing image: {e}")
        return None
    return image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    # Capture the image and check if it was successful
    image_path = capture_image()
    if image_path and os.path.exists(image_path):
        return render_template('index.html', captured=True)
    else:
        return render_template('index.html', captured=False, error="Failed to capture image")

@app.route('/image')
def image():
    # Serve the captured image
    image_path = '/tmp/capture.jpg'
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            return Response(f.read(), mimetype='image/jpeg')
    else:
        return 'Image not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

