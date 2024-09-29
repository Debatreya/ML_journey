# End to End Toy Project

## Model for predicting if a student will get placement based on `iq` and `cgpa`

### Dataset
[placement.csv](./Data/placement.csv)
### Notebook 
[index.ipynb](./Notebook/index.ipynb)
### Model (generated model)
[model.pkl](./Model/model.pkl)

### Fullstack app STEPS (How to use the .pkl file)


import sys
import pickle
import numpy as np

## Using `model.pkl` in a MERN Based Full Stack Project

To use the `model.pkl` file in a MERN (MongoDB, Express, React, Node.js) based full stack project, follow these steps:

### 1. Set Up the Backend

1. **Install Required Packages**:
    Ensure you have `express`, `body-parser`, and `child_process` installed in your Node.js backend.

    ```bash
    npm install express body-parser child_process
    ```

2. **Create a Python Script**:
    Create a Python script (`predict.py`) that loads the model and makes predictions.

    ```python

    # Load the model
    model = pickle.load(open('model.pkl', 'rb'))

    # Read input data from command line
    input_data = np.array([float(x) for x in sys.argv[1:]]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)

    # Print the prediction
    print(prediction[0])
    ```

3. **Create an Express Server**:
    Create an Express server (`server.js`) that handles API requests and calls the Python script.

    ```javascript
    const express = require('express');
    const bodyParser = require('body-parser');
    const { spawn } = require('child_process');

    const app = express();
    const PORT = process.env.PORT || 5000;

    app.use(bodyParser.json());

    app.post('/predict', (req, res) => {
         const { cgpa, iq } = req.body;

         // Call the Python script
         const pythonProcess = spawn('python', ['predict.py', cgpa, iq]);

         pythonProcess.stdout.on('data', (data) => {
              res.json({ prediction: data.toString() });
         });

         pythonProcess.stderr.on('data', (data) => {
              console.error(`stderr: ${data}`);
              res.status(500).send('Error occurred');
         });
    });

    app.listen(PORT, () => {
         console.log(`Server is running on port ${PORT}`);
    });
    ```

### 2. Set Up the Frontend

1. **Create a React Component**:
    Create a React component (`PredictForm.js`) that collects input data and sends it to the backend.

    ```javascript
    import React, { useState } from 'react';
    import axios from 'axios';

    const PredictForm = () => {
         const [cgpa, setCgpa] = useState('');
         const [iq, setIq] = useState('');
         const [prediction, setPrediction] = useState(null);

         const handleSubmit = async (e) => {
              e.preventDefault();
              try {
                    const response = await axios.post('/predict', { cgpa, iq });
                    setPrediction(response.data.prediction);
              } catch (error) {
                    console.error('Error making prediction', error);
              }
         };

         return (
              <div>
                    <form onSubmit={handleSubmit}>
                         <div>
                              <label>CGPA:</label>
                              <input type="number" value={cgpa} onChange={(e) => setCgpa(e.target.value)} required />
                         </div>
                         <div>
                              <label>IQ:</label>
                              <input type="number" value={iq} onChange={(e) => setIq(e.target.value)} required />
                         </div>
                         <button type="submit">Predict</button>
                    </form>
                    {prediction && <div>Prediction: {prediction}</div>}
              </div>
         );
    };

    export default PredictForm;
    ```

2. **Integrate the Component**:
    Integrate the `PredictForm` component into your main React application.

    ```javascript
    import React from 'react';
    import ReactDOM from 'react-dom';
    import PredictForm from './PredictForm';

    const App = () => (
         <div>
              <h1>Placement Prediction</h1>
              <PredictForm />
         </div>
    );

    ReactDOM.render(<App />, document.getElementById('root'));
    ```

### 3. Run the Application

1. **Start the Backend**:
    ```bash
    node server.js
    ```

2. **Start the Frontend**:
    ```bash
    npm start
    ```

Now, you should have a full stack MERN application where users can input their CGPA and IQ to get a placement prediction using the trained model.