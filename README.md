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

## Wiki part

### Scientific Basis

This project is based on research demonstrating that real-time visual feedback
can improve the experience for discussion participants.

### Main sources

- [A. Pentland, T. Kim and A. Chang, "Meeting Mediator: Enchancing Group Collaboration and Leadership with Sociometric Feedback"](https://www.media.mit.edu/publications/meeting-mediator-enhancing-group-collaboration-and-leadership-with-sociometric-feedback/)
- [T. Bergstrom and K. Karahalios, "Conversation Clock: Visualizing audio patterns in co-located groups"](https://ieeexplore.ieee.org/document/4076529)

#### 1. The Meeting Mediator

*   **Setup** 
    The team developed a system using "sociometric badges" worn by participants.
    These devices measured speaking time, turn-taking patterns, and body
    movement without recording content. A visual display provided real-time
    feedback on the group's interactivity and balance.

*   **Findings**
    The study found that visual feedback significantly reduced the dominance of
    over-participating members and encouraged quieter members to speak up. Groups with the feedback loop scored higher on the "social signaling"
    balance. The term is correlated with higher group intelligence and better
    decision making within the group.

#### 2. The Conversation Clock

*   **Setup**
    This project utilized a tabletop visualization where the history of the
    conversation was projected as concentric circles (clock shaped, hence the
    name). As time passed, the visualization grew, with color-coded segments
    representing who was speaking at any given moment.

*   **Findings**
    Users reported increased self-awareness and voluntarily adjusted their
    behavior to create a more balanced conversation, showing that visual cues
    can effectively regulate social interaction.

### Our implementation

Egalitarian Monologue uses a real time diarization model, only requiring a
microphone to function. The speaker categorizations made by the model are output
onto the web dashboard. The visual part of the app acts as the "social mirror",
nudging people towards egalitarian discussion (project name genesis 🤯).
