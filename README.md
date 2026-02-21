<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# Cognovoid 🎯

## Basic Details

### Team Name: DaisyCrux

### Team Members
- Member 1: Anna T Jeby - Muthoot Institute of Technology and Science,Varikoli
- Member 2:  Athira V - Muthoot Institute of Technology and Science,Varikoli

### Hosted Project Link
[mention your project hosted link here]

### Project Description
Cognovoid predicts a continuous stress score (0–10) from daily behavior inputs, calculates a cognitive risk score, and visualizes mental stability using interactive charts. The platform includes a friendly chatbot that guides users through the quiz and provides personalized recommendations to reduce stress and improve decision-making.
### The Problem statement
People often make poor decisions when mentally exhausted, overstressed, or emotionally reactive. Existing mental trackers display data but rarely provide real-time predictive insights or actionable guidance.### The Solution
We developed an interactive platform that:

Uses a chatbot to gently guide users through a behavioral quiz.

Predicts stress and cognitive risk using a trained XGBoost regression model.

Provides intuitive visualizations: doughnut charts for risk bands, radar charts for feature contributions, and energy curves for mental stability.

Offers personalized guidance to help users manage stress and avoid decision fatigue.


## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: JavaScript, Python, HTML, CSS
- Frameworks used: Flask (backend), Vanilla JS + HTML/CSS (frontend)
- Libraries used: XGBoost, pandas, numpy, matplotlib, Chart.js
- Tools used: VS Code, Jupyter Notebook, Git, Live Server

**For Hardware:**
- Main components: [List main components]
- Specifications: [Technical specifications]
- Tools required: [List tools needed]

---

## Features

List the key features of your project:
- Feature 1: Chatbot guidance: Friendly user interface that interacts before and during the quiz
- Feature 2: Gamified quiz input: Collects behavioral metrics via sliders and selects
- Feature 3: Stress prediction: XGBoost regression model outputs stress score and risk band
- Feature 4: Visual dashboards: Doughnut, radar, and energy curve visualizations
- Feature 5: Personalized guidance: Suggestions to reduce stress and improve cognitive stability
- Feature 6: History tracking: Saves previous quiz results for pattern analysis

---

## Implementation
### For Software:
Installation
  cd backend
    pip install -r requirements.txt
Train Model
  cd backend
    python train_model.py
Run Backend
  cd backend
    python app.py
Open Frontend Pages (via live server/static server)
  frontend/index.html
  frontend/quiz.html
  frontend/result.html

#### Installation
```bash
[Installation commands - e.g., npm install, pip install -r requirements.txt]
```

#### Run
```bash
[Run commands - e.g., npm start, python app.py]
```

### For Hardware:

#### Components Required
[List all components needed with specifications]

#### Circuit Setup
[Explain how to set up the circuit]

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

![Screenshot1] <img width="1854" height="927" alt="Landing" src="https://github.com/user-attachments/assets/d9d057f3-d15a-49bf-aec2-fb894e89f3ad" />

Landing page of Cognovoid showing the friendly chatbot interface that welcomes users and guides them to start the stress assessment quiz.

![Screenshot2] <img width="1350" height="911" alt="chatbot" src="https://github.com/user-attachments/assets/c1627d3a-03c4-422e-b7b5-02ba82346883" />

This screenshot shows the interactive chatbot in action, collecting the user’s initial mental state and guiding them through the behavioral quiz for stress and cognitive risk assessment.
![Screenshot3] <img width="1778" height="864" alt="chart" src="https://github.com/user-attachments/assets/8bb5ef7e-5a2f-4700-a0c2-d67bb2bff91e" />
![Screenshot4]<img width="1721" height="759" alt="curve" src="https://github.com/user-attachments/assets/07625145-29a9-4148-b823-aea53fe6f896" />

This screenshot shows the Energy Curve and Generalized Interpretation section of Cognovoid’s results page

#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)<img width="1536" height="1024" alt="SA Diagram" src="https://github.com/user-attachments/assets/e4be159a-6be4-4a46-9fab-9955d644acc3" />

Frontend
Mobile & Web App – Where users interact with the system, fill forms, view results, and get notifications.
Backend
API & Server – Processes requests, applies business logic, and communicates with the database and ML model.
Database – Stores users, stress scores, and app data (SQL/NoSQL).
External Services
ML Model – Predicts stress scores from user input.
Payment Gateway – Handles secure transactions (if any).
Flow

