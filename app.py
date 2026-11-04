import os
os.environ['FLASK_SKIP_DOTENV'] = '1'

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    print(f"\n* TransitNotice running on http://127.0.0.1:{port}")
    print("* Covering All 38 Districts of Tamil Nadu")
    print("* Press CTRL+C to quit\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
