# Egalitarian Monologue

Discussion participants visualization app.

## README part

### Premise

Participants are more aware of how much they talk when they can see it.
It helps loud people to slow down and quiet people to speak up.

### Dependences

- Flask
- Speechmatics
- HTML5 with Canvas API

### Setup & Installation

#### Prerequisites

- [Speechmatics API key](https://portal.speechmatics.com/dashboard)
- Python

#### Build

1.  Clone the repo

    ```bash
    git clone <repository-url>
    cd egalitarian_monologue
    ```

2.  Create and setup a python virtual environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

    > [!note]
    > On Linux, you need to install libasound2-dev.

4.  Export API key as env var

    ```bash
    export SPEECHMATICS_API_KEY=your_api_key_here
    ```

5.  Run python app

    ```bash
    python app/main.py
    ```

6.  Webapp

    Open your browser and go to `http://localhost:5000`.

### Testing

If you do not have a Speechmatics API key, you can enable the mock simulation mode in `app/main.py` to test the visualization logic.

1.  Open `app/main.py`.
2.  Uncomment the simulation thread and comment out the main loop:

    ```python
    # sm_thread = threading.Thread( target=start_async_loop, daemon=True )
    sm_thread = threading.Thread( target=mock_speechmatics_simulation, daemon=True )  # mock sim
    ```

3.  Restart the application.
