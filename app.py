import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import cv2
import numpy as np
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
