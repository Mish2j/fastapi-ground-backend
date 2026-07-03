"""
@app.post("/commands")
def send_command(request: CommandRequest):
    if request.command == SET_MODE_COMMAND:
        mode = request.params.get("mode")
        return set_mode(mode)

    return {
        "status": STATUS_REJECT,
        "message": f"Unknown command: {request.command}"
    }
"""