
  
    

  create  table "destination_db"."public"."film_ratings__dbt_tmp"
  
  
    as
  
  (
    WITH films_with_ratings AS (
    SELECT
        f.film_id,
        f.title,
        f.release_date,
        f.price,
        f.rating, 
        f.user_rating,
        case
    when f.user_rating >= 4.5 then 'Excellent'
    when f.user_rating >= 4.0 then 'Good'
    when f.user_rating >= 3.0 then 'Average'
    else 'Poor'
end AS rating_category
    FROM films f    
),

films_with_actors AS (
    SELECT
        f.film_id,
        f.title,
        STRING_AGG(a.actor_name, ', ') AS actors
    FROM films f
    LEFT JOIN film_actors fa ON f.film_id = fa.film_id
    LEFT JOIN actors a ON fa.actor_id = a.actor_id
    GROUP BY f.film_id, f.title 
)

SELECT 
    fwr.*,
    fwa.actors
FROM films_with_ratings fwr
LEFT JOIN films_with_actors fwa ON fwr.film_id = fwa.film_id
  );
  