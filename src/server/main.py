


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    import web
    web.app.run(port=5001, debug=True, threaded=True)
