from flask import Flask, request, send_file
import gpxpy
import gpxpy.gpx
from xml.etree import ElementTree as ET
import os

app = Flask(__name__)

def kml_to_gpx(kml_content):
    # Parse KML
    kml_root = ET.fromstring(kml_content)
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = kml_root.find('.//kml:coordinates', namespaces)
    
    if coordinates is None:
        raise ValueError("No coordinates found in KML file.")

    # Create GPX
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add points to GPX
    for coord in coordinates.text.strip().split():
        lon, lat, alt = map(float, coord.split(','))
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=alt))

    return gpx.to_xml()

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    kml_content = file.read().decode('utf-8')
    gpx_content = kml_to_gpx(kml_content)

    # Save GPX to a temporary file
    gpx_filename = 'converted.gpx'
    with open(gpx_filename, 'w') as f:
        f.write(gpx_content)

    return send_file(gpx_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)