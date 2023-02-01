[![Badge License]][license]

<a name="readme-top"></a>

<div align = center>

# T-shirt Color sorting for Blind People

_Welcome to the CYBATHLON Vision Assistance Race repository! Here you will find the code for a race that helps blind people identify and sort different colors according to their brightness._ <br>
_Course of Designing Mechatronic System Coordinated by Fabien Verité_

<br>

## Team

[![Badge Marco]][marco]
[![Badge Abdelghani]][abdelghani]
[![Badge Joseph]][joseph]

<br>


<div align = left>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<div align = center>
<img src="https://user-images.githubusercontent.com/47824890/213506874-16201128-3250-4c21-adf6-4f93361fd6d3.png" data-canonical-src="https://user-images.githubusercontent.com/47824890/213506874-16201128-3250-4c21-adf6-4f93361fd6d3.png" width="60%"/>

 _Pilots must take the colours from the clothesline on the left and hang them on the clothesline on the right. At the end of the task the colours must be sorted by base colour and within each base colour by brightness.
 Our proposed solution is a standalone vision system, comprising of a Raspberry Pi 3B as the central processing unit, a power bank for power supply, a vision camera for image capture, and a Bluetooth speaker or headphones for audio output. The system is housed in a 3D-printed case with a belt for waist-worn portability._

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<div align = left>

### Built With

* Raspberry PI 3
* Python 3.9
* OpenCV
* GTTS
* Solidworks


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
Before installing the requirements for LINUX users this tasks has to be done:
**Install mpg123** 
  ```sh
  sudo apt-get update
  sudo apt-get install mpg123 # or mpg321
  pip3 install mpyg321
  ```
  

### Installation
In the file _[requirements.txt](https://github.com/99Abdel/Blind-Tshirt-Sorting/blob/master/requirements.txt)_ are inserted the packages needed in the Raspberry PI to run the program.
* intallation command
  ```sh
  pip install -r requirements.txt
  ```
* You may want to Install just the requirements of this package
  ```sh
  pip install -r req.txt
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

  **Set up SSH**
  **Linux Users**
  * Download this package:
  ```sh
  sudo apt install openssh-server
  ```
  
  * Then log in via terminal with the command:
  ```sh
  ssh "username of raspberry"   ex:name@namepi
  password: "password"
  ```
  
  **Windows Users**
  * Download PuTTY
  
  * Then log in via PuTTY:
    insert the full username: name@namepi


## Run the code
In order to run the code the file <a href=https://github.com/99Abdel/Blind-Tshirt-Sorting/blob/master/main.py>`main.py`</a> has to be launched. Once you are in the same file folder you can run it using 
 ```sh 
 python main.py
  ```
 * * * 
<!-- USAGE EXAMPLES -->
## Usage
The code runs both on Windows and Rasbperry PI system. However, to increase the performances and reduce the computational power, comment the **cv2.imshow()** command in the **main.py** script, at line 167. 
 Note that **The completion of this task is mandatory when operating on a Raspberry device, missing to do so will result in the script not functioning properly.**

Acceleration of the system can be achieved by modifying certain parameters in the primary Python file, though this may result in a decreased robustness of the system as a whole. The tunable parameters can be found in <a href=https://github.com/99Abdel/Blind-Tshirt-Sorting/blob/master/constants.py>`constatants.py`</a> include:
- `UP_LIM` (*Deafault = 30*): percentage of colored pixel present in the analysed frame
- `LOW_LIM` (*Deafault = 10*): percentage of colored pixel present in the analysed frame
```python
if c1_perc > cs.UP_LIM and c2_perc < cs.LOW_LIM:
        c1_num += 1
        name = c1 + str(c1_num)
    elif c2_perc > cs.UP_LIM and c1_perc < cs.LOW_LIM:
        c2_num += 1
        name = c2 + str(c2_num)
    else:
        name = 'None'
```
The parameters `UP_LIM` and `LOW_LIM` serve as thresholds in the function `utilities.recognize_color`. The code snippet determines the color of a t-shirt in an analyzed frame based on the number of pixels of color 1 and color 2. If the number of pixels of color 1 exceeds `UP_LIM` and the number of pixels of color 2 is less than `LOW_LIM`, the t-shirt is assigned color 1. Conversely, if the number of pixels of color 2 exceeds `LOW_LIM` and the number of pixels of color 1 is less than `UP_LIM`, the t-shirt is assigned color 2. Otherwise the color assigned is None.

- `N_FRAME` (*Deafault = 5*): number of consequtive frames that have to be acquired to assure stability
- `FRAME_TOLL_UP` (*Deafault = 12*) and `FRAME_TOLL_LOW` (*Deafault = 2*): are implemented to ensure that the t-shirt being analyzed is in a stationary position directly in front of the camera, rather than just temporarily passing by.
- `WHITE_THRESHOLD` (*Deafault = 20*): percentage of pixel that have to become white (meaning that the t-shirt is in front of the camera) before the analysis is performed. 

```python
if white_pixel_percentage > cs.WHITE_THRESHOLD:
                frame_list.append(white_pixel_percentage)  # Add the white pixel percentage to the frame list

                # N_FRAME (minimum to assure stability, so that the tshirt is in fron of us and not just passing by)
                if len(frame_list) >= cs.N_FRAME:
                    # Check if the difference between the maximum and minimum values in the frame list is within the
                    # specified tolerance range (minimum to assure stability, so that the tshirt is in fron of us and
                    # not just passing by)
                    if abs(max(frame_list) - min(frame_list)) < cs.FRAME_TOLL_UP and abs(
                            max(frame_list) - min(frame_list)) > cs.FRAME_TOLL_LOW:
```

Moreover the colour mask for the segmentation can be modified in the same file:

```python
color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
                  'white': [[180, 18, 255], [0, 0, 231]],
                  'red1': [[180, 255, 255], [159, 50, 70]],
                  'red2': [[9, 255, 255], [0, 50, 70]],
                  'green': [[89, 255, 255], [36, 50, 70]],
                  'blue': [[130, 255, 255], [70, 10, 2]],
                  'yellow': [[35, 255, 255], [25, 50, 70]],
                  'purple': [[158, 255, 255], [129, 50, 70]],
                  'orange': [[50, 255, 255], [5, 50, 70]],
                  'gray': [[180, 18, 230], [0, 0, 40]]}
```
* * * 


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See <a href=https://github.com/99Abdel/Blind-Tshirt-Sorting/blob/master/LICENSE>`LICENSE.txt`</a>  for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

- Marco Milanesi - <a href = "mailto: marco.milanesi.99@gmail.com">marco.milanesi.99@gmail.com</a>
- Abdelghani Msaad - <a href = "mailto: a.msaad@studenti.unibs.it">a.msaad@studenti.unibs.it</a>
- Joseph Dittrick - <a href = "mailto: joseph.dittrick@etu.sorbonne-universite.fr">joseph.dittrick@etu.sorbonne-universite.fr</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!----------------------------------------------------------------------------->

[marco]: https://github.com/marco-milanesi
[abdelghani]: https://github.com/99Abdel
[joseph]: https://github.com/JoJolM
[license]: LICENSE

<!---------------------------------{ Badges }---------------------------------->

[badge license]: https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge
[badge marco]: https://img.shields.io/badge/Marco_Milanesi-4776c1?style=for-the-badge
[badge abdelghani]: https://img.shields.io/badge/Msaad_Abdelghani-2930c1?style=for-the-badge
[badge joseph]: https://img.shields.io/badge/Joseph_Dittrick-9cf?style=for-the-badge
