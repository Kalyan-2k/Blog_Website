from Routes import create_app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)
    # app.run(host='0.0.0.0')   # experiment
