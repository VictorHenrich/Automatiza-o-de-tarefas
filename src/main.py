from start import app


@app.initialize
def run_shell():
    import tasks

    app.cli.execute()


app.start()