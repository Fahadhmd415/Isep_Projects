Hi Everyone,

I am Fahadh Mohamed, I am a masters student in wireless telecommunications and IOT system at ISEP, Paris.
In this repository, I have uploaded my Projects that I worked on through out my semesters.

Project 1 : Big data

This project involves analyzing movie data from APIs and IMDb records using Apache Airflow, organized through a Directed Acyclic Graph (DAG). Two main analyses were conducted: computing yearly average ratings and recommending highly-rated movies (above 8) released after 2000. These analyses were performed using Spark SQL queries.

Data from two APIs was processed, converted from raw formats to efficient Parquet files, and then joined using IMDb IDs with SQL(Join). The first analysis focused on calculating average ratings annually, while the second identified top-rated movies released after 2000, sorted by numVotes.

The Joined data was indexed in Elasticsearch and visualized in Kibana. Two indexes, "movies" and "moviesdata," were created. Usage 1 was represented as a vertical bar chart displaying average ratings per year, while Usage 2 utilized a data model showing numVotes and ratings, sorted descendingly. These visualizations were accessible through an Elasticsearch dashboard, enabling user-friendly data exploration.

Project 2 : IOT in healthcare

This collaborative project involved ten team members split into two groups: five focused on Mobile platforms and the other five on Fixed platforms. Mobile teams integrated sensors with Arduino, detecting step counts and fall incidents through acceleration magnitude analysis. A GPS module provided latitude and longitude data. Through USB serial communication, Arduino sent this sensor data to a Raspberry Pi 3 Model B+ acting as a powerful gateway, equipped with WiFi and Bluetooth capabilities.

The team configured the Raspberry Pi by installing Raspberry Pi OS and connecting it to Firebase, Google's cloud service. Python scripts were developed to receive data from Arduino and transmit it to Firebase in real-time. Firebase Realtime Database was used for seamless data storage and retrieval, ensuring constant synchronization.

Data visualization was achieved using HTTP, JavaScript, and Firebase Realtime Database, enabling dynamic webpage updates. The integration allowed for efficient collaboration between Mobile and Fixed platforms, with sensor data processed through Arduino, transmitted to the Raspberry Pi gateway, and visualized in real-time on the project website. This comprehensive system provided accurate monitoring of step counts, fall incidents, and GPS coordinates, enhancing the project's potential applications in real-world scenarios.

