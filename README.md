<div align="center">
  
  <div>
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/pygame-00979D?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame" />
    <img src="https://img.shields.io/badge/neat-python-FF7F50?style=for-the-badge" alt="NEAT-Python" />
  </div>

  <h3 align="center">NEAT AI Flappy Bird</h3>
</div>

## 📋 Table of Contents

1. 🤖 [Introduction](#introduction)
2. ⚙️ [Tech Stack](#tech-stack)
3. 🔋 [Features](#features)
4. 🤸 [Quick Start](#quick-start)
5. 🕸️ [Snippets (Code to Copy)](#snippets)
6. 🔗 [Links](#links)

---

## <a name="introduction">🤖 Introduction</a>

This project implements a **NEAT AI-controlled Flappy Bird** using **Pygame** and **NEAT-Python**. The AI learns to navigate through obstacles by evolving its neural network over multiple generations.

NEAT (NeuroEvolution of Augmenting Topologies) is a genetic algorithm for training neural networks through evolution.

---

## <a name="tech-stack">⚙️ Tech Stack</a>

- Python
- Pygame
- NEAT-Python

---

## <a name="features">🔋 Features</a>

👉 **Neural Network Training**: Uses NEAT to evolve the AI for better performance.

👉 **Obstacle Navigation**: The AI learns to avoid pipes dynamically.

👉 **Real-Time Visualization**: Watch the AI train and improve over generations.

👉 **Customizable Configuration**: Modify `config-feedforward.txt` to tweak parameters.

---

## <a name="quick-start">🤸 Quick Start</a>

### **Prerequisites**
Ensure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/)

### **Cloning the Repository**

```bash
git clone https://github.com/Jonathan-Ultini/flappybird-ai.git
cd flappybird-ai
```

### **Installation**

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### **Running the Project**

```bash
python flappy_bird.py
```

Watch as the AI-controlled birds evolve and learn to navigate through the pipes!

---

## <a name="snippets">🕸️ Snippets</a>

<details>
<summary><code>NEAT Config Example</code></summary>

```ini
[NEAT]
pop_size = 10
fitness_threshold = 50
```

</details>

---

## <a name="links">🔗 Links</a>

- **NEAT-Python Docs** - [https://neat-python.readthedocs.io/en/latest/](https://neat-python.readthedocs.io/en/latest/)  
- **Pygame** - [https://www.pygame.org/](https://www.pygame.org/)  

Enjoy coding! 🚀

