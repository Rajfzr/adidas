from market import app

if __name__ == '__main__':
    start_keep_alive_thread()
    app.run(debug=False)