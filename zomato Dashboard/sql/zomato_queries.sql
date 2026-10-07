create database zomate_db;


use zomate_db;


create table restaurant (
    restaurant_id int,
    restaurant_name varchar(100),
    city varchar(100),
    loactioin varchar(100),
    cuisines varchar(100),
    ranting decimal(2,1),
    votes int,
    avarage_cost_for_two int,
    online_delivery varchar(10),
    table_booking varchar(10)
);
select restaurant_name ,city , rating, votes
from restaurants
order by rating desc
limit 10;


select city,count(*) as restaurant_count
from restaurants
group by city
order by restaurant_count desc;



select city round(avg(rating),2)as average_rating
from restaurants
group by city 
order by avarage_rating;



select online_delivery,count(*) as restaurant_count
from restaurants
group by online_delivery;


select city , round(avg(average_cost_for_city), 2) as avarage_cos
FROM restaurant
group by city
order by average_cost
