<h1> SimulFCImage - LaBabaTcheam C1 </h1>
<h2>Project Goal</h2>
<p>SimulFCImage is a Python-based application designed for the manipulation of multispectral images,
allowing users to perceive them in color. With its intuitive user interface, it enables the selection of various simulation methods to generate these images.</p>
<p> The application offers several simulation methods for the creation of color images, including : </p>
<h3>"True Color" Generation Method :</h3>
<p>This method uses specific calculations to generate a true-color image, as it would be perceived by a human being.</p>
<p>Example of use: Visualizing a multispectral image as a human would see it, in order to compare it with other generated images.</p>
<h3>"False Color" Generation Method :</h3>
<p>This method allows users to select three bands from those available in the multispectral image and assign them to a color channel (Red, Green, Blue - RGB) to generate an image.</p>
<p>Example of use: Isolating the visualization of a specific wavelength to highlight elements invisible to the human eye.</p>
<h3>Bee Vision Simulation :</h3>
<p>This method generates an image simulating the perception of the multispectral image in the visible spectrum for a bee.</p>
<h3>Color Blindness Simulation :</h3>
<p>This method produces an image representing how a colorblind person would perceive the multispectral image.</p>
<h3>Main Features of the Application :</h3>
<ul>
  <li>Loading a multispectral image from a file.</li>
  <li>Selecting the image generation method.</li>
  <li>Computing and generating the image based on the chosen method.</li>
	<li>Displaying the generated image with the option to save it.</li>
</ul>

<h2>Project Architecture</h2>

```bash
C:.
│   .gitignore
│   Program.py
│   setup.py
│
├───Exceptions
│   │   NotExistingBandException.py
│
├───HMI
│   │   MainWindow.py
│   │   SimulationChoiceWindow.py
│   │
│   ├───assets
│   │       home-logo.png
│   │       Logo-iut-dijon-auxerre-nevers.png
│   │       Logo-laboratoire-ImViA.png
│   │       no-image.1024x1024.png
│
├───LogicLayer
│   │   Band.py
│   │   ImageMS.py
│   │
│   ├───Factory
│   │   │   SimulatorFactory.py
│   │   │
│   │   ├───CreateSimulating
│   │   │       CreateBandChoiceSimulating.py
│   │   │       CreateBeeSimulating.py
│   │   │       CreateDaltonianSimulating.py
│   │   │       CreateHumanSimulating.py
│   │   │       ICreateSimulator.py
│   │   │
│   │   └───Simulating
│   │           BandChoiceSimulating.py
│   │           BeeSimulating.py
│   │           DaltonianSimulating.py
│   │           HumanSimulating.py
│   │           SimulatingMethod.py
│   │
│
└───Storage
    │   FileManager.py
    │   ImageManager.py
```
