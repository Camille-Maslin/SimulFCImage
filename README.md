<h1> SimulFCImage - LaBabaTcheam C1 </h1>

<h2>Project Goal</h2>
<p>SimulFCImage is a Python-based application designed for the manipulation of multispectral images,
allowing users to perceive them in color. With its intuitive user interface, it enables the selection of various simulation methods to generate these images.
The application offers several simulation methods for the creation of color images, including:</p>

<h3>"True Color" Generation Method:</h3>
<p>This method uses specific calculations to generate a true-color image, as it would be perceived by a human being.
Example of use: Visualizing a multispectral image as a human would see it, in order to compare it with other generated images.</p>

<h3>"False Color" Generation Method:</h3>
<p>This method allows users to select three bands from those available in the multispectral image and assign them to a color channel (Red, Green, Blue - RGB) to generate an image.
Example of use: Isolating the visualization of a specific wavelength to highlight elements invisible to the human eye.</p>

<h3>Bee Vision Simulation:</h3>
<p>This method generates an image simulating the perception of the multispectral image in the visible spectrum for a bee.</p>

<h3>Color Blindness Simulation:</h3>
<p>This method produces an image representing how a colorblind person would perceive the multispectral image.</p>

<h3>Main Features of the Application:</h3>
<ul>
  	<li>Loading a multispectral image from a file.</li>
  	<li>Selecting the image generation method.</li>
  	<li>Computing and generating the image based on the chosen method.</li>
	<li>Displaying the generated image with the option to save it.</li>
</ul>

<h2>How to use the application?</h2> 

<h3>Situation 1: You want the application compiled as an .exe file</h3>

<h4>Setup:</h4>
<p>Download the SimulFCImage.zip file in this Google Drive: https://drive.google.com/drive/folders/1uRv_wMsNEgHqScpr94n4Br1E7VYtcmYx?usp=sharing</p>
<p>(You may want to download the .tif data files with their metadata .txt in the folder "Teeth" present in the Google Drive with the application)</p>
<p>Unzip the SimulFCImage.zip.</p>
<p>Launch the application SimulFCImage.exe. </p>
<p>A window will open with a button labeled "Import an image."</p>
<p>Click this button and select your multispectral images in .tiff format.</p>
<p>Then you will need to import the metadata file in .txt format present with the .tiff image.</p>
<p>Once you click OK, your image will appear in the application.</p>
<p>You can view each band of the image by clicking the "Next" and "Previous" buttons.</p>

<h3>Generate a color image:</h3>

<h4>RGB bands choice:</h4>
<p>The "RGB bands choice" method is available in the "Generate a color image" window.
First of all, you need to select the "RGB bands choice" radio button.
You will then need to indicate in the "R", "G", and "B" spinboxes the band number you want to assign to each "RGB" channel.
Then you can proceed with the method.
If everything went well, you should see your newly generated image in the first window of the application next to your imported multispectral image.</p>

<h4>Save button:</h4>
<p>After the generation of your new image, the button "Save" under your newly generated image in the first window of the application is available. If you want to download your image in an RGB format (.png, .jpg), you simply need to click the "Save" button and choose where you want the image file to go.</p>

<br>

<h3>Situation 2: You are using git clone to compile the project yourself</h3>

<p>First, you need to install a few Python libraries. Run the following command in your command prompt (CMD): </p>

```bash
pip install Pillow rasterio numpy cx_Freeze
```

<p>Once the installation is complete, you can compile the application by running the Program.py file.</p>
<p>To learn how to use the application with the dataset, follow the instructions from the previous section starting at the "Launch the application SimulFCImage.exe".</p>

<h2>Project Architecture</h2>

```bash
S5_C1_LaBabaTcheam
├─Exceptions
│ └─...
├─HMI
│ ├─assets
│ │ └─...
│ ├─MainWindow.py
│ └─SimulationChoiceWindow.py
├─LogicLayer
│ ├─Factory
│ │ ├─CreateSimulating
│ │ │ ├─ CreateBandChoiceSimulating.py
│ │ │ ├─ CreateBeeSimulating.py
│ │ │ ├─ CreateDaltonianSimulating.py
│ │ │ ├─ CreateHumanSimulating.py
│ │ │ └─ ICreateSimulator.py
│ │ ├─Simulating
│ │ │ ├─ BandChoiceSimulating.py
│ │ │ ├─ BeeSimulating.py
│ │ │ ├─ DaltonianSimulating.py
│ │ │ ├─ HumanSimulating.py
│ │ │ └─ SimulatingMethod.py
│ └─└─SimulatorFactory.py
│ ├─Band.py
│ └─ImageMS.py
├─Storage
│ ├─FileManager.py
│ └─ImageManager.py
├─UnitTests
│ └─...
├─.gitignore
├─Program.py
├─README.md
└─setup.py
```
