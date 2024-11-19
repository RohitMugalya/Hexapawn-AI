# Hexapawn AI  

**Hexapawn AI** is a fascinating blend of classic gameplay and adaptive artificial intelligence, designed to both entertain and educate. Inspired by the classic Hexapawn game, this project introduces an AI opponent that mimics human learning behavior by following a *review-reflect-reinforce* approach. Each time the AI loses a game, it "remembers" the unsuccessful moves and avoids repeating them in future matches, steadily improving its gameplay. This makes every match a progressively challenging experience, offering players a chance to sharpen their strategic thinking.  

Built with modularity in mind, the project offers two ways to engage with the game: a minimalist **Command-Line Interface (CLI)** for a quick, focused experience, and a visually appealing **Graphical User Interface (GUI)** with drag-and-drop functionality powered by Pygame. Whether you're exploring the AI's decision-making process or simply enjoying a casual match, Hexapawn AI bridges the gap between entertainment and education in an open-source format. Perfect for enthusiasts looking to learn about AI, Python programming, or game development!  

---

## How to Run?  

Getting started with **Hexapawn AI** is simple! Follow these steps to set up and run the program on your system:  

### Prerequisites  

- Ensure you have **Python 3.9 or higher** installed on your system.  

---

### Steps  

1. **Clone the repository**
 ```
 git clone https://github.com/RohitMugalya/Hexapawn-AI.git
 cd Hexapawn-AI
```
2. **Create and activate virtual environment**
   ```
   python -m venv venv
   ```
     - on Linux system
     ```
     source venv/bin/activate
     ```
     - on Windows system
     ```
     .\venv\Scripts\activate.bat
     ```
3. **Install the requirements**
```
pip install  -r requirements.txt
```
4. **Run the program**
   - For Graphical user interface
   ```
   python gui.py
   ```
   - For Command line interface
   ```
   python cli.py
   ```
