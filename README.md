# Radetzky

Add randomised claps to detected beats on any audio file!

## Motivation

2021's [Vienna New Year's Concert](https://en.wikipedia.org/wiki/Vienna_New_Year%27s_Concert) was the very first ran without an audience.

The [Radetzky March](https://www.youtube.com/watch?v=2ORHVroiWHk) is a staple in the concert, usually the last encore piece played. The audience usually claps along to the music.

Riccardo Muti, the conductor of the 2021 edition, mentioned that "This is the first time the audience can listen to the March without the clapping". I thought it was weird, and hence this project is born.

## Try it out!

### Requirements
- Python 3
- Dependencies: 
    ```bash 
    pip install -r requirements.txt
    ```

### Running
- Place source audio (only 44.1kHz files supported as of now) in `data/`.
- Tweak the `Parameters` section in `main.py`.
- Run the code!
    ```bash
    python main.py
    ```
- Output is in `output/` with the same file name as the source's.

## Acknowledgements
- Clapping sound effect: see its [README](sounds/claps/README.md) for attribution
- Beat tracker ([`madmom`](https://madmom.readthedocs.io/)):
    - Sebastian Böck, Florian Krebs and Gerhard Widmer, “A Multi-Model Approach to Beat Tracking Considering Heterogeneous Music Styles”, Proceedings of the 15th International Society for Music Information Retrieval Conference (ISMIR), 2014.
    - Florian Krebs, Sebastian Böck and Gerhard Widmer, “An Efficient State Space Model for Joint Tempo and Meter Tracking”, Proceedings of the 16th International Society for Music Information Retrieval Conference (ISMIR), 2015.
    