from flask import Flask, render_template
import pymysql
import boto3
import os

app = Flask(__name__)

# Config from Environment Variables
s3_bucket = os.environ.get('S3_BUCKET')
s3_filename = os.environ.get('S3_IMAGE_FILENAME')
student_name = os.environ.get('STUDENT_NAME', 'Group 1')

def download_image():
    if not s3_bucket: return None
    
    if not os.path.exists('static'):
        os.makedirs('static')
        
    local_path = os.path.join('static', s3_filename)
    
    if not os.path.exists(local_path):
        try:
            print(f"Log: Attempting to download {s3_filename} from {s3_bucket}")
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.download_file(s3_bucket, s3_filename, local_path)
            print(f"Log: Successfully downloaded background image: {s3_filename}")
        except Exception as e:
            print(f"Log: Error downloading from S3: {e}")
            return None
    return s3_filename

@app.route('/')
def home():
    img = download_image()
    return render_template('home.html', student_name=student_name, background_image=img)

if __name__ == '__main__':
    print("Log: Starting Flask app on port 81")
    app.run(host='0.0.0.0', port=81)
