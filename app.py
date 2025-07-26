import webview
import threading
from view import app  

def start_flask():
    """Run the Flask app."""
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    
    threading.Thread(target=start_flask, daemon=True).start()

    
    webview.create_window(
        title='AI Crop Recommendation',
        url='http://127.0.0.1:5000',
        width=1000, 
        height=600, 
        resizable=True,  
        zoomable=True  
    )
    webview.start(debug=True)  
