Hi Everyone,

I am Fahadh Mohamed, I am a masters student in wireless telecommunications and IOT system at ISEP, Paris.
In this repository, I have uploaded my Projects that I worked on through out my semesters.

#Project 1 : Big data

This project involves analyzing movie data from APIs and IMDb records using Apache Airflow, organized through a Directed Acyclic Graph (DAG). Two main analyses were conducted: computing yearly average ratings and recommending highly-rated movies (above 8) released after 2000. These analyses were performed using Spark SQL queries.

Data from two APIs was processed, converted from raw formats to efficient Parquet files, and then joined using IMDb IDs with SQL(Join). The first analysis focused on calculating average ratings annually, while the second identified top-rated movies released after 2000, sorted by numVotes.

The Joined data was indexed in Elasticsearch and visualized in Kibana. Two indexes, "movies" and "moviesdata," were created. Usage 1 was represented as a vertical bar chart displaying average ratings per year, while Usage 2 utilized a data model showing numVotes and ratings, sorted descendingly. These visualizations were accessible through an Elasticsearch dashboard, enabling user-friendly data exploration.
