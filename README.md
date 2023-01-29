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

 _Pilots must take the colours from the clothesline on the left and hang them on the clothesline on the right. At the end of the task the colours must be sorted by base 
colour and within each base colour by brightness._

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
Before installing the requirements it is advisable to:

**Install mpg123** 
- npm
  ```sh
  npm install npm@latest -g
  ```
**Set up SSH**

### Installation
In the file _[requirements.txt](https://github.com/99Abdel/Blind-Tshirt-Sorting/blob/master/requirements.txt)_ are inserted the packages needed in the Raspberry PI to run the program.
* intallation command
  ```sh
  pip install -r requirements.txt
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
The code runs both on Windows and Rasbperry PI system. However, to increase the performances and reduce the computational power, comment the imshow ... 

Acceleration of the system can be achieved by modifying certain parameters in the primary Python file, though this may result in a decreased robustness of the system as a whole. The tunable parameters include:
- `UP_LIM` (*Deafault = 30*): percentage of colored pixel present in the analysed frame
- `LOW_LIM` (*Deafault = 10*): percentage of colored pixel present in the analysed frame
- `N_FRAME` (*Deafault = 5*): number of frames that have to be considered
- `FRAME_TOLL_UP` (*Deafault = 12*):
- `FRAME_TOLL_LOW` (*Deafault = 2*):
- `WHITE_THRESHOLD` (*Deafault = 20*): percentage of pixel that have to become white (meaning that the t-shirt is in front of the camera) before the analysis is performed. 

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
