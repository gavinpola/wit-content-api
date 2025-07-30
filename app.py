#!/usr/bin/env python3
"""
Main application entry point for Railway deployment
"""

from railway_deploy import app
import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False) 