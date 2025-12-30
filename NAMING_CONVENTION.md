# Naming Convention for Trained Models

To ensure consistent tracking of training iterations, all finished model files (`.zip` archives) must adhere to the following naming convention:

**Format:**
`[Model_Name]_[Last_Training_Concept]_[MM-DD-HHmm]`

**Variables:**
*   `[Model_Name]`: The agent being trained (e.g., `Megaman`, `Headcrab`, `Tinpet`).
*   `[Last_Training_Concept]`: A brief descriptor of the training goal or curriculum (e.g., `SlowTeacher`, `RayCastV1`, `PushupAttempt`).
*   `[MM-DD-HHmm]`: The date and time of completion in **PST Military Time** (e.g., `12-30-1430`).

**Examples:**
*   `Megaman_SlowTeacher_12-30-0845.zip`
*   `Headcrab_RayCastGround_12-30-0915.zip`

**Implementation:**
*   This convention applies to final artifacts retrieved from the Dojo (Colab).
*   Scripts like `retrieve_brain.py` should ideally rename the fetched file to match this format upon decryption.