User → Frontend → Backend → ML Model & Database → Backend → Frontend
**Application Workflow:**

![Workflow](docs/workflow.png)
User → Frontend → Backend → ML Model & Database → Backend → Frontend

---

### For Hardware:

#### Schematic & Circuit

![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

#### Build Photos

![Team](Add photo of your team here)

![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `https://api.yourproject.com`

##### Endpoints

**GET /api/endpoint**
- **Description:** [What it does]
- **Parameters:**
  - `param1` (string): [Description]
  - `param2` (integer): [Description]
- **Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**POST /api/endpoint**
- **Description:** [What it does]
- **Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

[Add more endpoints as needed...]

---

### For Mobile Apps:

#### App Flow Diagram

![App Flow](docs/app-flow.png)
*Explain the user flow through your application*

#### Installation Guide

**For Android (APK):**
1. Download the APK from [Release Link]
2. Enable "Install from Unknown Sources" in your device settings:
   - Go to Settings > Security
   - Enable "Unknown Sources"
3. Open the downloaded APK file
4. Follow the installation prompts
5. Open the app and enjoy!

**For iOS (IPA) - TestFlight:**
1. Download TestFlight from the App Store
2. Open this TestFlight link: [Your TestFlight Link]
3. Click "Install" or "Accept"
4. Wait for the app to install
5. Open the app from your home screen

**Building from Source:**
```bash
# For Android
flutter build apk
# or
./gradlew assembleDebug

# For iOS
flutter build ios
# or
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug
```

---

### For Hardware Projects:

#### Bill of Materials (BOM)

| Component | Quantity | Specifications | Price | Link/Source |
|-----------|----------|----------------|-------|-------------|
| Arduino Uno | 1 | ATmega328P, 16MHz | ₹450 | [Link] |
| LED | 5 | Red, 5mm, 20mA | ₹5 each | [Link] |
| Resistor | 5 | 220Ω, 1/4W | ₹1 each | [Link] |
| Breadboard | 1 | 830 points | ₹100 | [Link] |
| Jumper Wires | 20 | Male-to-Male | ₹50 | [Link] |
| [Add more...] | | | | |

**Total Estimated Cost:** ₹[Amount]

#### Assembly Instructions

**Step 1: Prepare Components**
1. Gather all components listed in the BOM
2. Check component specifications
3. Prepare your workspace
![Step 1](images/assembly-step1.jpg)
*Caption: All components laid out*

**Step 2: Build the Power Supply**
1. Connect the power rails on the breadboard
2. Connect Arduino 5V to breadboard positive rail
3. Connect Arduino GND to breadboard negative rail
![Step 2](images/assembly-step2.jpg)
*Caption: Power connections completed*

**Step 3: Add Components**
1. Place LEDs on breadboard
2. Connect resistors in series with LEDs
3. Connect LED cathodes to GND
4. Connect LED anodes to Arduino digital pins (2-6)
![Step 3](images/assembly-step3.jpg)
*Caption: LED circuit assembled*

**Step 4: [Continue for all steps...]**

**Final Assembly:**
![Final Build](images/final-build.jpg)
*Caption: Completed project ready for testing*

---

### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
```

#### Demo Output

**Example 1: Basic Processing**

**Input:**
```
This is a sample input file
with multiple lines of text
for demonstration purposes
```

**Command:**
```bash
python script.py sample.txt
```

**Output:**
```
Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
```

**Example 2: Advanced Usage**

**Input:**
```json
{
  "name": "test",
  "value": 123
}
```

**Command:**
```bash
python script.py -v --format json data.json
```

**Output:**
```
[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
```

---

## Project Demo

### Video
[Add your demo video link here - YouTube, Google Drive, etc.]

*Explain what the video demonstrates - key features, user flow, technical highlights*

### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:**  GitHub Copilot,ChatGPT

**Purpose:**
- Code suggestions, algorithm explanations, frontend-backend integration guidance

**Key Prompts Used:**
- "Debug this async function that's causing race conditions"

**Percentage of AI-generated code:** [Approximately 15%]

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

*Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!*

---

## Team Contributions

- Anna T Jeby: Frontend development,chatbot integration, result visualization
-  Athira V]: Backend development, XGBoost model training, API creation, system architecture
---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
